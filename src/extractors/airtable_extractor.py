import pandas as pd
from typing import Dict, Any
import logging
from .base_extractor import BaseExtractor

logger = logging.getLogger(__name__)


class AirtableExtractor(BaseExtractor):
    """Extractor specialized for Birth Certificate data"""

    def __init__(self, files: Dict, headers: Dict):
        super().__init__(
            api_url="https://api.airtable.com/v0/appZo3a2wKyMLh3UC/Candidate%20Data?filterByFormula=OR(LEN({Barangay Clearance})>0, LEN({TIN Number Upload})>0, LEN({BIR 2316})>0, LEN({Birth Certificate})>0, LEN({Birth Certificate of Dependents (if applicable)})>0, LEN({COE from previous employer (if available)})>0, LEN({Marriage Contract (if applicable)})>0, LEN({NBI Clearance})>0 , LEN({Occupational Permit})>0, LEN({SSS ID Upload})>0, LEN({UMID Number Upload})>0, LEN({Police Clearance})>0, LEN({Upload Resume})>0, LEN({School Records})>0 )",
            files=files,
            headers={
                "Authorization": f"Bearer {headers}",
                "Content-Type": "application/json",
            },
            operation=2
        )

    def extract(self) -> Dict[str, Any]:
        """Extract AirTable data from API and convert to Excel format"""
        try:
            # Make API request
            data = self._make_api_request()

            return data

        except Exception as e:
            logger.error(f"Error in extract: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"error": f"Unexpected error: {str(e)}"}
