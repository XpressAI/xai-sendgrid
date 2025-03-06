<p align="center">
  <a href="https://github.com/XpressAI/xircuits/tree/master/xai_components#xircuits-component-library-list">Component Libraries</a> •
  <a href="https://github.com/XpressAI/xircuits/tree/master/project-templates#xircuits-project-templates-list">Project Templates</a>
  <br>
  <a href="https://xircuits.io/">Docs</a> •
  <a href="https://xircuits.io/docs/Installation">Install</a> •
  <a href="https://xircuits.io/docs/category/tutorials">Tutorials</a> •
  <a href="https://xircuits.io/docs/category/developer-guide">Developer Guides</a> •
  <a href="https://github.com/XpressAI/xircuits/blob/master/CONTRIBUTING.md">Contribute</a> •
  <a href="https://www.xpress.ai/blog/">Blog</a> •
  <a href="https://discord.com/invite/vgEg2ZtxCw">Discord</a>
</p>

<p align="center"><i>Xircuits Component Library for SendGrid! Seamlessly send and receive emails within Xircuits workflows.</i></p>

---

## Xircuits Component Library for SendGrid

The Xircuits SendGrid Component Library enables seamless integration with SendGrid’s email services, allowing users to send emails, parse incoming emails, and manage attachments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Main Xircuits Components](#main-xircuits-components)
- [Installation](#installation)

## Prerequisites

Before you begin, make sure you have the following:

1. Python 3.9+.
2. Xircuits.
3. SendGrid API key.


## Main Xircuits Components

### SendGridSendEmail Component:  
Sends an email using SendGrid’s API. Requires an API key, sender, recipient, subject, and message body.  

<img src="https://github.com/user-attachments/assets/cff452b5-c495-4022-bda7-2bd8caa0b34c" alt="Image" width="200" height="200" />

### SendgridParseExtractEmail Component:  
Extracts email data received via the SendGrid Inbound Parse Webhook, including sender, recipient, subject, body, and attachments.  

<img src="https://github.com/user-attachments/assets/8c0a4982-e333-436e-b726-6202f61aa5c7" alt="Image" width="200" height="200" />

### SendgridParseCleanAttachments Component:  
Deletes downloaded attachments from parsed emails to maintain a clean storage environment.  

<img src="https://github.com/user-attachments/assets/700a8f6d-587c-4537-833a-0203451e290c" alt="Image" width="250" height="100" />

## Installation

To use this component library, ensure that you have an existing [Xircuits setup](https://xircuits.io/docs/main/Installation). You can then install the SendGrid library using the [component library interface](https://xircuits.io/docs/component-library/installation#installation-using-the-xircuits-library-interface), or through the CLI using:

```
xircuits install sendgrid
```

You can also install it manually by cloning the repository:

```
# base Xircuits directory

git clone https://github.com/XpressAI/xai-sendgrid xai_components/xai_sendgrid
pip install -r xai_components/xai_sendgrid/requirements.txt
```

