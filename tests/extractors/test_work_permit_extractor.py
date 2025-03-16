import pytest
from unittest.mock import patch, MagicMock
from src.extractors.work_permit_extractor import WorkPerminExtractor


@pytest.fixture
def mock_api_response():
    """Fixture to provide mock API response data"""
    return {
        "file": "work_permit.pdf",
        "data": {
            "fields": {
                "Candidate_Name": {"value": "John Doe"},
                "Validity": {"value": "2023-06-01 to 2024-06-01"}
            }
        }
    }


class TestWorkPermitExtractor:

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_success(self, mock_post, mock_files, mock_headers, mock_api_response):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Create instance of WorkPerminExtractor
        extractor = WorkPerminExtractor(files=mock_files, headers=mock_headers)

        # Mock the ExcelGenerator generate_working_permit_excel method
        with patch('src.extractors.work_permit_extractor.ExcelGenerator') as mock_excel_gen:
            mock_excel_instance = MagicMock()
            mock_excel_gen.return_value = mock_excel_instance

            mock_excel_data = b"mock excel data"
            mock_excel_instance.generate_working_permit_excel.return_value = {
                "excel_data": mock_excel_data}

            # Call extract method
            result = extractor.extract()

            # Verify results
            assert result["excel_data"] == mock_excel_data
            assert result["filename"] == "work_permit_work_permit.xlsx"
            assert result["content_type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            # Verify Excel generator was called with the correct data
            extracted_data = extractor._extract_work_permit_data(
                mock_api_response)
            mock_excel_instance.generate_working_permit_excel.assert_called_once_with(
                extracted_data)

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_api_error(self, mock_post):
        # Setup mock response for API error
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("API Error")
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Create instance of WorkPerminExtractor
        extractor = WorkPerminExtractor(files={"file": (
            "work_permit.pdf", b"test content", "application/pdf")}, headers={"Authorization": "Bearer test_token"})

        # Call extract method
        result = extractor.extract()

        # Verify error handling
        assert "error" in result
        assert "Unexpected error" in result["error"]

    def test_extract_work_permit_data(self, mock_api_response):
        # Create instance of WorkPerminExtractor
        extractor = WorkPerminExtractor(files={}, headers={})

        # Extract work permit data
        result = extractor._extract_work_permit_data(mock_api_response)

        # Verify structure and data
        assert "working_permit_info" in result

        # Verify specific data points
        assert result["working_permit_info"]["Candidate Name"] == "John Doe"
        assert result["working_permit_info"]["Validity"] == "2023-06-01 to 2024-06-01"

    def test_work_permit_info(self, mock_api_response):
        extractor = WorkPerminExtractor(files={}, headers={})
        fields = mock_api_response["data"]["fields"]

        result = extractor._work_permit_info(fields)

        assert result["Candidate Name"] == "John Doe"
        assert result["Validity"] == "2023-06-01 to 2024-06-01"
