import io
import logging
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import aiohttp
from googleapiclient.http import MediaIoBaseUpload
import urllib

logger = logging.getLogger(__name__)


class UpdateAirtable:
    def __init__(self, airtable_api_key, airtable_base_id, airtable_table_name, parent_folder_id):
        """
        Initialize the UpdateAirtable class with Airtable and Google Drive credentials.

        Args:
            airtable_api_key (str): API key for Airtable authentication
            airtable_base_id (str): ID of the Airtable base
            airtable_table_name (str): Name of the Airtable table
            parent_folder_id (str): ID of the parent folder in Google Drive where files will be uploaded
        """
        self.airtable_api_key = airtable_api_key
        self.airtable_base_id = airtable_base_id
        self.airtable_table_name = airtable_table_name
        self.parent_folder_id = parent_folder_id

    def update(self, file_id, candidate_id, column_name):
        """
        Update an Airtable record with a Google Drive file link.

        Args:
            file_id (str): ID of the file in Google Drive
            candidate_id (str): ID of the record in Airtable to update
            column_name (str): Name of the column in Airtable to update with the file link

        Returns:
            dict: Dictionary containing the status of the update operation
        """
        # The Google Drive direct link
        file_link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
        table_encoded = urllib.parse.quote(self.airtable_table_name)
        logger.info(
            f"Updating Airtable with file link: {file_link} {column_name} {candidate_id}")
        # Set up the Airtable API request
        update_url = f"https://api.airtable.com/v0/{self.airtable_base_id}/{table_encoded}/{candidate_id}"
        logger.info(
            f"UPDATE URL: {update_url}")
        # Set up the Airtable API request
        headers = {
            "Authorization": f"Bearer {self.airtable_api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "fields": {
                column_name: file_link
            }
        }

        # Send the update request
        requests.patch(
            update_url, headers=headers, json=data)

        # Return the response
        return {
            "status": "link updated",
            "id": candidate_id,
            "update column": column_name
        }

    async def send_to_google_drive(self, file_byte, excelname):
        """
        Upload a file to Google Drive.

        Args:
            file_byte (bytes): Binary data of the file to upload
            excelname (str): Name to give the uploaded file

        Returns:
            dict: Dictionary containing the status, file ID, and file link of the uploaded file
        """
        SERVICE_ACCOUNT_FILE = "./config-google-service.json"
        SCOPES = ['https://www.googleapis.com/auth/drive.file']

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        drive_service = build("drive", "v3", credentials=credentials)

        file_metadata = {
            "name": excelname,
            "parents": [self.parent_folder_id],
        }

        EXCEL_FILE = io.BytesIO(file_byte)

        media = MediaIoBaseUpload(
            EXCEL_FILE, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        uploaded_file = drive_service.files().create(
            body=file_metadata, media_body=media, fields="id, webViewLink").execute()

        file_id = uploaded_file.get("id")
        file_link = uploaded_file.get("webViewLink")

        return {
            "status": "success",
            "file_id": file_id,
            "file_link": file_link,
        }

    async def download_file(self, url):
        """
        Download a file from a URL asynchronously.

        Args:
            url (str): URL of the file to download

        Returns:
            bytes: Binary content of the downloaded file, or None if download fails
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.read()

        return None
