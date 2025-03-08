import pandas as pd
from io import BytesIO
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ExcelGenerator:
    """Utility class to generate Excel files from structured data"""

    def generate_cv_excel(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Excel file from CV data"""
        try:
            # Create Excel file in memory using BytesIO
            excel_buffer = BytesIO()

            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                # Personal Information Sheet
                personal_info_df = pd.DataFrame(
                    cv_data["personal_info"], index=[0])
                personal_info_df.to_excel(
                    writer, sheet_name='Personal Info', index=False)

                # Introduction Sheet
                intro_df = pd.DataFrame(
                    {"Introduction": [cv_data["introduction"]]})
                intro_df.to_excel(
                    writer, sheet_name='Introduction', index=False)

                # Work Experience Sheet
                work_exp_df = pd.DataFrame(cv_data["work_experience"]) if cv_data["work_experience"] else pd.DataFrame(
                    columns=["Company", "Position", "StartDate", "EndDate"])
                work_exp_df.to_excel(
                    writer, sheet_name='Work Experience', index=False)

                # Technical Skills Sheet
                tech_skills_df = pd.DataFrame(
                    {"Skills": cv_data["technical_skills"]}) if cv_data["technical_skills"] else pd.DataFrame({"Skills": []})
                tech_skills_df.to_excel(
                    writer, sheet_name='Technical Skills', index=False)

                # Education Sheet
                education_df = pd.DataFrame(
                    {"Education": cv_data["education"]}) if cv_data["education"] else pd.DataFrame({"Education": []})
                education_df.to_excel(
                    writer, sheet_name='Education', index=False)

                # Awards Sheet
                awards_df = pd.DataFrame(
                    {"Awards": cv_data["awards"]}) if cv_data["awards"] else pd.DataFrame({"Awards": []})
                awards_df.to_excel(writer, sheet_name='Awards', index=False)

                # Format worksheets for better readability
                self._format_worksheets(writer)

                logger.info("Excel data written to buffer using xlsxwriter")

            # Get the Excel data as bytes
            excel_buffer.seek(0)
            excel_data = excel_buffer.getvalue()

            logger.info(f"Excel data size: {len(excel_data)} bytes")

            if len(excel_data) > 0:
                return {"excel_data": excel_data}
            else:
                logger.error("Excel data has zero size")
                return {"error": "Excel data has zero size"}

        except Exception as e:
            logger.error(f"Error generating Excel: {str(e)}")
            return {"error": f"Error creating Excel file: {str(e)}"}

    def generate_birth_cert_excel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Excel file for birth certificate data"""
        try:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:

                # Candiate Name Info Sheet
                candidate_name_info_df = pd.DataFrame([data["personal_info"]])
                candidate_name_info_df.to_excel(
                    writer, sheet_name="Personal Info", index=False)

                # Birth Info Sheet
                birth_info_df = pd.DataFrame([data["birth_info"]])
                birth_info_df.to_excel(
                    writer, sheet_name="Birth Info", index=False)

                # Format worksheets for better readability
                self._format_worksheets(writer)

                logger.info("Excel data written to buffer using xlsxwriter")

            excel_data = excel_buffer.getvalue()
            return {"excel_data": excel_data}

        except Exception as e:
            logger.error(f"Error generating birth certificate Excel: {str(e)}")
            return {"error": f"Failed to generate Excel: {str(e)}"}

    def generate_id_excel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Excel file for birth certificate data"""
        try:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:

                # ID Info Sheet
                _info_df = pd.DataFrame(data["id_info"]) if data["id_info"] else pd.DataFrame(
                    columns=["ID Type", "ID Number", "Candidate Name", "Candidate LastName", "Candidate Middlename", "Date of birth", "Candidate Address"])
                _info_df.to_excel(
                    writer, sheet_name="Personal Info", index=False)

                # Format worksheets for better readability
                self._format_worksheets(writer)

                logger.info("Excel data written to buffer using xlsxwriter")

            excel_data = excel_buffer.getvalue()
            return {"excel_data": excel_data}

        except Exception as e:
            logger.error(f"Error generating birth certificate Excel: {str(e)}")
            return {"error": f"Failed to generate Excel: {str(e)}"}

    def _format_worksheets(self, writer) -> None:
        """Format Excel worksheets for better readability"""
        # Wrap text in all cells
        cell_format = writer.book.add_format({'text_wrap': True})

        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            # Set column widths
            for i in range(10):  # Set width for first 10 columns
                # default width of 50
                worksheet.set_column(i, i, 50, cell_format)
