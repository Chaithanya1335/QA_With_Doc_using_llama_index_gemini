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
    def __init__(self,model,docs):
        self.model = model
        self.docs = docs

        
    def get_vector_store_as_query_engine(self):
        
        """
        This function returns a query engine object that can be used to query the vector store.
        """

        try:
          
            # Getting Embedding Model
            logging.info("Getting Embedding Model")
            embedding_model = GeminiEmbedding(model_name="models/embedding-001")

            # Creating service context
            logging.info("Creating Service Context")
           
            setting = Settings
            setting.llm = self.model
            setting.embed_model = embedding_model
            setting.chunk_size = 1000
            setting.chunk_overlap = 20

            logging.info("Service Context Created")

            # Cretaing Vector store
            logging.info("Creating Vector Store")
            vector_store = VectorStoreIndex.from_documents(documents=self.docs)
            logging.info("Vector Store Created")

            # Storing data as locally
            logging.info("Storing Data Locally")
            vector_store.storage_context.persist()
            logging.info("Data Stored Locally")

            

            query_engine = vector_store.as_query_engine()

            return query_engine

            
        except Exception as e:
            raise customexception(e,sys)


