import pandas as pd
from typing import Dict, Any
import logging
from .base_extractor import BaseExtractor
from ..utils.excel_generator import ExcelGenerator

logger = logging.getLogger(__name__)


class BirthCertExtractor(BaseExtractor):
    """Extractor specialized for Birth Certificate data"""

    def __init__(self, files: Dict, headers: Dict):
        """
        Initialize the BirthCertExtractor with files and headers.

        Args:
            files (Dict): Dictionary containing file data
            headers (Dict): Dictionary containing request headers
        """
        super().__init__(
            api_url="https://api.finhero.asia/finxtract/ph-birth-cert/extract-birth-certificate",
            files=files,
            headers=headers
        )

    def extract(self) -> Dict[str, Any]:
        """
        Extract Birth Certificate data from API and convert to Excel format.

        Returns:
            Dict[str, Any]: Dictionary containing Excel data, filename, and content type,
            or error information if extraction fails
        """
        try:
            # Make API request
            data = self._make_api_request()

            # Process filename
            original_filename = self._get_original_filename()
            filename = data.get("file", original_filename)
            filename = self._sanitize_filename(filename)
            logger.info(f"Processing file: {filename}")

            # Extract data from API response
            extracted_data = self._extract_birth_cert_data(data)

            # Generate Excel file
            excel_generator = ExcelGenerator()
            excel_result = excel_generator.generate_birth_cert_excel(
                extracted_data)

            if excel_result.get("error"):
                return {"error": excel_result["error"]}

            return {
                "excel_data": excel_result["excel_data"],
                "filename": f"{filename}_birth_cert_data.xlsx",
                "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }

        except Exception as e:
            logger.error(f"Error in extract: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Unexpected error: {str(e)}"}

    def _extract_birth_cert_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and structure all Birth Certificate data from API response.

        Args:
            data (Dict[str, Any]): Raw API response data

        Returns:
            Dict[str, Any]: Structured birth certificate information
        """
        fields = data.get("data", {}).get("fields", {})

        return {
            "personal_info": self._extract_personal_info(fields),
        }

    def _extract_personal_info(self, fields: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract personal information from birth certificate.

        Args:
            fields (Dict[str, Any]): Fields from the API response

        Returns:
            Dict[str, str]: Personal information including name and date of birth
        """
        name_field = fields.get("Candidate_Name", {})
        dob_field = fields.get("Date_Of_Birth", {})
        return {
            "Name": name_field.get("value", ""),
            "Date Of Birth": dob_field.get("value", ""),
        }
