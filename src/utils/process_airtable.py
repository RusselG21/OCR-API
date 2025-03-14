import logging
from src.utils import ExtractionProcess
logger = logging.getLogger(__name__)


class ProcessAirtable:

    def __init__(self,  constant_column, document_requirements, extractor_map, constant_column_extracted, header, airtableClass, detail):
        """
        Initialize the ProcessAirtable class with required parameters.

        Args:
            constant_column (dict): Dictionary mapping column keys to their values
            document_requirements (dict): Dictionary of document methods and their associated document types
            extractor_map (dict): Dictionary mapping document methods to their extractor classes
            constant_column_extracted (dict): Dictionary mapping document types to their extracted column names
            header (dict): Headers for API requests
            airtableClass (UpdateAirtable): Instance of the UpdateAirtable class for interacting with Airtable
            detail (list): List of records to process from Airtable
        """
        self.header = header
        self.airtableClass = airtableClass
        self.detail = detail
        self.constant_column = constant_column
        self.document_requirements = document_requirements
        self.extractor_map = extractor_map
        self.constant_column_extracted = constant_column_extracted

    async def process_airtable(self):
        """
        Process Airtable records, download attachments, extract data, and update Airtable with Google Drive links.

        This method iterates through records in the detail list, finds attachments that need processing,
        applies the appropriate extractor, saves the results to Google Drive, and updates the Airtable record.

        Returns:
            list: List of dictionaries containing the status and update information for each processed record
        """
        response_list = []
        # object inside []
        for items in self.detail:
            # check inside of field {}
            field = items.get("fields", {})
            # check key and value inside of field {}
            for fieldkey, fieldvalue in field.items():
                # check if key is in CONSTANT_COLUMN dictionary
                for constcolumnkey, constcolumnvalue in self.constant_column.items():
                    # check value inside of CONSTANT_COLUMN dictionary
                    if constcolumnkey == fieldkey:
                        # check if key is equal to fieldkey
                        if fieldvalue == 'No Attachment' and constcolumnvalue in field:
                            # url is inside of field attachemt fielditem.get("url", "")
                            for fielditem in field.get(constcolumnvalue, []):
                                # check if key is in DOCUMENT_REQUIREMENTS dictionary
                                for doc_method, doc_type in self.document_requirements.items():
                                    # check if constcolumnvalue in doc_type sample: "Birth Certificate" in ["Birth Certificate"]
                                    if constcolumnvalue in doc_type:
                                        # check if key is in DOCUMENT_REQUIREMENTS dictionary
                                        extractor_class = self.extractor_map.get(
                                            doc_method)
                                        # if class is existing in EXTRACTOR_MAP
                                        if extractor_class:
                                            # download file from airtable
                                            file_data = await self.airtableClass.download_file(fielditem.get("url", ""))
                                            # process the file
                                            extractor = ExtractionProcess(
                                                extractor_class, file_data, self.header)
                                            # get the result
                                            result_excel = await extractor.proccess_extraction()
                                            # get the file bytes
                                            file_bytes = result_excel.body
                                            # send the file to google drive
                                            google_response = await self.airtableClass.send_to_google_drive(
                                                file_bytes, f"{field.get("Name")}_{fielditem.get('filename', '')}")
                                            file_id = google_response.get(
                                                "file_id")
                                            # update airtable
                                            column_change = self.constant_column_extracted.get(
                                                constcolumnvalue)
                                            # update airtable
                                            air_update = self.airtableClass.update(
                                                file_id, items.get("id"), column_change)
                                            # append the status
                                            response_list.append({
                                                "status": "success",
                                                "name": field.get("Name"),
                                                "airtable_update": air_update
                                            })
        return response_list
