from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pprint import pprint

@xai_component
class GDriveAuth(Component):
    """A component that authenticates with Google Drive using a service account.
    """
    gauth: OutArg[any]


    def execute(self, ctx) -> None:

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        # Save gauth in the context for other components to use
        ctx.update({'gauth': gauth})
        self.gauth.value = gauth


# @xai_component
# class GDriveAuthService(Component):
#     """A component that authenticates with Google Drive using a service account.

#     ##### inPorts:
#     - json_path: the path to the service account's secrets JSON file.
#     """
#     json_path: InCompArg[str]
#     gauth: OutArg[any]


#     def execute(self, ctx) -> None:
#         json_path = self.json_path.value

#         settings = {
#             "client_config_backend": "service",
#             "service_config": {
#                 "client_json_file_path": json_path,
#             }
#         }
#         # Create instance of GoogleAuth
#         gauth = GoogleAuth(settings=settings)
#         # Authenticate
#         gauth.ServiceAuth()

#         # Save gauth in the context for other components to use
#         ctx.update({'gauth': gauth})
#         self.gauth.value = gauth


@xai_component
class GetFilesByQuery(Component):
    """A component that gets files from Google Drive based on a complex query.

    ##### inPorts:
    - filename: the name of the file to search for.
    - mimetype: the MIME type of the file to search for.
    """
    gauth: InArg[any]
    filename: InCompArg[str]
    mimetype: InCompArg[str]
    files: OutArg[any]

    def execute(self, ctx) -> None:
        gauth = self.gauth.value if self.gauth.value else ctx["gauth"]
        filename = self.filename.value
        mimetype = self.mimetype.value

        # Create a new GoogleDrive instance
        drive = GoogleDrive(gauth)

        # Query
        query = {'q': f"title = '{filename}' and mimeType='{mimetype}'"}
        
        # Get list of files that match against the query
        files = drive.ListFile(query).GetList()
        pprint(files)

        # Save the file list in the context for other components to use
        ctx.update({'files': files})
        self.files.value = files


@xai_component(color="green")
class UploadFileToGDrive(Component):
    """A component that uploads a file to a specific folder on Google Drive.

    ##### inPorts:
    - file_path: the path to the file to upload.
    - folder_id: the ID of the folder to upload the file to.
    - filename: the name to give the uploaded file.
    """
    gauth: InArg[any]
    file_path: InCompArg[str]
    folder_id: InCompArg[str]
    filename: InCompArg[str]
    mimetype: InArg[str]

    def execute(self, ctx) -> None:

        import mimetypes

        file_path = self.file_path.value
        folder_id = self.folder_id.value
        filename = self.filename.value

        # Determine the MIME type of the file
        if self.mimetype.value is None:
            mimetype, _ = mimetypes.guess_type(file_path)
        else:
            mimetype = self.mimetype.value

        # Create a new GoogleDrive instance
        gauth = self.gauth.value if self.gauth.value else ctx["gauth"]
        drive = GoogleDrive(gauth)

        # Define file metadata, including the target folder ID
        metadata = {
            'parents': [{"id": folder_id}],
            'title': filename,
            'mimeType': mimetype
        }

        # Create a new GoogleDriveFile instance and set its content to the image file
        file = drive.CreateFile(metadata=metadata)
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
    gauth: InArg[any]
    file_id: InCompArg[str]
    output_path: InCompArg[str]

    def execute(self, ctx) -> None:
        file_id = self.file_id.value
        output_path = self.output_path.value

        # Create a new GoogleDrive instance
        gauth = self.gauth.value if self.gauth.value else ctx["gauth"]
        drive = GoogleDrive(gauth)

        # Initialize a GoogleDriveFile instance with the given file ID
        file = drive.CreateFile({'id': file_id})

        # Download the file and save it to the specified output path
        file.GetContentFile(output_path)
