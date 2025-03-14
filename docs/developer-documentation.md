# OCR-API Technical Documentation

## System Overview

OCR-API is a document processing system that extracts structured data from various document types using optical character recognition (OCR) and processes this data for storage and analysis. The system integrates with Airtable for data management and Google Drive for file storage.

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   FastAPI   │──────▶   Extract   │──────▶    Store   │
│  Endpoints  │      │ & Process   │      │   Results   │
└─────────────┘      └─────────────┘      └─────────────┘
       ▲                    │                    │
       │                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │      │   OCR API   │      │  Airtable   │
│  Requests   │      │  (Finhero)  │      │ Google Drive│
└─────────────┘      └─────────────┘      └─────────────┘
```

The system consists of the following components:

- **FastAPI Application**: Provides RESTful endpoints for document processing
- **Extraction Services**: Document-specific extractors that process different document types
- **Data Mapping**: Maps extracted data to standardized formats
- **External Integrations**: Airtable for data storage and Google Drive for file storage

## API Endpoints

### Document Extraction Endpoints

| Endpoint                  | HTTP Method | Description                                     | Input       | Output                                     |
| ------------------------- | ----------- | ----------------------------------------------- | ----------- | ------------------------------------------ |
| `/extract_cv`             | POST        | Extract data from CV/resume                     | File upload | JSON with extracted CV data                |
| `/extract_birth_cert`     | POST        | Extract data from birth certificates            | File upload | JSON with extracted birth certificate data |
| `/extract_id`             | POST        | Extract data from ID documents                  | File upload | JSON with extracted ID data                |
| `/extract_diploma`        | POST        | Extract data from diplomas                      | File upload | JSON with extracted diploma data           |
| `/extract_working_permit` | POST        | Extract data from working permits               | File upload | JSON with extracted working permit data    |
| `/update_airtable`        | GET         | Process and update Airtable with extracted data | None        | JSON status report                         |

## Core Components

### Extractors

The system uses specialized extractors for each document type, all located in the `src/extractors` directory:

- `CVExtractor`: Extracts information from resumes and CVs
- `BirthCertExtractor`: Extracts information from birth certificates
- `IDExtractor`: Extracts information from various ID documents
- `DiplomaExtractor`: Extracts information from educational certificates
- `WorkPerminExtractor`: Extracts information from work permits
- `AirtableExtractor`: Fetches data from Airtable

### Utility Classes

- `ExtractionProcess`: Handles the document extraction workflow
- `UpdateAirtable`: Updates Airtable with extracted information
- `ProcessAirtable`: Orchestrates the entire process of extracting from documents and updating Airtable

### Mapping System

The mapping system in `src/mapper/extractor_mapper.py` provides the following key mappings:

- `CONSTANT_COLUMN`: Maps extracted document confirmation keys to document upload keys
- `CONSTANT_COLUMN_EXTRACTED`: Maps document upload keys to extracted document confirmation keys
- `DOCUMENT_REQUIREMENTS`: Maps extraction functions to required document types
- `EXTRACTOR_MAP`: Maps extraction functions to extractor classes

## Setup and Installation

### Prerequisites

- Python 3.8+
- Finhero API key
- Airtable account and API key
- Google Drive API credentials

### Installation

1. Clone the repository

```bash
git clone [repository-url]
cd OCR-API
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Configure environment variables
   - Finhero API key
   - Airtable API key
   - Google Drive credentials

### Running the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The application will be available at http://localhost:8000

## Integration Details

### Finhero OCR Integration

The system uses Finhero's OCR API for document processing. API calls use the subscription key defined in the `HEADERS` constant.

### Airtable Integration

The system connects to Airtable using:

- `AIRTABLE_API_KEY`: Authentication token
- `AIRTABLE_BASE_ID`: Target base identifier
- `AIRTABLE_TABLE_NAME`: Target table name

### Google Drive Integration

Files are stored in Google Drive using:

- `PARENT_FOLDER_ID`: Folder to store processed documents

## Document Processing Workflow

1. Document file is uploaded to an extraction endpoint
2. The appropriate extractor processes the document through the Finhero OCR API
3. The extracted data is structured according to document type
4. For Airtable updates:
   - Files are downloaded from Airtable
   - Documents are processed with the appropriate extractors
   - Results are uploaded to Google Drive
   - Airtable records are updated with the extracted information

## Troubleshooting

### Common Issues

1. **OCR Extraction Failed**:

   - Check file format (supported formats: PDF, JPG, PNG)
   - Verify Finhero API key is valid
   - Check document quality

2. **Airtable Update Failed**:

   - Verify Airtable API key is valid
   - Check permissions for the base and table

3. **Google Drive Upload Failed**:
   - Verify Google Drive credentials are valid
   - Check folder permissions

### Logging

The application uses Python's logging module with:

- Log file output: `app.log`
- Console output
- Log level: INFO

## Development Guidelines

### Adding a New Document Extractor

1. Create a new extractor class in `src/extractors`
2. Extend the appropriate base class
3. Implement the extraction logic
4. Update the `EXTRACTOR_MAP` and `DOCUMENT_REQUIREMENTS` in `src/mapper/extractor_mapper.py`
5. Create a new endpoint in `app.py`

### Testing

Run tests using:

```bash
pytest tests/
```

## Security Considerations

- API keys are currently stored in plain text in the code. In production, consider:
  - Using environment variables
  - Implementing a secret management system
  - Rotating keys regularly

## Future Improvements

- Move configuration to environment variables
- Implement caching for better performance
- Add authentication for API endpoints
- Develop a user interface for monitoring document processing
