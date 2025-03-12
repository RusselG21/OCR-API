from fastapi import FastAPI, File, UploadFile
from src.extractors import CVExtractor, BirthCertExtractor, IDExtractor, DiplomaExtractor, WorkPerminExtractor, AirtableExtractor
import os
import logging
import sys
from src.utils import ExtractionProcess
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set up logging with detailed information
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI()

headers = {"Ocp-Apim-Subscription-Key": "1afe622ee4aa47439faa619583316758"}
header_airtable = "patsgONcHhgZccHRk.dccf8082dbdb03e1a5182e32f57ea29c82f543c8dfb3246c32e8c90d0bf4c54f"


@app.post("/extract_cv")
async def extract(file: UploadFile = File(...)):
    """
    Extract information from a CV/resume document.

    Args:
        file (UploadFile): The CV document file to be processed.

    Returns:
        dict: Extracted information from the CV in a structured format.
    """
    extrator = ExtractionProcess(CVExtractor, file, headers)
    result = await extrator.proccess_extraction()
    return result


@app.post("/extract_birth_cert")
async def extract_birth_cert(file: UploadFile = File(...)):
    """
    Extract information from a birth certificate document.

    Args:
        file (UploadFile): The birth certificate document file to be processed.

    Returns:
        dict: Structured data extracted from the birth certificate.
    """
    extrator = ExtractionProcess(BirthCertExtractor, file, headers)
    result = await extrator.proccess_extraction()
    return result


@app.post("/extract_id")
async def extract_id(file: UploadFile = File(...)):
    """
    Extract information from an ID document.

    Args:
        file (UploadFile): The ID document file to be processed.

    Returns:
        dict: Structured data extracted from the ID document.
    """
    extrator = ExtractionProcess(IDExtractor, file, headers)
    result = await extrator.proccess_extraction()
    return result


@app.post("/extract_diploma")
async def extract_diploma(file: UploadFile = File(...)):
    """
    Extract information from a diploma or educational certificate.

    Args:
        file (UploadFile): The diploma document file to be processed.

    Returns:
        dict: Structured data extracted from the diploma document.
    """
    extrator = ExtractionProcess(DiplomaExtractor, file, headers)
    result = await extrator.proccess_extraction()
    return result


@app.post("/extract_working_permit")
async def extract_working_permit(file: UploadFile = File(...)):
    """
    Extract information from a working permit document.

    Args:
        file (UploadFile): The working permit document file to be processed.

    Returns:
        dict: Structured data extracted from the working permit document.
    """
    extrator = ExtractionProcess(WorkPerminExtractor, file, headers)
    result = await extrator.proccess_extraction()
    return result


@app.get("/UploadExcelReulst")
async def UploadExcelReulst():
    SERVICE_ACCOUNT_FILE = "./config-google-service.json"
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    # Authenticate using the service account
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    # Build the Google Drive API client
    drive_service = build("drive", "v3", credentials=credentials)

    # Upload metadata (file name and parent folder)
    file_metadata = {
        "name": "uploaded-file.xlsx",  # Name it will have in Google Drive
        # Upload to the specified folder
        "parents": ["12GT9G9l1lJNrm75FexQw8ACptO8c8bDK"],
    }

    EXCEL_FILE = "./DTR Russel Gutierrez.xlsx"

    media = MediaFileUpload(
        EXCEL_FILE, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    uploaded_file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id, webViewLink").execute()

    return {"status": "success", "file_link": uploaded_file.get("webViewLink")}


@app.get("/extract_airtable")
async def extract_airtable():
    data = AirtableExtractor(files={}, headers=header_airtable).extract()
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="debug")
