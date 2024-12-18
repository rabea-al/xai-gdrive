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





<p align="center"><i>Xircuits Component Library for Google Drive! Seamlessly integrate and manage your Google Drive files and folders.</i></p>

---
## Xircuits Component Library for Google Drive

This library integrates Google Drive functionalities into Xircuits, enabling seamless file management. It supports authentication, file uploads, downloads, queries, and updates using Google Drive APIs.

## Table of Contents

- [Preview](#preview)
- [Prerequisites](#prerequisites)
- [Main Xircuits Components](#main-xircuits-components)
- [Try the Examples](#try-the-examples)
- [Installation](#installation)

## Preview

### GDriveSimpleDownload Example

<img src="https://github.com/user-attachments/assets/621a7bb1-ad5f-436c-8acb-d544539e1bde" alt="GDriveSimpleDownload" />

### GDriveSimpleUpdate Example  

<img src="https://github.com/user-attachments/assets/339989fd-9e37-4d91-9eba-92e88553b810" alt="GDriveSimpleUpdate" />

### GDriveSimpleUpload Example  

<img src="https://github.com/user-attachments/assets/6b9f9816-d248-43c3-a219-213dc5def20b" alt="GDriveSimpleUpload" />

## Prerequisites

Before you begin, you will need the following:

1. Python3.9+.
2. Xircuits.

## Main Xircuits Components

### GDriveServiceAuth Component:
Authenticates with Google Drive using a service account JSON file.

<img src="https://github.com/user-attachments/assets/1894340b-dcba-489c-bc77-f2285371a736" alt="GDriveServiceAuth" width="200" height="100" />

### GetFilesByQuery Component:
Searches for files in Google Drive using a specified filename and MIME type.

<img src="https://github.com/user-attachments/assets/5b2b7cba-d559-4e1b-80a2-df89e89a9e29" alt="GetFilesByQuery" width="200" height="150" />

### UpdateFileInGDrive Component:
Updates an existing file in Google Drive or uploads a new file if not found.

<img src="https://github.com/user-attachments/assets/ad74a8c0-9531-40c6-a987-1222f0565f2e" alt="UpdateFileInGDrive" width="200" height="150" />

### GDriveUserOAuth Component:
Authenticates with Google Drive using OAuth for user accounts.


### UploadFileToGDrive Component:
Uploads a file to a specific folder on Google Drive with optional metadata.

### DownloadFileFromGDrive Component:
Downloads a file from Google Drive to a specified local path.

### GDriveFileSystem Component:
Creates a Google Drive file system using a service account for folder management.

## Try the Examples

We have provided an example workflow to help you get started with the Google Drive component library. Give it a try and see how you can create custom Google Drive components for your applications.

### GDriveSimpleDownload Example  
This example authenticates with Google Drive using a service account and downloads a specified file by its `file_id`, saving it locally.

### GDriveSimpleUpdate Example  
This example authenticates with Google Drive using a service account and updates the content of a file in a specified folder. If the file does not exist, it uploads it as a new file.

### GDriveSimpleUpload Example  
This example authenticates with Google Drive using a service account and uploads a file to a specified folder, allowing custom file naming during the upload process.

## Installation


To use this component library, ensure that you have an existing [Xircuits setup](https://xircuits.io/docs/main/Installation). You can then install the GDrive library using the [component library interface](https://xircuits.io/docs/component-library/installation#installation-using-the-xircuits-library-interface), or through the CLI using:

```
xircuits install gdrive
```
You can also do it manually by cloning and installing it:
```
# base Xircuits directory
git clone https://github.com/XpressAI/xai_gdrive xai_components/xai_gdrive
pip install -r xai_components/xai_gdrive/requirements.txt 
```

## Finding GDrive IDs
- To get the folder id, navigate to your GDrive directory and copy the last part of the string: https://drive.google.com/drive/folders/`the-folder-id-string`
- To get a file id, navigate to your file > right-click > copy link. You should get a link like this: https://drive.google.com/file/d/`the-file-id-string`/view?usp=drive_link

## Authentication

[[Source](https://docs.gspread.org/en/latest/oauth2.html)]

To access a drive via Google Drive API you need to authenticate and authorize your application. If you plan to access Google Drive on behalf of a bot account use Service Account. If you’d like to access spreadsheets on behalf of end users (including yourself) use OAuth Client ID. 

### Getting Service Credentials

A service account is a special type of Google account intended to represent a non-human user that needs to authenticate and be authorized to access data in Google APIs.

Since it’s a separate account, by default it does not have access to any drives until you share it with this account. Just like any other Google account.

1. Enable API Access.
    1. Head to Google Developers Console and create a new project (or select the one you already have).
    2. In the box labeled “Search for APIs and Services”, search for “Google Drive API” and enable it.
2. Go to “APIs & Services > Credentials” and choose “Create credentials > Service account key”.
3. Fill out the form
4. Click “Create” and “Done”.
5. Press “Manage service accounts” above Service Accounts.
6. Press on ⋮ near recently created service account and select “Manage keys” and then click on “ADD KEY > Create new key”.
7. Select JSON key type and press “Create”.
You will automatically download a JSON file with credentials. It may look like this:
    ```
    {
        "type": "service_account",
        "project_id": "api-project-XXX",
        "private_key_id": "2cd … ba4",
        "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
        "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
        "client_id": "473 … hd.apps.googleusercontent.com",
        ...
    }
    ```
  Remember the path to the downloaded credentials file. Also, in the next step you’ll need the value of client_email from this file.

8. **Very important!** Go to your google drive directory and share it with a client_email from the step above. Just like you do with any other Google account.
9. Place the credentials in a place that jupyterlab can access. You can then pass the path in the `GSDriveServiceAuth` component.

### Getting OAuth Credentials

[[source](https://docs.iterative.ai/PyDrive2/quickstart/#authentication)]

1. Go to APIs Console and make your own project.
2. Search for `Google Drive API`, select the entry, and click `Enable`.
3. Select [`Credentials`](https://console.cloud.google.com/apis/credentials) from the left menu, click `Create Credentials` from the top bar, select `OAuth client ID`.
4. Now, the product name and consent screen need to be set -> click `Configure consent screen` and follow the instructions. Once finished:
    a. Select `Application type` to be Web application.
    b. Enter an appropriate name.
    c. Input http://localhost:8080/ for `Authorized redirect URIs`.
    d. Click `Create`.
5. Click `Download JSON` on the right side of Client ID to download client_secret_<really long ID>.json.

    The downloaded file has all authentication information of your application. Rename the file to “client_secrets.json” and place it in your root working directory, or pass the .json path to the `GDriveUserOAuth` component.