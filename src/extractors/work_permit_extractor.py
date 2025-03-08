import pandas as pd
from typing import Dict, Any, List, Optional
import logging
from .base_extractor import BaseExtractor
from ..utils.excel_generator import ExcelGenerator

logger = logging.getLogger(__name__)


class WorkPerminExtractor(BaseExtractor):
    """Extractor specialized for Work Permit data"""

    def __init__(self, files: Dict, headers: Dict):
        super().__init__(
            api_url="https://api.finhero.asia/finxtract/ph-work-permit/extract-work-permit",
            files=files,
            headers=headers
        )

    def extract(self) -> Dict[str, Any]:
        """Extract Work Permit data from API and convert to Excel format"""
        try:
            # Make API request
            data = self._make_api_request()

            # Process filename
            original_filename = self._get_original_filename()
            filename = data.get("file", original_filename)
            filename = self._sanitize_filename(filename)
            logger.info(f"Processing file: {filename}")

            # Extract data from API response
            extracted_data = self._extract_work_permit_data(data)

            # Generate Excel file
            excel_generator = ExcelGenerator()
            excel_result = excel_generator.generate_working_permit_excel(
                extracted_data)

            if excel_result.get("error"):
                return {"error": excel_result["error"]}

            return {
                "excel_data": excel_result["excel_data"],
                "filename": f"{filename}_work_permit.xlsx",
                "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }

        except Exception as e:
            logger.error(f"Error in extract: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Unexpected error: {str(e)}"}

    def _extract_work_permit_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and structure all Diploma data from API response"""
        fields = data.get("data", {}).get("fields", {})

        return {
            "working_permit_info": self._work_permit_info(fields),
        }

    def _work_permit_info(self, fields: Dict[str, Any]) -> Dict[str, str]:
        """Extract document type information from diploma"""
        candidate_name_field = fields.get("Candidate_Name", {})
        validity_field = fields.get("Validity", {})
        return {
            "Candidate Name": candidate_name_field.get("value", ""),
            "Validity": validity_field.get("value", ""),
        }
