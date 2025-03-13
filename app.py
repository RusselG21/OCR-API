from io import BytesIO
from fastapi import FastAPI, File, UploadFile
from src.extractors import CVExtractor, BirthCertExtractor, IDExtractor, DiplomaExtractor, WorkPerminExtractor, AirtableExtractor
import logging
import sys
from src.utils import ExtractionProcess, UpdateAirtable
from mapper import CONSTANT_COLUMN, CONSTANT_COLUMN_EXTRACTED, DOCUMENT_REQUIREMENTS, EXTRACTOR_MAP
import requests

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

HEADERS = {"Ocp-Apim-Subscription-Key": "1afe622ee4aa47439faa619583316758"}
HEADER_AIRTABLE = "patsgONcHhgZccHRk.dccf8082dbdb03e1a5182e32f57ea29c82f543c8dfb3246c32e8c90d0bf4c54f"
AIRTABLE_API_KEY = "patsgONcHhgZccHRk.dccf8082dbdb03e1a5182e32f57ea29c82f543c8dfb3246c32e8c90d0bf4c54f"
AIRTABLE_BASE_ID = "appZo3a2wKyMLh3UC"
AIRTABLE_FIELD_NAME = "Extracted Barangay Clearance"
AIRTABLE_TABLE_NAME = "Candidate Data"
RECORD_ID = "rec4aPr0R1qS8v5HH"
PARENT_FOLDER_ID = "12GT9G9l1lJNrm75FexQw8ACptO8c8bDK"


@app.post("/extract_cv")
async def extract(file: UploadFile = File(...)):
    """
    Extract information from a CV/resume document.

    Args:
        file (UploadFile): The CV document file to be processed.

    Returns:
        dict: Extracted information from the CV in a structured format.
    """
    extrator = ExtractionProcess(CVExtractor, file, HEADERS)
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
    extrator = ExtractionProcess(BirthCertExtractor, file, HEADERS)
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
    extrator = ExtractionProcess(IDExtractor, file, HEADERS)
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
    extrator = ExtractionProcess(DiplomaExtractor, file, HEADERS)
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
    extrator = ExtractionProcess(WorkPerminExtractor, file, HEADERS)
    result = await extrator.proccess_extraction()
    return result


@app.get("/update_airtable_V2")
async def update_airtable():
    data = AirtableExtractor(files={}, headers=HEADER_AIRTABLE).extract()
    detail = data.get("records", [])
    ilist = []  # empty list to hold the file
    airtableClass = UpdateAirtable(
        AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, PARENT_FOLDER_ID)
    # object inside []
    for items in detail:
        # check inside of field {}
        field = items.get("fields", {})
        # check key and value inside of field {}
        for fieldkey, fieldvalue in field.items():
            # check if key is in CONSTANT_COLUMN dictionary
            for constcolumnkey, constcolumnvalue in CONSTANT_COLUMN.items():
                # check value inside of CONSTANT_COLUMN dictionary
                if constcolumnkey == fieldkey:
                    # check if key is equal to fieldkey
                    logger.error(f"fieldkey: {fieldkey}")
                    if fieldvalue == 'No Attachment' and constcolumnvalue in field:
                        # url is inside of field attachemt fielditem.get("url", "")
                        for fielditem in field.get(constcolumnvalue, []):
                            # check if key is in DOCUMENT_REQUIREMENTS dictionary
                            for doc_method, doc_type in DOCUMENT_REQUIREMENTS.items():
                                # check if constcolumnvalue in doc_type sample: "Birth Certificate" in ["Birth Certificate"]
                                if constcolumnvalue in doc_type:
                                    # check if key is in DOCUMENT_REQUIREMENTS dictionary
                                    extractor_class = EXTRACTOR_MAP.get(
                                        doc_method)
                                    # if class is existing in EXTRACTOR_MAP
                                    if extractor_class:
                                        # download file from airtable
                                        file_data = await airtableClass.download_file(fielditem.get("url", ""))
                                        # process the file
                                        extractor = ExtractionProcess(
                                            extractor_class, file_data, HEADERS)
                                        # get the result
                                        result_excel = await extractor.proccess_extraction()
                                        # get the file bytes
                                        file_bytes = result_excel.body
                                        # send the file to google drive
                                        google_response = await airtableClass.send_to_google_drive(
                                            file_bytes, f"{field.get("Name")}_{fielditem.get('filename', '')}")
                                        file_id = google_response.get(
                                            "file_id")
                                        # update airtable
                                        column_change = CONSTANT_COLUMN_EXTRACTED.get(
                                            constcolumnvalue)
                                        # update airtable
                                        air_update = airtableClass.update(
                                            file_id, items.get("id"), column_change)
                                        # append the status
                                        ilist.append(air_update.get("status"))

    return ilist


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="debug")
