# Xircuits Google Drive Component Library

Component library based on the [PyDrive2](https://github.com/iterative/PyDrive2) library.


## Installation

```
pip install -r requirements.txt
```

To use this component library, simply copy the directory / clone or submodule the repository to your working Xircuits project directory.

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