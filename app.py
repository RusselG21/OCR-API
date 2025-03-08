from fastapi import FastAPI, File, UploadFile
from src.extractors import CVExtractor, BirthCertExtractor, IDExtractor, DiplomaExtractor, WorkPerminExtractor
import os
import logging
import sys
from src.utils import ExtractionProcess

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="debug")
