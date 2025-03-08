from fastapi import HTTPException, Response
import logging

from fastapi.responses import JSONResponse

from src.extractors.base_extractor import APITimeoutError

logger = logging.getLogger(__name__)


class ExtractionProcess:
    """
    Utility class to handle document extraction processes.

    This class provides a reusable workflow for processing different types of documents
    using various extractors. It handles file validation, extraction, and error handling.
    """

    def __init__(self, iclass: object, ifile: any, header: str):
        """
        Initialize the extraction process.

        Args:
            iclass (object): The extractor class to use for processing the document
            ifile (any): The uploaded file object from FastAPI
            header (str): Authentication header for API access
        """
        self.baseclass = iclass
        self.file = ifile
        self.header = header

    async def proccess_extraction(self):
        """
        Process document extraction workflow.

        This method handles the complete extraction process:
        1. Validates the uploaded file
        2. Reads the file content
        3. Passes the file to the appropriate extractor
        4. Handles any errors during extraction
        5. Returns the extraction results or appropriate error responses

        Returns:
            Response: FastAPI Response object containing either Excel data or error information

        Raises:
            HTTPException: For various error conditions during processing
        """
        try:
            # Validate the file
            if not self.file.filename:
                raise HTTPException(status_code=400, detail="No selected file")

            logger.info(f"Received file: {self.file.filename}")

            # Get the file content
            file_content = await self.file.read()
            if not file_content:
                raise HTTPException(status_code=400, detail="Empty file")

            logger.info(f"File size: {len(file_content)} bytes")
            files = {'file': (self.file.filename, file_content)}

            # Process the file using the Birth Certificate extractor
            logger.info(f"Extracting data from file: {self.file.filename}")
            extractor = self.baseclass(files, self.header)
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
