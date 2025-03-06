from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse, Response
from src.extractors import CVExtractor, BirthCertExtractor, APITimeoutError
import os
import logging
import sys

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
    try:
        # Validate the file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No selected file")

        logger.info(f"Received file: {file.filename}")

        # Get the file content
        file_content = await file.read()
        if not file_content:
            raise HTTPException(status_code=400, detail="Empty file")

        logger.info(f"File size: {len(file_content)} bytes")
        files = {'file': (file.filename, file_content)}

        # Process the file using the CV extractor
        logger.info(f"Extracting data from file: {file.filename}")
        extractor = CVExtractor(files, headers)
        result = extractor.extract()

        # Handle extraction errors
        if not result:
            logger.error("Extraction result is None")
            raise HTTPException(
                status_code=500, detail="Failed to process file")

        if "error" in result:
            error_msg = result["error"]
            logger.error(f"Error in extraction: {error_msg}")
            if "timed out" in error_msg.lower():
                return JSONResponse(content={"detail": error_msg}, status_code=504)
            return JSONResponse(content={"detail": error_msg}, status_code=500)

        # Return Excel data
        if "excel_data" in result:
            logger.info("Using in-memory Excel data")
            filename = result.get("filename", "extracted_cv.xlsx")
            content_type = result.get(
                "content_type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

            logger.info(
                f"Returning excel data with content type: {content_type}")
            logger.info(
                f"Excel data length: {len(result['excel_data'])} bytes")
            logger.info(f"Excel filename: {filename}")

            # Return with explicit headers to ensure browser handles it correctly
            return Response(
                content=result["excel_data"],
                media_type=content_type,
                headers={
                    "Content-Disposition": f"attachment; filename=\"{filename}\"",
                    "Content-Type": content_type
                }
            )
        else:
            raise HTTPException(
                status_code=500, detail="Excel data not found in result")

    except APITimeoutError as e:
        logger.error(f"API timeout: {str(e)}")
        return JSONResponse(content={"detail": str(e)}, status_code=504)
    except Exception as e:
        logger.error(f"Error in extract endpoint: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/extract_birth_cert")
async def extract_birth_cert(file: UploadFile = File(...)):
    try:
        # Validate the file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No selected file")

        logger.info(f"Received file: {file.filename}")

        # Get the file content
        file_content = await file.read()
        if not file_content:
            raise HTTPException(status_code=400, detail="Empty file")

        logger.info(f"File size: {len(file_content)} bytes")
        files = {'file': (file.filename, file_content)}

        # Process the file using the Birth Certificate extractor
        logger.info(f"Extracting data from file: {file.filename}")
        extractor = BirthCertExtractor(files, headers)
        result = extractor.extract()

        # Handle extraction errors
        if not result:
            logger.error("Extraction result is None")
            raise HTTPException(
                status_code=500, detail="Failed to process file")

        if "error" in result:
            error_msg = result["error"]
            logger.error(f"Error in extraction: {error_msg}")
            if "timed out" in error_msg.lower():
                return JSONResponse(content={"detail": error_msg}, status_code=504)
            return JSONResponse(content={"detail": error_msg}, status_code=500)

        # Return Excel data
        if "excel_data" in result:
            logger.info("Using in-memory Excel data")
            filename = result.get("filename", "extracted_birth_cert.xlsx")
            content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            logger.info(
                f"Returning excel data with content type: {content_type}")
            logger.info(
                f"Excel data length: {len(result['excel_data'])} bytes")
            logger.info(f"Excel filename: {filename}")

            # Return with explicit headers to ensure browser handles it correctly
            return Response(
                content=result["excel_data"],
                media_type=content_type,
                headers={
                    "Content-Disposition": f"attachment; filename=\"{filename}\"",
                    "Content-Type": content_type
                }
            )
        else:
            raise HTTPException(
                status_code=500, detail="Excel data not found in result")

    except APITimeoutError as e:
        logger.error(f"API timeout: {str(e)}")
        return JSONResponse(content={"detail": str(e)}, status_code=504)
    except Exception as e:
        logger.error(f"Error in extract_birth_cert endpoint: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, log_level="debug")
