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
    """Base class for all extractors"""

    def __init__(self, api_url: str, files: Dict, headers: Dict, operation=1):
        self.api_url = api_url
        self.files = files
        self.headers = headers
        self.timeout = 30  # API timeout in seconds
        self.operation = operation

    def _get_original_filename(self) -> str:
        """Extract original filename from files dictionary"""
        if isinstance(self.files['file'], tuple):
            return self.files['file'][0]
        return "unknown_file"

    def _make_api_request(self) -> Dict[str, Any]:
        """Make API request with error handling"""
        try:
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

        except requests.exceptions.Timeout:
            logger.error(
                f"API request to {self.api_url} timed out after {self.timeout} seconds")
            raise APITimeoutError("API request timed out")

        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            raise ExtractorError(f"API request failed: {str(e)}")

        except ValueError as e:
            logger.error(f"Invalid JSON in API response: {str(e)}")
            raise APIResponseError("Invalid API response format")

    def _sanitize_filename(self, filename: str) -> str:
        """Clean up filename for safe usage"""
        filename = filename.replace('.pdf', '').replace('.docx', '')
        sanitized = ''.join(c for c in filename if c.isalnum()
                            or c in [' ', '_', '-'])
        return sanitized if sanitized else "extracted_data"

    def extract(self) -> Dict[str, Any]:
        """Main extraction method to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement extract method")
