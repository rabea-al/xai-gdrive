from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive



@xai_component
class GDriveServiceAuth(Component):
    """A component that authenticates with Google Drive using a service account.

    ##### inPorts:
    - json_path: the path to the service account's secrets JSON file.
    """
    json_path: InCompArg[str]
    gauth: OutArg[any]
    gdrive: OutArg[any]

    def execute(self, ctx) -> None:

        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_file_path": self.json_path.value,
            }
        }
        # Create instance of GoogleAuth
        gauth = GoogleAuth(settings=settings)
        gauth.ServiceAuth()

        # Save gauth in the context for other components to use
        ctx.update({'gauth': gauth})
        self.gauth.value = gauth

        self.gdrive.value = GoogleDrive(gauth)
        ctx.update({'gdrive': self.gdrive.value})


@xai_component
class GDriveUserOAuth(Component):
    """A component that authenticates with Google Drive using a service account.
    """

    json_path: InArg[str]
    gauth: OutArg[any]
    gdrive: OutArg[any]

    def execute(self, ctx) -> None:

        gauth = GoogleAuth()
        
        if self.json_path.value:
            gauth.LoadClientConfigFile(self.json_path.value)
        else:
            gauth.LoadClientConfigFile('token.json')
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