from src.extractors import CVExtractor, BirthCertExtractor, IDExtractor, DiplomaExtractor, WorkPerminExtractor

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
