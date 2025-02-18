from xai_components.base import InArg, InCompArg, OutArg, Component, BaseComponent, xai_component, secret
import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from flask import request
import base64
import email
import mimetypes
from six import iteritems
from werkzeug.utils import secure_filename
import re


class Parse(object):

    def __init__(self, request):
        self._request = request
        request.get_data(as_text=True)
        self._payload = request.form
        self._raw_payload = request.data

    def key_values(self):
        """
        Return a dictionary of key/values in the payload received from
        the webhook
        """
        key_values = {}
        for key in self.keys:
            if key in self.payload:
                key_values[key] = self.payload[key]
        return key_values

    def get_raw_email(self):
        """
        This only applies to raw payloads:
        https://sendgrid.com/docs/Classroom/Basics/Inbound_Parse_Webhook/setting_up_the_inbound_parse_webhook.html#-Raw-Parameters
        """
        if 'email' in self.payload:
            raw_email = email.message_from_string(self.payload['email'])
            return raw_email
        else:
            return None

    def attachments(self):
        """Returns an object with:
        type = file content type
        file_name = the name of the file
        contents = base64 encoded file contents"""
        attachments = None
        if 'attachment-info' in self.payload:
            attachments = self._get_attachments(self.request)
        # Check if we have a raw message
        raw_email = self.get_raw_email()
        if raw_email is not None:
            attachments = self._get_attachments_raw(raw_email)
        return attachments

    def _get_attachments(self, request):
        attachments = []
        for _, filestorage in iteritems(request.files):
            attachment = {}
            if filestorage.filename not in (None, 'fdopen', '<fdopen>'):
                filename = secure_filename(filestorage.filename)
                attachment['type'] = filestorage.content_type
                attachment['file_name'] = filename
                attachment['contents'] = base64.b64encode(filestorage.read())
                attachments.append(attachment)
        return attachments

    def _get_attachments_raw(self, raw_email):
        attachments = []
        counter = 1
        for part in raw_email.walk():
            attachment = {}
            if part.get_content_maintype() == 'multipart':
                continue
            filename = part.get_filename()
            if not filename:
                ext = mimetypes.guess_extension(part.get_content_type())
                if not ext:
                    ext = '.bin'
                filename = 'part-%03d%s' % (counter, ext)
            counter += 1
            attachment['type'] = part.get_content_type()
            attachment['file_name'] = filename
            attachment['contents'] = part.get_payload(decode=False)
            attachments.append(attachment)
        return attachments

    @property
    def keys(self):
        return self._keys

    @property
    def request(self):
        return self._request

    @property
    def payload(self):
        return self._payload

    @property
    def raw_payload(self):
        return self._raw_payload

def extract_email(full_email: str) -> str:
        """Extracts the email address from a string formatted as 'Name <email>'."""
        match = re.search(r'<([^>]+)>', full_email)
        return match.group(1) if match else full_email

@xai_component
class SendGridSendEmail(Component):
    """A Xircuits component to send an email using SendGrid.

    ##### inPorts:
    - api_key: The SendGrid API key.
    - from_address: The email address of the sender.
    - to_address: The email address who will receive the email.
    - subject: The subject of the email.
    - message: The message content of the email.

    """
    api_key: InArg[secret]
    from_address: InCompArg[str]
    to_address: InCompArg[str]
    subject: InCompArg[str]
    message: InCompArg[str]

    def execute(self, ctx) -> None:
        api_key = self.api_key.value if self.api_key.value is not None else os.getenv("SENDGRID_API_KEY")
        sender_email = extract_email(self.from_address.value)
        receiver_email = extract_email(self.to_address.value)
        subject = self.subject.value
        message = self.message.value

        print(f"Sending: To: {receiver_email} From: {sender_email} Subject: {subject} Message: {message}", flush=True)

        
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        from_email = Email(sender_email)
        to_email = To(receiver_email)
        email_content = Content("text/plain", message)
        mail = Mail(from_email, to_email, subject, email_content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()
        print(f"About to send: {mail_json}")

        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code != 202:
            raise Exception(f"Failed to send email. Status code: {response.status_code}")



@xai_component
class SendgridParseExtractEmail(Component):
    """Extracts email data received via the SendGrid Inbound Parse webhook.

    ##### outPorts:
    - to: The recipient(s) of the email.
    - from_addr: The sender of the email.
    - subject: The subject line of the email.
    - body: The body content of the email.
    - attachment_paths: List of file paths for the downloaded attachments.
    """

    to: OutArg[str]
    from_addr: OutArg[str]
    subject: OutArg[str]
    body: OutArg[str]
    attachment_paths: OutArg[list]

    def execute(self, ctx) -> None:
        parse = Parse(request)

        # Debugging statements to log the payload
        #print("Raw Payload:", parse.raw_payload)
        #print("Parsed Payload:", parse.payload)

        # Extract email data directly from the payload
        self.to.value = parse.payload.get('to', None)
        self.from_addr.value = parse.payload.get('from', None)
        self.subject.value = parse.payload.get('subject', None)
        self.body.value = parse.payload.get('text', None)  # Using 'text' for plain text body

        # Debugging output
        print("Extracted 'To':", self.to.value)
        print("Extracted 'From':", self.from_addr.value)
        #print("Extracted 'Subject':", self.subject.value)
        #print("Extracted 'Body':", self.body.value)

        attachments = parse.attachments() or []  # Ensure attachments is a list even if None
        attachment_paths = []

        for attachment in attachments:
            try:
                file_path = os.path.join('/data/home/attachments', attachment['file_name'])
                with open(file_path, 'wb') as file:
                    file.write(base64.b64decode(attachment['contents']))
                attachment_paths.append(file_path)
            except (binascii.Error, TypeError) as e:
                print(f"Error decoding attachment {attachment['file_name']}: {e}")

        self.attachment_paths.value = attachment_paths

        # Debugging output for attachments
        #print("Attachment Paths:", self.attachment_paths.value)



@xai_component
class SendgridParseCleanAttachments(Component):
    """Deletes downloaded attachment files.

    ##### inPorts:
    - attachment_paths: List of file paths to be deleted.
    """

    attachment_paths: InCompArg[list]

    def execute(self, ctx) -> None:
        if self.attachment_paths.value:
            for file_path in self.attachment_paths.value:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")