from exception import customexception
from logger import logging
import os
import sys
from llama_index.core import SimpleDirectoryReader



class DataIngestion:
    def __init__(self):
        pass

    def initiate_data_ingestion(self, uploaded_files):
        """
        This function initiates the data ingestion process. It reads the data from the files uploaded by the user in Streamlit.

        Args:
        - uploaded_files (list): List of Streamlit file objects.

        Returns:
        - docs (list): List of documents loaded from the uploaded files.
        """
        try:
            logging.info("Data ingestion initiated")

            # Create a temporary directory to store the uploaded files
            temp_dir = "temp_uploaded_files"
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Save the uploaded files to the temporary directory
            for uploaded_file in uploaded_files:
                with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())

            # Use SimpleDirectoryReader to read the files from the temp directory
            docs = SimpleDirectoryReader(input_dir = temp_dir ).load_data()

            logging.info("Data ingestion completed")

            # Optionally clean up the temporary files
            for uploaded_file in uploaded_files:
                os.remove(os.path.join(temp_dir, uploaded_file.name))

            return docs

        except Exception as e:
            raise customexception(e, sys)

