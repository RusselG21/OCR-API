import requests
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ExtractorError(Exception):
    """Base exception for extraction errors"""
    pass


class APITimeoutError(ExtractorError):
    """Exception raised when API request times out"""
    pass


class APIResponseError(ExtractorError):
    """Exception raised when API response is invalid"""
    pass


class BaseExtractor:
    """
    Base class for all extractors

    1 is for POST request
    else is for GET request

    """

    def __init__(self, api_url: str, files: Dict, headers: Dict, operation=1):
        """
        Initialize the BaseExtractor with API connection details.

        Args:
            api_url (str): The URL of the API to connect to
            files (Dict): Dictionary containing file data to be sent
            headers (Dict): HTTP headers to be included in the request
            operation (int, optional): Operation type - 1 for POST, anything else for GET. Defaults to 1.
        """
        self.api_url = api_url
        self.files = files
        self.headers = headers
        self.timeout = 30
        self.operation = operation

    def _get_original_filename(self) -> str:
        """
        Extract original filename from files dictionary.

        Returns:
            str: The original filename if available, otherwise "unknown_file"
        """
        if isinstance(self.files['file'], tuple):
            return self.files['file'][0]
        return "unknown_file"

    def _make_api_request(self) -> Dict[str, Any]:
        """
        Make API request with error handling.

        Sends either a POST or GET request to the configured API endpoint
        based on the operation type specified during initialization.

        Returns:
            Dict[str, Any]: The JSON response from the API

        Raises:
            APITimeoutError: If the API request times out
            APIResponseError: If the API returns a non-200 status code or invalid JSON
            ExtractorError: For other request failures
        """
        response: any
        if self.operation == 1:
            response = requests.post(
                self.api_url,
                files=self.files,
                headers=self.headers,
                timeout=self.timeout
            )
        else:
            response = requests.get(
                self.api_url,
                headers=self.headers,
                timeout=self.timeout
            )
        logger.info(f"API Response: {response.status_code}")
        
        if response.status_code != 200:
            raise APIResponseError(
                f"API returned status code {response.status_code}")
            
        return response.json()


    def _sanitize_filename(self, filename: str) -> str:
        """
        Clean up filename for safe usage.

        Args:
            filename (str): The original filename to sanitize

        Returns:
            str: A sanitized version of the filename with potentially unsafe characters removed
        """
        filename = filename.replace('.pdf', '').replace('.docx', '')
        sanitized = ''.join(c for c in filename if c.isalnum()
                            or c in [' ', '_', '-'])
        return sanitized if sanitized else "extracted_data"