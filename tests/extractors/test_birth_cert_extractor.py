import pytest
from unittest.mock import patch, MagicMock
from src.extractors.birth_cert_extractor import BirthCertExtractor


@pytest.fixture
def mock_api_response():
    """Fixture to provide mock API response data"""
    return {
        "file": "birth_certificate.pdf",
        "data": {
            "fields": {
                "Candidate_Name": {"value": "John Doe"},
                "Date_Of_Birth": {"value": "January 15, 1990"}
            }
        }
    }


class TestBirthCertExtractor:

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_success(self, mock_post, mock_files, mock_headers, mock_api_response):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Create instance of BirthCertExtractor
        extractor = BirthCertExtractor(files=mock_files, headers=mock_headers)

        # Mock the ExcelGenerator generate_birth_cert_excel method
        with patch('src.extractors.birth_cert_extractor.ExcelGenerator') as mock_excel_gen:
            mock_excel_instance = MagicMock()
            mock_excel_gen.return_value = mock_excel_instance

            mock_excel_data = b"mock excel data"
            mock_excel_instance.generate_birth_cert_excel.return_value = {
                "excel_data": mock_excel_data}

            # Call extract method
            result = extractor.extract()

            # Verify results
            assert result["excel_data"] == mock_excel_data
            assert result["filename"] == "birth_certificate_birth_cert_data.xlsx"
            assert result["content_type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            # Verify Excel generator was called with the correct data
            extracted_data = extractor._extract_birth_cert_data(
                mock_api_response)
            mock_excel_instance.generate_birth_cert_excel.assert_called_once_with(
                extracted_data)

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_api_error(self, mock_post, mock_files, mock_headers):
        # Setup mock response for API error
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("API Error")
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Create instance of BirthCertExtractor
        extractor = BirthCertExtractor(files=mock_files, headers=mock_headers)

        # Call extract method
        result = extractor.extract()

        # Verify error handling
        assert "error" in result
        assert "Unexpected error" in result["error"]

    def test_extract_birth_cert_data(self, mock_api_response):
        # Create instance of BirthCertExtractor
        extractor = BirthCertExtractor(files={}, headers={})

        # Extract birth certificate data
        result = extractor._extract_birth_cert_data(mock_api_response)

        # Verify structure and data
        assert "personal_info" in result

        # Verify specific data points
        assert result["personal_info"]["Name"] == "John Doe"
        assert result["personal_info"]["Date Of Birth"] == "January 15, 1990"

    def test_extract_personal_info(self, mock_api_response):
        extractor = BirthCertExtractor(files={}, headers={})
        fields = mock_api_response["data"]["fields"]

        result = extractor._extract_personal_info(fields)

        assert result["Name"] == "John Doe"
        assert result["Date Of Birth"] == "January 15, 1990"
