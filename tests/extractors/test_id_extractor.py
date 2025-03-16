import pytest
from unittest.mock import patch, MagicMock
from src.extractors.id_extractor import IDExtractor


@pytest.fixture
def mock_api_response():
    """Fixture to provide mock API response data"""
    return {
        "file": "id_scan.pdf",
        "data": {
            "fields": {
                "IDs_info": {
                    "values": [
                        {
                            "ID_Type": {"value": "Driver's License"},
                            "ID_Number": {"value": "N01-12-345678"},
                            "Name": {"value": "John Doe"},
                            "Expiry_Date": {"value": "2025-06-30"}
                        },
                        {
                            "ID_Type": {"value": "SSS ID"},
                            "ID_Number": {"value": "SSS-1234567890"},
                            "Name": {"value": "John Doe"},
                            "Expiry_Date": {"value": "Valid Until Cancelled"}
                        }
                    ]
                }
            }
        }
    }


class TestIDExtractor:

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_success(self, mock_post, mock_files, mock_headers, mock_api_response):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Create instance of IDExtractor
        extractor = IDExtractor(files=mock_files, headers=mock_headers)

        # Mock the ExcelGenerator generate_id_excel method
        with patch('src.extractors.id_extractor.ExcelGenerator') as mock_excel_gen:
            mock_excel_instance = MagicMock()
            mock_excel_gen.return_value = mock_excel_instance

            mock_excel_data = b"mock excel data"
            mock_excel_instance.generate_id_excel.return_value = {
                "excel_data": mock_excel_data}

            # Call extract method
            result = extractor.extract()

            # Verify results
            assert result["excel_data"] == mock_excel_data
            assert result["filename"] == "id_scan_id.xlsx"
            assert result["content_type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            # Verify Excel generator was called with the correct data
            extracted_data = extractor._extract_id_data(mock_api_response)
            mock_excel_instance.generate_id_excel.assert_called_once_with(
                extracted_data)

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_api_error(self, mock_post):
        # Setup mock response for API error
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("API Error")
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Create instance of IDExtractor
        extractor = IDExtractor(files={"file": (
            "id_scan.pdf", b"test content", "application/pdf")}, headers={"Authorization": "Bearer test_token"})

        # Call extract method
        result = extractor.extract()

        # Verify error handling
        assert "error" in result
        assert "Unexpected error" in result["error"]

    def test_extract_id_data(self, mock_api_response):
        # Create instance of IDExtractor
        extractor = IDExtractor(files={}, headers={})

        # Extract ID data
        result = extractor._extract_id_data(mock_api_response)

        # Verify structure and data
        assert "id_info" in result
        assert len(result["id_info"]) == 2

        # Verify specific data points
        assert result["id_info"][0]["ID_Type"] == "Driver's License"
        assert result["id_info"][0]["ID_Number"] == "N01-12-345678"
        assert result["id_info"][1]["ID_Type"] == "SSS ID"

    def test_extract_personal_info(self, mock_api_response):
        extractor = IDExtractor(files={}, headers={})
        values = mock_api_response["data"]["fields"]["IDs_info"]["values"]

        result = extractor._extract_personal_info(values)

        assert len(result) == 2
        assert result[0]["ID_Type"] == "Driver's License"
        assert result[1]["Name"] == "John Doe"

    def test_extract_personal_info_empty(self):
        extractor = IDExtractor(files={}, headers={})
        values = []

        result = extractor._extract_personal_info(values)

        assert len(result) == 0
