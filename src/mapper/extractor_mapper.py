from ..extractors import CVExtractor, BirthCertExtractor, IDExtractor, DiplomaExtractor, WorkPerminExtractor

"""
This module provides mappings and constants for document extraction and processing.
CONSTANT_COLUMN:
    A dictionary mapping extracted document confirmation keys to their corresponding document upload keys.
CONSTANT_COLUMN_EXTRACTED:
    A dictionary mapping document upload keys to their corresponding extracted document confirmation keys.
DOCUMENT_REQUIREMENTS:
    A dictionary mapping extraction functions to the list of document types they require.
EXTRACTOR_MAP:
    A dictionary mapping extraction functions to their corresponding extractor classes.
The extraction process follows these steps:
1. Check if the key in CONSTANT_COLUMN is "No Attachment". If true, it means the value in CONSTANT_COLUMN_EXTRACTED has no attachment yet.
2. If the key in CONSTANT_COLUMN is available in the JSON response and the key is "No Attachment" and the value is available, it will look in the JSON response (indicating it is not extracted yet but has an attachment from the value column).
3. If the value in CONSTANT_COLUMN is available in DOCUMENT_REQUIREMENTS, it will get its designated key (used to map in EXTRACTOR_MAP to get the base class needed to extract the document).
4. The base class will be used to extract the document and return the extracted data.
5. The extracted data will be saved to Google Drive and then uploaded to Airtable.

                                  +----------------+
                                  | Document Input |
                                  +-------+--------+
                                          |
                                          v
  +------------------+           +-----------------+
  | CONSTANT_COLUMN  |---------->| Check if "No    |
  +------------------+           | Attachment"     |
                                 +--------+--------+
                                          |
                                          v
+--------------------+          +------------------+
| JSON Response Data |--------->| Document needs   |<-------+
+--------------------+          | extraction?      |        |
                                +--------+---------+        |
                                         |                  |
                                         v                  |
  +--------------------+        +------------------+        |
  | DOCUMENT_          |------->| Map to extractor |        |
  | REQUIREMENTS       |        | function         |        |
  +--------------------+        +--------+---------+        |
                                         |                  |
                                         v                  |
  +------------------+          +------------------+        |
  | EXTRACTOR_MAP    |--------->| Select extractor |        |
  +------------------+          | class            |        |
                                +--------+---------+        |
                                         |                  |
                                         v                  |
                               +-------------------+        |
                               | Extract document  |        |
                               | data              |        |
                               +--------+----------+        |
                                        |                   |
                                        v                   |
                               +-------------------+        |
                               | Save to Google    |        |
                               | Drive             |        |
                               +--------+----------+        |
                                        |                   |
                                        v                   |
                               +-------------------+        |
                               | Upload to Airtable|--------+
                               +-------------------+
        
        
 """

CONSTANT_COLUMN = {
    "Extracted TIN Number Upload Confirmation": "TIN Number Upload",
    "Extracted Birth Certificate Confirmation": "Birth Certificate",
    "Extracted Occupational Permit Confirmation": "Occupational Permit",
    "Extracted SSS ID Upload Confirmation": "SSS ID Upload",
    "Extracted UMID Number Upload Confirmation": "UMID Number Upload",
    "Extracted Upload Resume Confirmation": "Upload Resume",
    "Extracted School Records Confirmation": "School Records"
}

CONSTANT_COLUMN_EXTRACTED = {
    "TIN Number Upload": "Extracted TIN Number Upload",
    "Birth Certificate": "Extracted Birth Certificate",
    "Occupational Permit": "Extracted Occupational Permit",
    "SSS ID Upload": "Extracted SSS ID Upload",
    "UMID Number Upload": "Extracted UMID Number Upload",
    "Upload Resume": "Extracted Upload Resume",
    "School Records": "Extracted School Records"
}


DOCUMENT_REQUIREMENTS = {
    "extract_birth_cert": ["Birth Certificate"],
    "extract_cv": ["Upload Resume"],
    "extract_id": ["SSS ID Upload, UMID Number Upload", "TIN Number Upload"],
    "extract_diploma": ["School Records"],
    "extract_working_permit": ["Occupational Permit"]
}

EXTRACTOR_MAP = {
    "extract_birth_cert": BirthCertExtractor,
    "extract_cv": CVExtractor,
    "extract_id": IDExtractor,
    "extract_diploma": DiplomaExtractor,
    "extract_working_permit": WorkPerminExtractor
}
