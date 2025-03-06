import pandas as pd
from typing import Dict, Any, List, Optional
import logging
from .base_extractor import BaseExtractor
from ..utils.excel_generator import ExcelGenerator

logger = logging.getLogger(__name__)


class CVExtractor(BaseExtractor):
    """Extractor specialized for CV/resume data"""

    def __init__(self, files: Dict, headers: Dict):
        super().__init__(
            api_url="https://api.finhero.asia/finxtract/cv/extractCV",
            files=files,
            headers=headers
        )

    def extract(self) -> Dict[str, Any]:
        """Extract CV data from API and convert to Excel format"""
        try:
            # Make API request
            data = self._make_api_request()

            # Process filename
            original_filename = self._get_original_filename()
            filename = data.get("file", original_filename)
            filename = self._sanitize_filename(filename)
            logger.info(f"Processing file: {filename}")

            # Extract data from API response
            extracted_data = self._extract_cv_data(data)

            # Generate Excel file
            excel_generator = ExcelGenerator()
            excel_result = excel_generator.generate_cv_excel(extracted_data)

            if excel_result.get("error"):
                return {"error": excel_result["error"]}

            return {
                "excel_data": excel_result["excel_data"],
                "filename": f"{filename}_cv_data.xlsx",
                "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            }

        except Exception as e:
            logger.error(f"Error in extract: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Unexpected error: {str(e)}"}

    def _extract_cv_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and structure all CV data from API response"""
        fields = data.get("data", {}).get("fields", {})
        extracted_data = data.get("data", {}).get("extractedData", {})

        return {
            "personal_info": self._extract_personal_info(fields),
            "introduction": self._extract_introduction(fields),
            "work_experience": self._extract_work_experience(extracted_data),
            "technical_skills": self._extract_technical_skills(fields),
            "education": self._extract_education(fields),
            "awards": self._extract_awards(fields)
        }

    def _extract_personal_info(self, fields: Dict[str, Any]) -> Dict[str, str]:
        """Extract candidate's personal information"""
        return {
            "Name": fields.get("CandidateName", {}).get("value", ""),
            "Contact": fields.get("CandidateContactNo", {}).get("value", ""),
            "Email": fields.get("CandidateEmail", {}).get("value", ""),
            "Address": fields.get("CandidateAddress", {}).get("value", "")
        }

    def _extract_introduction(self, fields: Dict[str, Any]) -> str:
        """Extract candidate's introduction/summary"""
        return fields.get("Introduction", {}).get("value", "")

    def _extract_work_experience(self, extracted_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract work experience details"""
        work_exp = extracted_data.get("WorkingExperienceDetails", [])
        logger.info(f"Work experience data: {work_exp}")
        return work_exp

    def _extract_technical_skills(self, fields: Dict[str, Any]) -> List[str]:
        """Extract technical skills"""
        tech_skills = []
        skill_entries = fields.get("TechnicalSkill", {}).get("values", [])
        for skill in skill_entries:
            tech_skills.append(skill.get("Skill", {}).get("value", ""))
        return tech_skills

    def _extract_education(self, fields: Dict[str, Any]) -> List[str]:
        """Extract education details"""
        education_data = []
        education_entries = fields.get("Education", {}).get("values", [])
        for edu in education_entries:
            education_data.append(edu.get("Course", {}).get("value", ""))
        return education_data

    def _extract_awards(self, fields: Dict[str, Any]) -> List[str]:
        """Extract awards and certifications"""
        awards_data = []
        award_entries = fields.get("Awards", {}).get("values", [])
        for award in award_entries:
            awards_data.append(award.get("Award", {}).get("value", ""))
        return awards_data
