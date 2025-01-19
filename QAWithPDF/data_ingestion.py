from exception import customexception
from logger import logging
import os
import sys
from llama_index.core import SimpleDirectoryReader



class DataIngestion:
    def __init__(self):
        pass
    def initiate_data_ingestion(self,path:str):
        """
        This function initiates the data ingestion process. It reads the data from the directory specified in the path

        Args: Path(str)

        Returns: Documents
        """

        try:
            logging.info("Data ingestion initiated")
            # Read the data from specific file
            docs = SimpleDirectoryReader(path).load_data()
            
            logging.info("Data Ingestion completed")

            return docs
        
        except Exception as e:
            raise customexception(e,sys)

