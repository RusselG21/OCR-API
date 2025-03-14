import pandas as pd
from typing import Dict, Any, List, Optional
import logging
from .base_extractor import BaseExtractor
from ..utils.excel_generator import ExcelGenerator

logger = logging.getLogger(__name__)


class DiplomaExtractor(BaseExtractor):
    """Extractor specialized for Diploma data"""

    def __init__(self, files: Dict, headers: Dict):
        """
        Initialize the DiplomaExtractor with files and headers.

        Args:
            files (Dict): Dictionary containing file data
            headers (Dict): Dictionary containing request headers
        """
        super().__init__(
            api_url="https://api.finhero.asia/finxtract/ph-school-record/extract-diploma",
            files=files,
            headers=headers
        )

    def extract(self) -> Dict[str, Any]:
        """
        Extract Diploma data from API and convert to Excel format.

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
            extracted_data = self._extract_diploma_data(data)

            # Generate Excel file
            excel_generator = ExcelGenerator()
            excel_result = excel_generator.generate_diploma_excel(
                extracted_data)

            if excel_result.get("error"):
                return {"error": excel_result["error"]}

            return {
                "excel_data": excel_result["excel_data"],
                "filename": f"{filename}_diploma.xlsx",
                "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }

        except Exception as e:
            logger.error(f"Error in extract: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Unexpected error: {str(e)}"}

    def _extract_diploma_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and structure all Diploma data from API response.

        Args:
            data (Dict[str, Any]): Raw API response data

        Returns:
            Dict[str, Any]: Structured diploma information
        """
        fields = data.get("data", {}).get("fields", {})

        return {
            "diploma_info": self._doploma_info(fields),
        }

    def _doploma_info(self, fields: Dict[str, Any]) -> Dict[str, str]:
        """
        Extract document information from diploma.

        Args:
            fields (Dict[str, Any]): Fields from the API response

        Returns:
            Dict[str, str]: Extracted diploma information
        """
        doc_field = fields.get("Doc_Type", {})
        candidate_name_field = fields.get("Candidate_Name", {})
        school_name_field = fields.get("School_Name", {})
        date_graduated_field = fields.get("Date_Graduated", {})
        return {
            "Document Type": doc_field.get("value", ""),
            "Candidate Name": candidate_name_field.get("value", ""),
            "School Name": school_name_field.get("value", ""),
            "Date graduated": date_graduated_field.get("value", ""),
        }
