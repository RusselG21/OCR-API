import pandas as pd
from typing import Dict, Any, List, Optional
import logging
from .base_extractor import BaseExtractor
from ..utils.excel_generator import ExcelGenerator

logger = logging.getLogger(__name__)


class IDExtractor(BaseExtractor):
    """Extractor specialized for ID data"""

    def __init__(self, files: Dict, headers: Dict):
        super().__init__(
            api_url="https://api.finhero.asia/finxtract/ph-id/extract-phid",
            files=files,
            headers=headers
        )

    def extract(self) -> Dict[str, Any]:
        """Extract ID data from API and convert to Excel format"""
        try:
            # Make API request
            data = self._make_api_request()

            # Process filename
            original_filename = self._get_original_filename()
            filename = data.get("file", original_filename)
            filename = self._sanitize_filename(filename)
            logger.info(f"Processing file: {filename}")

            # Extract data from API response
            extracted_data = self._extract_id_data(data)

            # Generate Excel file
            excel_generator = ExcelGenerator()
            excel_result = excel_generator.generate_id_excel(
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

    def _extract_id_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract and structure all ID data from API response"""
        id_info = data.get("data", {}).get("fields", {}).get(
            "IDs_info", {}).get("values", [])
        logger.warning(f"ID Info {id_info}")
        return {
            "id_info": self._extract_personal_info(id_info),
        }

    def _extract_personal_info(self, values: List[Dict[str, Any]]) -> List[Dict[str, any]]:
        """Extract personal information from birth certificate"""
        id_records: List[Dict[str, str]] = []

        for value in values:
            if isinstance(value, dict):  # Ensure value is a dictionary
                extracted = {
                    key: sub_value["value"]
                    for key, sub_value in value.items()
                    if isinstance(sub_value, dict) and "value" in sub_value
                }
                if extracted:  # Only append if something was extracted
                    id_records.append(extracted)
        logger.warning(f"ID Records {id_records}")
        return id_records
