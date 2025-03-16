import pytest
from unittest.mock import patch, MagicMock
from src.extractors.diploma_extractor import DiplomaExtractor


# mock_files fixture removed
# mock_headers fixture removed

@pytest.fixture
def mock_api_response():
    """Fixture to provide mock API response data"""
    return {
        "file": "diploma.pdf",
        "data": {
            "fields": {
                "Doc_Type": {"value": "Bachelor's Degree"},
                "Candidate_Name": {"value": "John Doe"},
                "School_Name": {"value": "University of Technology"},
                "Date_Graduated": {"value": "June 15, 2020"}
            }
        }
    }


class TestDiplomaExtractor:

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_success(self, mock_post, mock_files, mock_headers, mock_api_response):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Create instance of DiplomaExtractor
        extractor = DiplomaExtractor(files=mock_files, headers=mock_headers)

        # Mock the ExcelGenerator generate_diploma_excel method
        with patch('src.extractors.diploma_extractor.ExcelGenerator') as mock_excel_gen:
            mock_excel_instance = MagicMock()
            mock_excel_gen.return_value = mock_excel_instance

            mock_excel_data = b"mock excel data"
            mock_excel_instance.generate_diploma_excel.return_value = {
                "excel_data": mock_excel_data}

            # Call extract method
            result = extractor.extract()

            # Verify results
            assert result["excel_data"] == mock_excel_data
            assert result["filename"] == "diploma_diploma.xlsx"
            assert result["content_type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            # Verify Excel generator was called with the correct data
            extracted_data = extractor._extract_diploma_data(mock_api_response)
            mock_excel_instance.generate_diploma_excel.assert_called_once_with(
                extracted_data)

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_api_error(self, mock_post):
        # Setup mock response for API error
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("API Error")
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Create instance of DiplomaExtractor
        extractor = DiplomaExtractor(files={"file": (
            "diploma.pdf", b"test content", "application/pdf")}, headers={"Authorization": "Bearer test_token"})

        # Call extract method
        result = extractor.extract()

        # Verify error handling
        assert "error" in result
        assert "Unexpected error" in result["error"]

    def test_extract_diploma_data(self, mock_api_response):
        # Create instance of DiplomaExtractor
        extractor = DiplomaExtractor(files={}, headers={})

        # Extract diploma data
        result = extractor._extract_diploma_data(mock_api_response)

        # Verify structure and data
        assert "diploma_info" in result

        # Verify specific data points
        assert result["diploma_info"]["Document Type"] == "Bachelor's Degree"
        assert result["diploma_info"]["Candidate Name"] == "John Doe"
        assert result["diploma_info"]["School Name"] == "University of Technology"
        assert result["diploma_info"]["Date graduated"] == "June 15, 2020"

    def test_diploma_info(self, mock_api_response):
        extractor = DiplomaExtractor(files={}, headers={})
        fields = mock_api_response["data"]["fields"]

        result = extractor._doploma_info(fields)

        assert result["Document Type"] == "Bachelor's Degree"
        assert result["Candidate Name"] == "John Doe"
        assert result["School Name"] == "University of Technology"
        assert result["Date graduated"] == "June 15, 2020"
