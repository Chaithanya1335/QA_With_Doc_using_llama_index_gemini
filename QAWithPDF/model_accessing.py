from logger import logging
from exception import customexception
from llama_index.llms.gemini import Gemini
import google.generativeai as genai
from dotenv import load_dotenv
import os
import sys

# Loading Environment Varibles
load_dotenv()


class ModelAccess:
    def __init__(self):
        pass
    def get_model(self):

        gemini_api_key = os.getenv("GOOGLE_API_KEY")

        if gemini_api_key=="":
            print("Please set the Google API Key in the .env file")

        try:
            logging.info("Accessing model")

            # Initialize the Gemini API
            genai.configure(api_key=gemini_api_key)

            logging.info("Gemini api is configured Successfully")

            model = Gemini(api_key=gemini_api_key,model="models/gemini-1.5-pro")

            logging.info("Model accesed successfully")

            return model
        
        except Exception as e:
            raise customexception(e,sys)
    

