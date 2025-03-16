from io import BytesIO
from fastapi import UploadFile, HTTPException
from fastapi.responses import Response, JSONResponse
import logging
import inspect

logger = logging.getLogger(__name__)


class ExtractionProcess:
    def __init__(self, extractor_class, file, headers):
        """
        Initialize the extraction process with either an uploaded file or a downloaded file (bytes).

        Args:
            extractor_class: The class responsible for document extraction.
            file: Either an `UploadFile` (for uploaded files) or `bytes` (for downloaded files).
            headers: Headers required for the extraction request.
        """
        self.extractor_class = extractor_class
        self.headers = headers

        # Log file type for debugging
        logger.info(
            f"File type: {type(file)}, Module: {type(file).__module__}, Name: {type(file).__name__}")

        # Check if file is truly an UploadFile instance
        if hasattr(file, 'file') and hasattr(file, 'filename'):
            logger.info(
                f"File appears to be an UploadFile with filename: {file.filename}")
            self.file = file
            self.filename = file.filename
            self.is_upload_file = True
        # Check for bytes object
        elif isinstance(file, bytes):
            logger.info("File identified as bytes object")
            self.file = BytesIO(file)  # Convert bytes to file-like object
            self.filename = "downloaded_file.xlsx"  # Default filename
            self.is_upload_file = False
        else:
            # Log additional information about the file object
            logger.error(f"Invalid file type: {type(file)}")
            logger.error(
                f"File attributes: {dir(file) if hasattr(file, '__dict__') else 'No attributes'}")
            logger.error(f"File representation: {str(file)[:100]}...")

            raise ValueError(
                f"Invalid file format: expected UploadFile or bytes, got {type(file)}")

    async def proccess_extraction(self):
        """
        Process document extraction workflow.

        This method:
        1. Validates the uploaded/downloaded file.
        2. Reads the file content.
        3. Passes the file to the appropriate extractor.
        4. Handles any errors during extraction.
        5. Returns the extracted results or an appropriate error response.

        Returns:
            FastAPI Response object containing either extracted data or error messages.
        """
        try:
            # ✅ Validate the file
            if not self.filename:
                raise HTTPException(status_code=400, detail="No selected file")

            logger.info(f"Received file: {self.filename}")

            # ✅ Read file content based on type
            if self.is_upload_file:
                file_content = await self.file.read()  # Read from UploadFile
            else:
                file_content = self.file.getvalue()  # Read from BytesIO

            if not file_content:
                raise HTTPException(status_code=400, detail="Empty file")

            logger.info(f"File size: {len(file_content)} bytes")
            files = {'file': (self.filename, file_content)}

            # ✅ Process the file using the appropriate extractor
            logger.info(f"Extracting data from file: {self.filename}")
            extractor = self.extractor_class(files, self.headers)
            result = extractor.extract()

            # ✅ Handle extraction errors
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

            # ✅ Return extracted Excel data
            if "excel_data" in result:
                logger.info("Using in-memory Excel data")
                filename = result.get("filename", "extracted_birth_cert.xlsx")
                content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                logger.info(
                    f"Returning excel data with content type: {content_type}")
                logger.info(
                    f"Excel data length: {len(result['excel_data'])} bytes")
                logger.info(f"Excel filename: {filename}")

                return Response(
                    content=result['excel_data'],
                    media_type=content_type,
                    headers={
                        "Content-Disposition": f"attachment; filename=\"{filename}\"",
                        "Content-Type": content_type
                    }
                )
            else:
                return JSONResponse(content=result)

        except Exception as e:
            logger.error(f"Error in extraction process: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=500, detail=f"An error occurred: {str(e)}")
