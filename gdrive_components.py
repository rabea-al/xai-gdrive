from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.fs import GDriveFileSystem
import json
import os
import base64

def get_auth_type_from_json(json_obj):
    if isinstance(json_obj, dict):
        if 'web' in json_obj:
            return 'OAuth User'
        elif 'type' in json_obj and json_obj['type'] == 'service_account':
            return 'Service Auth'
    return 'Unknown type'

@xai_component
class GDriveServiceAuth(Component):
    """A component that authenticates with Google Drive using a service account.

    ##### inPorts:
    - json_path: the path to the service account's secrets JSON file.
    """
    GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_path: InArg[str]
    gauth: OutArg[any]
    gdrive: OutArg[any]

    def execute(self, ctx) -> None:
        json_path = self.GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_path.value

        if json_path and os.path.exists(json_path):
            print(f"Using provided service account JSON: {json_path}")
            with open(json_path, 'r') as f:
                GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_dict = json.load(f)
        else:
            print("Provided path is empty or does not exist. Checking environment variable...")
            encoded_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_CREDENTIALS")

            if not encoded_json:
                raise ValueError("Neither a valid file path nor GOOGLE_SERVICE_ACCOUNT_CREDENTIALS environment variable was found.")

            GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_dict = json.loads(base64.b64decode(encoded_json).decode())

        auth_type = get_auth_type_from_json(GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_dict)
        if auth_type != 'Service Auth':
            raise ValueError(f'Expected a Service Auth JSON file, but got {auth_type}')

        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_dict": GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_dict,
            }
        }

        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()

        ctx.update({'gauth': gauth})
        self.gauth.value = gauth

        self.gdrive.value = GoogleDrive(gauth)
        ctx.update({'gdrive': self.gdrive.value})

        print("Google Drive authentication completed successfully.")
        
@xai_component
class GDriveUserOAuth(Component):
    """A component that authenticates with Google Drive using a service account.
    """

    oauth_json_path: InArg[str]
    gauth: OutArg[any]
    gdrive: OutArg[any]

    def execute(self, ctx) -> None:

        gauth = GoogleAuth()
        
        if self.oauth_json_path.value:
            auth_type = get_auth_type_from_json(self.oauth_json_path.value)

            if auth_type != 'OAuth User':
                raise ValueError(f'Expected a OAuth User JSON file, but got {auth_type}')

            gauth.LoadClientConfigFile(self.oauth_json_path.value)
        
        gauth.LocalWebserverAuth()

        ctx.update({'gauth': gauth})
        self.gauth.value = gauth

        self.gdrive.value = GoogleDrive(gauth)
        ctx.update({'gdrive': self.gdrive.value})


@xai_component
class GetFilesByQuery(Component):
    """A component that gets files from Google Drive based on a complex query.

    ##### inPorts:
    - filename: the name of the file to search for.
    - mimetype: the MIME type of the file to search for.
    """
    gdrive: InArg[any]
    filename: InCompArg[str]
    mimetype: InCompArg[str]
    files: OutArg[any]

    def execute(self, ctx) -> None:
        gdrive = self.gdrive.value if self.gdrive.value else ctx["gdrive"]
        filename = self.filename.value
        mimetype = self.mimetype.value

        # Query
        query = {'q': f"title = '{filename}' and mimeType='{mimetype}'"}
        
        # Get list of files that match against the query
        self.files.value = gdrive.ListFile(query).GetList()


@xai_component(color="green")
class UploadFileToGDrive(Component):
    """A component that uploads a file to a specific folder on Google Drive.

    ##### inPorts:
    - file_path: the path to the file to upload.
    - folder_id: the ID of the folder to upload the file to.
    - filename: the name to give the uploaded file.
    """

    gdrive: InArg[any]
    file_path: InCompArg[str]
    folder_id: InCompArg[str]
    filename: InArg[str]
    mimetype: InArg[str]

    def execute(self, ctx) -> None:

        import os
        import mimetypes

        file_path = self.file_path.value
        folder_id = self.folder_id.value
        filename = self.filename.value if self.filename.value else os.path.basename(file_path)

        # Determine the MIME type of the file
        if self.mimetype.value is None:
            mimetype, _ = mimetypes.guess_type(file_path)
        else:
            mimetype = self.mimetype.value

        # Create a new GoogleDrive instance
        gdrive = self.gdrive.value if self.gdrive.value else ctx["gdrive"]

        # Define file metadata, including the target folder ID
        metadata = {
            'parents': [{"id": folder_id}],
            'title': filename,
            'mimeType': mimetype
        }

        # Create a new GoogleDriveFile instance and set its content to the image file
        file = gdrive.CreateFile(metadata=metadata)
        file.SetContentFile(file_path)

        # Upload the file to Google Drive
        file.Upload()


@xai_component
class DownloadFileFromGDrive(Component):
    """A component that downloads a file from Google Drive.

    ##### inPorts:
    - file_id: the ID of the file to download.
    - output_path: the path to save the downloaded file.
    """
    gdrive: InArg[any]
    file_id: InCompArg[str]
    output_path: InCompArg[str]

    def execute(self, ctx) -> None:
        file_id = self.file_id.value
        output_path = self.output_path.value

        # Create a new GoogleDrive instance
        gdrive = self.gdrive.value if self.gdrive.value else ctx["gdrive"]

        # Initialize a GoogleDriveFile instance with the given file ID
        file = gdrive.CreateFile({'id': file_id})

        # Download the file and save it to the specified output path
        file.GetContentFile(output_path)


@xai_component
class GDriveFileSystem(Component):
    """
    Component to create a Google Drive File System instance.
    """

    json_path: InArg[str]
    folder_id: InArg[str]
    fs: OutArg[any]

    def __init__(self):
        super().__init__()
        self.folder_id.value = "root"

    def execute(self, ctx) -> None:
        json_path = self.json_path.value

        if json_path and os.path.exists(json_path):
            print(f"Using provided JSON key file: {json_path}")
            with open(json_path, 'r') as f:
                GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_dict = json.load(f)
        else:
            print("Provided path is empty or does not exist. Checking environment variable...")
            encoded_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_CREDENTIALS")

            if not encoded_json:
                raise ValueError("Neither a valid file path nor GOOGLE_SERVICE_ACCOUNT_CREDENTIALS environment variable was found.")

            GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_dict = json.loads(base64.b64decode(encoded_json).decode())

        self.fs.value = GDriveFileSystem(
            self.folder_id.value,
            use_service_account=True,
            client_json_dict=GOOGLE_SERVICE_ACCOUNT_CREDENTIALS_dict,
        )

        ctx.update({'fs': self.fs.value})
        print("Google Drive File System initialized successfully.")

@xai_component
class UpdateFileInGDrive(Component):
    """A component that updates the content of an existing file in Google Drive
    or uploads a new file if no match is found in the specified folder.

    ##### inPorts:
    - gdrive: the GoogleDrive instance.
    - file_path: the path to the local file whose content will be used.
    - folder_id: the ID of the folder to search within (default is 'root').
    - filename: the name of the file in Google Drive.
    """

    gdrive: InArg[any]
    file_path: InCompArg[str]
    folder_id: InCompArg[str]
    filename: InCompArg[str]

    def execute(self, ctx) -> None:
        import hashlib
        from os.path import basename, exists

        gdrive = self.gdrive.value if self.gdrive.value else ctx["gdrive"]
        folder_id = self.folder_id.value if self.folder_id.value else "root"
        file_path = self.file_path.value
        filename = self.filename.value if self.filename.value else basename(file_path)

        # Check if the local file exists
        if not exists(file_path):
            print(f"The file '{file_path}' does not exist locally. Please check the path and try again.")
            return

        # Function to calculate file hash (MD5)
        def calculate_file_hash(file_path):
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()

        local_file_hash = calculate_file_hash(file_path)

        # Search for the file in the specified folder
        query = f"'{folder_id}' in parents and title='{filename}' and trashed=false"
        file_list = gdrive.ListFile({"q": query}).GetList()

        if len(file_list) == 1:
            gdrive_file = file_list[0]

            # Compare MD5 hash to avoid unnecessary uploads
            if 'md5Checksum' in gdrive_file and gdrive_file['md5Checksum'] == local_file_hash:
                print(f"The file '{filename}' is already up-to-date in Google Drive (File ID: {gdrive_file['id']}).")
                return

            # Update existing file content
            gdrive_file.SetContentFile(file_path)
            gdrive_file.Upload()
            print(f"Updated the file '{filename}' in Google Drive (File ID: {gdrive_file['id']}).")
        else:
            # Create and upload a new file if not found
            metadata = {
                "parents": [{"id": folder_id}],
                "title": filename,
            }
            gdrive_file = gdrive.CreateFile(metadata)
            gdrive_file.SetContentFile(file_path)
            gdrive_file.Upload()
            print(f"Uploaded a new file '{filename}' to Google Drive (File ID: {gdrive_file['id']}).")
