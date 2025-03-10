import csv
from io import StringIO
from typing import Dict, Any, List
import logging
import json

logger = logging.getLogger(__name__)


class CSVGenerator:
    """Utility class to generate CSV files from structured data"""

    def generate_cv_csv(self, cv_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate CSV file from CV data.

        Creates a CSV file containing CV data with sections separated by headers.

        Args:
            cv_data (Dict[str, Any]): Dictionary containing structured CV data

        Returns:
            Dict[str, Any]: Dictionary with CSV data as string or error information
        """
        try:
            # Create CSV file in memory using StringIO
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)

            # Write Personal Information
            writer.writerow(["--- PERSONAL INFORMATION ---"])
            if "personal_info" in cv_data and cv_data["personal_info"]:
                for key, value in cv_data["personal_info"].items():
                    writer.writerow([key, value])
            writer.writerow([])  # Empty row as separator

            # Write Introduction
            writer.writerow(["--- INTRODUCTION ---"])
            writer.writerow([cv_data.get("introduction", "")])
            writer.writerow([])

            # Write Work Experience
            writer.writerow(["--- WORK EXPERIENCE ---"])
            if "work_experience" in cv_data and cv_data["work_experience"]:
                # Write headers
                if cv_data["work_experience"]:
                    headers = cv_data["work_experience"][0].keys()
                    writer.writerow(headers)
                    # Write data rows
                    for job in cv_data["work_experience"]:
                        writer.writerow(job.values())
            writer.writerow([])

            # Write Technical Skills
            writer.writerow(["--- TECHNICAL SKILLS ---"])
            if "technical_skills" in cv_data and cv_data["technical_skills"]:
                for skill in cv_data["technical_skills"]:
                    writer.writerow([skill])
            writer.writerow([])

            # Write Education
            writer.writerow(["--- EDUCATION ---"])
            if "education" in cv_data and cv_data["education"]:
                for edu in cv_data["education"]:
                    writer.writerow([edu])
            writer.writerow([])

            # Write Awards
            writer.writerow(["--- AWARDS ---"])
            if "awards" in cv_data and cv_data["awards"]:
                for award in cv_data["awards"]:
                    writer.writerow([award])

            # Get the CSV data as string
            csv_data = csv_buffer.getvalue()

            logger.info(f"CSV data size: {len(csv_data)} bytes")

            if len(csv_data) > 0:
                return {"csv_data": csv_data}
            else:
                logger.error("CSV data has zero size")
                return {"error": "CSV data has zero size"}

        except Exception as e:
            logger.error(f"Error generating CSV: {str(e)}")
            return {"error": f"Error creating CSV file: {str(e)}"}

    def generate_birth_cert_csv(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate CSV file for birth certificate data.

        Creates a CSV document containing extracted birth certificate information.

        Args:
            data (Dict[str, Any]): Dictionary containing structured birth certificate data

        Returns:
            Dict[str, Any]: Dictionary with CSV data as string or error information
        """
        try:
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)

            # Write Personal Information
            writer.writerow(["--- PERSONAL INFORMATION ---"])
            if "personal_info" in data and data["personal_info"]:
                for key, value in data["personal_info"].items():
                    writer.writerow([key, value])

            csv_data = csv_buffer.getvalue()
            logger.info("CSV data generated for birth certificate")

            return {"csv_data": csv_data}

        except Exception as e:
            logger.error(f"Error generating birth certificate CSV: {str(e)}")
            return {"error": f"Failed to generate CSV: {str(e)}"}

    def generate_id_csv(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate CSV file for ID document data.

        Creates a CSV document containing ID information such as ID type,
        number, name details, date of birth, and address.

        Args:
            data (Dict[str, Any]): Dictionary containing structured ID document data

        Returns:
            Dict[str, Any]: Dictionary with CSV data as string or error information
        """
        try:
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)

            # Write ID Information
            writer.writerow(["--- ID INFORMATION ---"])
            if "id_info" in data and data["id_info"]:
                # Write headers
                writer.writerow(data["id_info"].keys())
                # Write values
                writer.writerow(data["id_info"].values())

            csv_data = csv_buffer.getvalue()
            logger.info("CSV data generated for ID document")

            return {"csv_data": csv_data}

        except Exception as e:
            logger.error(f"Error generating ID document CSV: {str(e)}")
            return {"error": f"Failed to generate CSV: {str(e)}"}

    def generate_diploma_csv(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate CSV file for diploma or educational certificate data.

        Creates a CSV document containing diploma details including 
        candidate name, school name, graduation date, and other relevant information.

        Args:
            data (Dict[str, Any]): Dictionary containing structured diploma data

        Returns:
            Dict[str, Any]: Dictionary with CSV data as string or error information
        """
        try:
            logger.info(
                f"Generating diploma CSV with data: {json.dumps(data, default=str)}")
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)

            # Write Diploma Information
            writer.writerow(["--- DIPLOMA INFORMATION ---"])
            if "diploma_info" in data and data["diploma_info"]:
                for key, value in data["diploma_info"].items():
                    writer.writerow([key, value])

            csv_data = csv_buffer.getvalue()
            logger.info("CSV data generated for diploma")

            return {"csv_data": csv_data}

        except Exception as e:
            logger.error(f"Error generating diploma CSV: {str(e)}")
            return {"error": f"Failed to generate CSV: {str(e)}"}

    def generate_working_permit_csv(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate CSV file for working permit data.

        Creates a CSV document containing working permit details such as
        candidate name, permit validity dates, and other relevant information.

        Args:
            data (Dict[str, Any]): Dictionary containing structured working permit data

        Returns:
            Dict[str, Any]: Dictionary with CSV data as string or error information
        """
        try:
            logger.info(
                f"Generating working permit CSV with data: {json.dumps(data, default=str)}")
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)

            # Write Working Permit Information
            writer.writerow(["--- WORKING PERMIT INFORMATION ---"])
            if "working_permit_info" in data and data["working_permit_info"]:
                for key, value in data["working_permit_info"].items():
                    writer.writerow([key, value])

            csv_data = csv_buffer.getvalue()
            logger.info("CSV data generated for working permit")

            return {"csv_data": csv_data}

        except Exception as e:
            logger.error(f"Error generating working permit CSV: {str(e)}")
            return {"error": f"Failed to generate CSV: {str(e)}"}
