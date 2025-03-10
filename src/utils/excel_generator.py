import pandas as pd
from io import BytesIO
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class ExcelGenerator:
    """Utility class to generate Excel files from structured data"""

    def generate_cv_excel(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Excel file from CV data.

        Creates a multi-sheet Excel document with separate sheets for:
        - Personal Information
        - Introduction
        - Work Experience
        - Technical Skills
        - Education
        - Awards

        Args:
            cv_data (Dict[str, Any]): Dictionary containing structured CV data

        Returns:
            Dict[str, Any]: Dictionary with Excel data as bytes or error information
        """
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
                self._format_worksheets(writer, awards_df)

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
        """
        Generate Excel file for birth certificate data.

        Creates an Excel document containing extracted birth certificate
        information on a single sheet.

        Args:
            data (Dict[str, Any]): Dictionary containing structured birth certificate data

        Returns:
            Dict[str, Any]: Dictionary with Excel data as bytes or error information
        """
        try:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:

                # Candiate Info Sheet
                candidate_name_info_df = pd.DataFrame([data["personal_info"]])
                candidate_name_info_df.to_excel(
                    writer, sheet_name="Personal Info", index=False)

                # Format worksheets for better readability
                self._format_worksheets(writer, candidate_name_info_df)

                logger.info("Excel data written to buffer using xlsxwriter")

            excel_data = excel_buffer.getvalue()
            return {"excel_data": excel_data}

        except Exception as e:
            logger.error(f"Error generating birth certificate Excel: {str(e)}")
            return {"error": f"Failed to generate Excel: {str(e)}"}

    def generate_id_excel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Excel file for ID document data.

        Creates an Excel document containing ID information such as ID type,
        number, name details, date of birth, and address.

        Args:
            data (Dict[str, Any]): Dictionary containing structured ID document data

        Returns:
            Dict[str, Any]: Dictionary with Excel data as bytes or error information
        """
        try:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:

                # ID Info Sheet
                _info_df = pd.DataFrame(data["id_info"]) if data["id_info"] else pd.DataFrame(
                    columns=["ID Type", "ID Number", "Candidate Name", "Candidate LastName", "Candidate Middlename", "Date of birth", "Candidate Address"])
                _info_df.to_excel(
                    writer, sheet_name="Personal Info", index=False)
                # Format worksheets for better readability
                self._format_worksheets(writer, _info_df)

                logger.info("Excel data written to buffer using xlsxwriter")

            excel_data = excel_buffer.getvalue()
            return {"excel_data": excel_data}

        except Exception as e:
            logger.error(f"Error generating birth certificate Excel: {str(e)}")
            return {"error": f"Failed to generate Excel: {str(e)}"}

    def generate_diploma_excel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Excel file for diploma or educational certificate data.

        Creates an Excel document containing diploma details including
        candidate name, school name, graduation date, and other relevant information.

        Args:
            data (Dict[str, Any]): Dictionary containing structured diploma data

        Returns:
            Dict[str, Any]: Dictionary with Excel data as bytes or error information
        """
        logger.warning(data)
        try:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:

                # ID Info Sheet
                _info_df = pd.DataFrame([data["diploma_info"]]) if data["diploma_info"] else pd.DataFrame(
                    columns=["ID Type", "Candidate Name", "School Name", "Date Graduated", "Candidate Address"])
                _info_df.to_excel(
                    writer, sheet_name="Personal Info", index=False)

                # Format worksheets for better readability
                self._format_worksheets(writer, _info_df)

                logger.info("Excel data written to buffer using xlsxwriter")

            excel_data = excel_buffer.getvalue()
            return {"excel_data": excel_data}

        except Exception as e:
            logger.error(f"Error generating birth certificate Excel: {str(e)}")
            return {"error": f"Failed to generate Excel: {str(e)}"}

    def generate_working_permit_excel(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Excel file for working permit data.

        Creates an Excel document containing working permit details such as
        candidate name, permit validity dates, and other relevant information.

        Args:
            data (Dict[str, Any]): Dictionary containing structured working permit data

        Returns:
            Dict[str, Any]: Dictionary with Excel data as bytes or error information
        """
        logger.warning(data)
        try:
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:

                # ID Info Sheet
                _info_df = pd.DataFrame([data["working_permit_info"]]) if data["working_permit_info"] else pd.DataFrame(
                    columns=["Candidate Name", "Validity"])
                _info_df.to_excel(
                    writer, sheet_name="Personal Info", index=False)
                # Format worksheets for better readability
                self._format_worksheets(writer, _info_df)

                logger.info("Excel data written to buffer using xlsxwriter")

            excel_data = excel_buffer.getvalue()
            return {"excel_data": excel_data}

        except Exception as e:
            logger.error(f"Error generating birth certificate Excel: {str(e)}")
            return {"error": f"Failed to generate Excel: {str(e)}"}

    def _format_worksheets(self, writer, df) -> None:
        """
        Format Excel worksheets for better readability.

        Applies consistent formatting to all worksheets in the Excel document,
        including text wrapping and column width adjustments.

        Args:
            writer: The ExcelWriter object containing the worksheets to format

        Returns:
            None
        """
        # Wrap text in all cells
        cell_format = writer.book.add_format({'text_wrap': True})
        red_format = writer.book.add_format(
            {'bg_color': 'red', 'font_color': 'white'})

        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            # Set column widths
            for i in range(10):  # Set width for first 10 columns
                worksheet.set_column(i, i, 50, cell_format)

            # Apply red background to blank cells
            for row_num in range(1, len(df) + 1):  # Skip header row
                for col_num, cell_value in enumerate(df.iloc[row_num - 1]):
                    # Check for empty cells
                    if cell_value == '' or pd.isna(cell_value):
                        worksheet.write(
                            row_num, col_num, 'Unable to extract text. The document is unclear or blurred.', red_format)
