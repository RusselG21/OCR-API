import pytest
from unittest.mock import patch, MagicMock
from src.extractors.cv_extractor import CVExtractor


@pytest.fixture
def mock_api_response():
    """Fixture to provide mock API response data"""
    return {
        "file": "resume.pdf",
        "data": {
            "fields": {
                "CandidateName": {"value": "John Doe"},
                "CandidateContactNo": {"value": "123-456-7890"},
                "CandidateEmail": {"value": "john.doe@example.com"},
                "CandidateAddress": {"value": "123 Main St, City"},
                "Introduction": {"value": "Experienced software developer"},
                "TechnicalSkill": {
                    "values": [
                        {"Skill": {"value": "Python"}},
                        {"Skill": {"value": "JavaScript"}}
                    ]
                },
                "Education": {
                    "values": [
                        {"Course": {"value": "Computer Science Degree"}}
                    ]
                },
                "Awards": {
                    "values": [
                        {"Award": {"value": "Best Developer 2023"}}
                    ]
                }
            },
            "extractedData": {
                "WorkingExperienceDetails": [
                    {
                        "Company": "Tech Corp",
                        "Position": "Senior Developer",
                        "Duration": "2020-2023",
                        "Responsibilities": "Developing software solutions"
                    }
                ]
            }
        }
    }


class TestCVExtractor:

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_success(self, mock_post, mock_files, mock_headers, mock_api_response):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Create instance of CVExtractor
        extractor = CVExtractor(files=mock_files, headers=mock_headers)

        # Mock the ExcelGenerator generate_cv_excel method
        with patch('src.extractors.cv_extractor.ExcelGenerator') as mock_excel_gen:
            mock_excel_instance = MagicMock()
            mock_excel_gen.return_value = mock_excel_instance

            mock_excel_data = b"mock excel data"
            mock_excel_instance.generate_cv_excel.return_value = {
                "excel_data": mock_excel_data}

            # Call extract method
            result = extractor.extract()

            # Verify results
            assert result["excel_data"] == mock_excel_data
            assert result["filename"] == "resume_cv_data.xlsx"
            assert result["content_type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            # Verify the API was called correctly
            mock_post.assert_called_once_with

            # Verify Excel generator was called with the correct data
            extracted_data = extractor._extract_cv_data(mock_api_response)
            mock_excel_instance.generate_cv_excel.assert_called_once_with(
                extracted_data)

    @patch('src.extractors.base_extractor.requests.post')
    def test_extract_api_error(self, mock_post, mock_files, mock_headers):
        # Setup mock response for API error
        mock_response = MagicMock()
        mock_response.json.side_effect = Exception("API Error")
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        # Create instance of CVExtractor
        extractor = CVExtractor(files=mock_files, headers=mock_headers)

        # Call extract method
        result = extractor.extract()

        # Verify error handling
        assert "error" in result
        assert "Unexpected error" in result["error"]

    def test_extract_cv_data(self, mock_api_response):
        # Create instance of CVExtractor
        extractor = CVExtractor(files={}, headers={})

        # Extract CV data
        result = extractor._extract_cv_data(mock_api_response)

        # Verify structure and data
        assert "personal_info" in result
        assert "introduction" in result
        assert "work_experience" in result
        assert "technical_skills" in result
        assert "education" in result
        assert "awards" in result

        # Verify specific data points
        assert result["personal_info"]["Name"] == "John Doe"
        assert result["technical_skills"] == ["Python", "JavaScript"]
        assert len(result["work_experience"]) == 1
        assert result["work_experience"][0]["Company"] == "Tech Corp"

    def test_extract_personal_info(self, mock_api_response):
        extractor = CVExtractor(files={}, headers={})
        fields = mock_api_response["data"]["fields"]

        result = extractor._extract_personal_info(fields)

        assert result["Name"] == "John Doe"
        assert result["Contact"] == "123-456-7890"
        assert result["Email"] == "john.doe@example.com"
        assert result["Address"] == "123 Main St, City"

    # Additional test cases for other extraction methods can be added similarly
