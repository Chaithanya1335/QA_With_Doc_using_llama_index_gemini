from data_ingestion import DataIngestion
from model_accessing import ModelAccess
from logger import logging
from exception import customexception
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import StorageContext,load_index_from_storage,VectorStoreIndex
from llama_index.core import ServiceContext,set_global_service_context
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
import os
import sys
from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()

class VectorStore:
    def __init__(self):
        pass
    def get_vector_store_as_query_engine(self):
        
        """
        This function returns a query engine object that can be used to query the vector store.
        """

        try:
            # Loading the Data
            logging.info("Getting Data")
            docs = DataIngestion().initiate_data_ingestion("data")
            logging.info("Data Ingested")

            logging.info("Getting Model")
            model = ModelAccess().get_model()
            logging.info("Model Retrieved")

            # Getting Embedding Model
            logging.info("Getting Embedding Model")
            embedding_model = GeminiEmbedding(model_name="models/embedding-001")

            # Creating service context
            logging.info("Creating Service Context")
            
          
            
           
            Settings.llm = model
            Settings.embed_model = embedding_model
            Settings.chunk_size = 1000
            Settings.chunk_overlap = 20

            logging.info("Service Context Created")

            # Cretaing Vector store
            logging.info("Creating Vector Store")
            vector_store = VectorStoreIndex.from_documents(documents=docs,service_context=Settings)
            logging.info("Vector Store Created")

            # Storing data as locally
            logging.info("Storing Data Locally")
            vector_store.storage_context.persist()
            logging.info("Data Stored Locally")

            query_engine = vector_store.as_query_engine()

            return query_engine

            
        except Exception as e:
            raise customexception(e,sys)


if __name__ == "__main__":
    vector_store = VectorStore()
    query_engine = vector_store.get_vector_store_as_query_engine()