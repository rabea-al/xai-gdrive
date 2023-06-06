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

The downloaded file has all authentication information of your application. Rename the file to “client_secrets.json” and place it in your working directory.