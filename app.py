from fastapi import FastAPI, File, UploadFile
import urllib
from src.extractors import CVExtractor, BirthCertExtractor, IDExtractor, DiplomaExtractor, WorkPerminExtractor, AirtableExtractor
import logging
import sys
from src.utils import ExtractionProcess, UpdateAirtable, ProcessAirtable
from src.mapper import EXTRACTOR_MAP, DOCUMENT_REQUIREMENTS, CONSTANT_COLUMN, CONSTANT_COLUMN_EXTRACTED, extract_url
import threading
import time
import asyncio
from contextlib import asynccontextmanager

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

# Create a lifespan context manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code (runs when the app starts)
    thread = threading.Thread(target=run_airtable_update_task, daemon=True)
    thread.start()
    logger.info("Background Airtable update service started")

    yield  # This line separates startup from shutdown code

    # Shutdown code would go here if needed
    logger.info("Shutting down background tasks")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Finhero API key
HEADERS = {"Ocp-Apim-Subscription-Key": "1afe622ee4aa47439faa619583316758"}
# Airtable API key
AIRTABLE_API_KEY = "patsgONcHhgZccHRk.dccf8082dbdb03e1a5182e32f57ea29c82f543c8dfb3246c32e8c90d0bf4c54f"
# Airtable base ID
AIRTABLE_BASE_ID = "appZo3a2wKyMLh3UC"
# Airtable table name
AIRTABLE_TABLE_NAME = "Candidate Data copy"
# Google Drive folder ID
PARENT_FOLDER_ID = "152BmT2NwrO9PQegVf5BZHI0D23hZ7OBD"

# Run Time
RUN_TIME = 60


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


@app.get("/update_airtable")
async def update_airtable():
    """
    Endpoint to update Airtable records and process attachments.

    This endpoint fetches data from Airtable, processes attachments based on   specific document requirements,
    downloads files, processes them, uploads the processed files to Google Drive, and updates Airtable with the new information.

    Returns:
        list: A list of statuses indicating the result of each Airtable update  operation.

    Raises:
        Exception: If any error occurs during the processing of files or updating   Airtable.

    Dependencies:
        - AirtableExtractor: Class to extract data from Airtable.
        - UpdateAirtable: Class to handle Airtable updates and file downloads.
        - EXTRACTOR_MAP: Dictionary mapping document methods to their respective    extractor classes.
        - DOCUMENT_REQUIREMENTS: Dictionary defining document requirements.
        - CONSTANT_COLUMN: Dictionary mapping Airtable fields to their respective   constants.
        - CONSTANT_COLUMN_EXTRACTED: Dictionary mapping extracted constants to  their respective Airtable fields.
        - AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME,  PARENT_FOLDER_ID: Airtable and Google Drive configuration constants.
    """
    table_name_encoded = urllib.parse.quote(AIRTABLE_TABLE_NAME)

    url = extract_url()

    data = AirtableExtractor(
        files={}, headers=AIRTABLE_API_KEY, table_name=table_name_encoded, dynamic_url=url).extract()

    detail = data.get("records", [])

    airtableClass = UpdateAirtable(
        AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, PARENT_FOLDER_ID)

    process_airtable = ProcessAirtable(CONSTANT_COLUMN, DOCUMENT_REQUIREMENTS,
                                       EXTRACTOR_MAP, CONSTANT_COLUMN_EXTRACTED, HEADERS, airtableClass, detail)

    response = await process_airtable.process_airtable()

    if response:
        return response

    return {"status": "No records processed"}


# Background task to run update_airtable every 60 seconds
def run_airtable_update_task():
    async def task_wrapper():
        while True:
            try:
                logger.info("Running scheduled Airtable update")
                await update_airtable()
                logger.info("Scheduled Airtable update completed")
            except Exception as e:
                logger.error(f"Error in scheduled Airtable update: {e}")
            await asyncio.sleep(RUN_TIME)  # Run every 60 seconds

    # Create event loop for the background thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task_wrapper())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="debug")
