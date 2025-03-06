import requests
import pandas as pd
from io import BytesIO
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


class Extract:
    url = "https://api.finhero.asia/finxtract/cv/extractCV"

    def __init__(self, files, headers):
        self.files = files
        self.headers = headers

    def extract_cv(self):
        try:
            # Add timeout to avoid long waiting times (30 seconds)
            response = requests.post(
                self.url, files=self.files, headers=self.headers, timeout=30)
            data = response.json()

            logger.info(f"API Response: {response.status_code}")

            # Extract filename from response or use a default
            if isinstance(self.files['file'], tuple):
                original_filename = self.files['file'][0]
            else:
                original_filename = "unknown_file"

            filename = data.get("file", original_filename).replace(
                '.pdf', '').replace('.docx', '')
            filename = ''.join(
                c for c in filename if c.isalnum() or c in [' ', '_', '-'])
            if not filename:
                filename = "cv_data"  # Fallback filename
            logger.info(f"Processing file: {filename}")

            # Extract all relevant data from the response
            fields = data.get("data", {}).get("fields", {})
            extracted_data = data.get("data", {}).get("extractedData", {})

            # Get candidate information
            candidate_name = fields.get("CandidateName", {}).get("value", "")
            contact_no = fields.get("CandidateContactNo", {}).get("value", "")
            email = fields.get("CandidateEmail", {}).get("value", "")
            address = fields.get("CandidateAddress", {}).get("value", "")
            introduction = fields.get("Introduction", {}).get("value", "")

            # Process WorkingExperienceDetails
            work_exp = extracted_data.get("WorkingExperienceDetails", [])
            logger.info(f"Work experience data: {work_exp}")
            work_exp_df = pd.DataFrame(work_exp) if work_exp else pd.DataFrame(
                columns=["Company", "Position", "StartDate", "EndDate"])

            # Extract technical skills
            tech_skills = []
            skill_entries = fields.get("TechnicalSkill", {}).get("values", [])
            for skill in skill_entries:
                tech_skills.append(skill.get("Skill", {}).get("value", ""))
            tech_skills_df = pd.DataFrame(
                {"Skills": tech_skills}) if tech_skills else pd.DataFrame({"Skills": []})

            # Extract education
            education_data = []
            education_entries = fields.get("Education", {}).get("values", [])
            for edu in education_entries:
                education_data.append(edu.get("Course", {}).get("value", ""))
            education_df = pd.DataFrame(
                {"Education": education_data}) if education_data else pd.DataFrame({"Education": []})

            # Extract awards/certifications
            awards_data = []
            award_entries = fields.get("Awards", {}).get("values", [])
            for award in award_entries:
                awards_data.append(award.get("Award", {}).get("value", ""))
            awards_df = pd.DataFrame(
                {"Awards": awards_data}) if awards_data else pd.DataFrame({"Awards": []})

            # Create Excel file in memory using BytesIO
            excel_buffer = BytesIO()
            try:
                # Use a different Excel engine - try xlsxwriter which is more reliable
                with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                    # Personal Information Sheet
                    personal_info = {
                        "Name": [candidate_name],
                        "Contact": [contact_no],
                        "Email": [email],
                        "Address": [address]
                    }

                    # Introduction might be too long for a single cell, put it in its own sheet
                    intro_df = pd.DataFrame({"Introduction": [introduction]})

                    personal_info_df = pd.DataFrame(personal_info)
                    personal_info_df.to_excel(
                        writer, sheet_name='Personal Info', index=False)
                    intro_df.to_excel(
                        writer, sheet_name='Introduction', index=False)

                    # Work Experience Sheet
                    work_exp_df.to_excel(
                        writer, sheet_name='Work Experience', index=False)

                    # Technical Skills Sheet
                    tech_skills_df.to_excel(
                        writer, sheet_name='Technical Skills', index=False)

                    # Education Sheet
                    education_df.to_excel(
                        writer, sheet_name='Education', index=False)

                    # Awards Sheet
                    awards_df.to_excel(
                        writer, sheet_name='Awards', index=False)

                    # Format each worksheet for better readability
                    for sheet_name in writer.sheets:
                        worksheet = writer.sheets[sheet_name]
                        # Set column widths - using simple index approach instead of get_columns
                        for i in range(10):  # Set width for first 10 columns
                            # default width of 30
                            worksheet.set_column(i, i, 30)

                    logger.info(
                        "Excel data written to buffer using xlsxwriter")
            except Exception as e:
                logger.error(f"Error writing to Excel buffer: {str(e)}")
                return {"error": f"Error creating Excel file: {str(e)}"}

            # Get the Excel data as bytes
            excel_buffer.seek(0)
            excel_data = excel_buffer.getvalue()

            logger.info(f"Excel data size: {len(excel_data)} bytes")

            if len(excel_data) > 0:
                # Set the correct content type for Excel files
                filename = f"{filename}_cv_data.xlsx"
                logger.info(f"Returning Excel with filename: {filename}")
                return {
                    "excel_data": excel_data,
                    "filename": filename,
                    "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                }
            else:
                logger.error("Excel data has zero size")
                return {"error": "Excel data has zero size"}

        except requests.exceptions.Timeout:
            logger.error("API request timed out after 30 seconds")
            return {"error": "API request timed out"}
        except Exception as e:
            logger.error(f"Error in extract_cv: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Unexpected error: {str(e)}"}
