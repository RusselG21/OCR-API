# 🔍 OCR-API: Document Extraction System

## 🧰 Technology Stack

### 💻 What Powers Our System

- **Python**: A user-friendly programming language that helps our system process information quickly and efficiently - think of it as the brain of our operation.

### 🧩 Main Building Blocks

- **🔤 Text Recognition Technology**: Our system can "read" text from images and documents, similar to how humans read but done by a computer.
- **📑 Specialized Document Processors**: We have different tools designed to handle specific types of documents:
  - 📝 Resume Processor: Understands and extracts information from job applications
  - 👶 Birth Certificate Processor: Pulls important details from birth records
  - 🪪 ID Document Processor: Works with driver's licenses, passports, and other identification
  - 🎓 Academic Certificate Processor: Handles diplomas and educational records
  - 👷‍♂️ Work Permit Processor: Manages employment authorization documents

### 🔄 Connected Systems

- **☁️ Google Drive Connection**: After we process your documents, we store them securely in Google Drive - similar to saving files in a digital filing cabinet.
- **📊 Airtable Connection**: We organize all the extracted information in Airtable - think of this as a smart spreadsheet that keeps everything organized.

## ⚙️ How Document Processing Works

Our document processing pipeline uses a series of technical components to manage, identify, and extract information. Here's how it works:

### 🗺️ Dictionary Mapping Structure

The system relies on four key dictionaries to manage the extraction flow:

1. **CONSTANT_COLUMN**: Maps confirmation keys to upload keys

   ```python
   CONSTANT_COLUMN = {
       "Extracted TIN Number Upload Confirmation": "TIN Number Upload",
       "Extracted Birth Certificate Confirmation": "Birth Certificate",
       "Extracted Occupational Permit Confirmation": "Occupational Permit",
       "Extracted SSS ID Upload Confirmation": "SSS ID Upload",
       "Extracted UMID Number Upload Confirmation": "UMID Number Upload",
       "Extracted Upload Resume Confirmation": "Upload Resume",
       "Extracted School Records Confirmation": "School Records"
   }
   ```

2. **CONSTANT_COLUMN_EXTRACTED**: Maps upload keys to extracted data fields

   ```python
   CONSTANT_COLUMN_EXTRACTED = {
       "TIN Number Upload": "Extracted TIN Number Upload",
       "Birth Certificate": "Extracted Birth Certificate",
       "Occupational Permit": "Extracted Occupational Permit",
       "SSS ID Upload": "Extracted SSS ID Upload",
       "UMID Number Upload": "Extracted UMID Number Upload",
       "Upload Resume": "Extracted Upload Resume",
       "School Records": "Extracted School Records"
   }
   ```

3. **DOCUMENT_REQUIREMENTS**: Associates extraction functions with document types

   ```python
   DOCUMENT_REQUIREMENTS = {
       "extract_birth_cert": ["Birth Certificate"],
       "extract_cv": ["Upload Resume"],
       "extract_id": ["SSS ID Upload", "UMID Number Upload", "TIN Number Upload"],
       "extract_diploma": ["School Records"],
       "extract_working_permit": ["Occupational Permit"]
   }
   ```

4. **EXTRACTOR_MAP**: Links extraction functions to their processor classes
   ```python
   EXTRACTOR_MAP = {
       "extract_birth_cert": BirthCertExtractor,
       "extract_cv": CVExtractor,
       "extract_id": IDExtractor,
       "extract_diploma": DiplomaExtractor,
       "extract_working_permit": WorkPerminExtractor
   }
   ```

### 🔄 Technical Process Flow

When a document enters our system, it undergoes this technical process:

1. **Document Ingestion**: The document is submitted via API endpoint or picked up by the automatic background service.

2. **Attachment Verification**: The system checks if the document has an attachment by examining if the corresponding key in `CONSTANT_COLUMN` contains "No Attachment".

3. **Processing Assessment**: If the document has an attachment and needs processing, the system proceeds to extraction.

4. **Extractor Function Mapping**: The system identifies the document type and maps it to the appropriate extraction function using the `DOCUMENT_REQUIREMENTS` dictionary.

5. **Processor Class Selection**: It retrieves the corresponding processor class via the `EXTRACTOR_MAP` dictionary (e.g., CVExtractor, IDExtractor).

6. **Information Extraction**: The processor class parses the document using OCR technology and structures the data according to predefined schemas.

7. **Cloud Storage**: The processed data is stored in Google Drive with appropriate metadata.

8. **Database Update**: The system updates Airtable using the `CONSTANT_COLUMN_EXTRACTED` dictionary to map fields correctly.

This technical pipeline ensures efficient document processing with appropriate routing based on document types. The system runs both on-demand via API endpoints and automatically through a scheduled background service.

### 📊 Processing Flow Diagram

```
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
```

## 🔄 Background Service

Our system includes a helpful automated assistant that works behind the scenes:

### ⏱️ Automatic Document Processing

- **🤖 Always Working**: Our background service runs continuously, checking for new documents every 60 seconds - like having an assistant who never sleeps!

- **🔍 What It Does**: This service automatically:
  1. Checks Airtable for new document submissions
  2. Downloads any new files it finds
  3. Determines what type of documents they are
  4. Processes them using the appropriate specialist
  5. Uploads the results back to Google Drive
  6. Updates Airtable with the extracted information
- **⚡ Benefits**: This automation means:
  - No manual triggering needed
  - Documents are processed promptly
  - Information flows smoothly into your systems
  - Everything stays up-to-date without human intervention

The background service ensures that your document processing pipeline runs efficiently and continuously, providing a seamless experience for all users of the system. 🚀
