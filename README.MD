## End To End Question Answaring web App

## ABOUT : 
This is web application where user can upload files (txt,pdf,doc) and ask question to the AI model. AI model will answer the question based on the uploaded file.

## Features:
-> User can upload files (txt,pdf,doc).

-> user can ask question to the AI model via text.

-> user can ask question to the AI model via voice.

-> user can access New chat

-> user can access chat history

-> user can delete chat history

## Technologies Used:
-> Frontend: Streamlit

-> Model : gemini-1.5-flash

-> Embedding : models/embedding-001

-> Frame work : llama_index

-> Vector Database : vector database from llama_index


# how to run ?

**Steps :**
1. clone the repository using following command
    
            git clone https://github.com/Chaithanya1335/QA_With_Doc_using_llama_index_gemini

2. install the required packages using following command

            pip install -r requirements.txt

3. run application using following command

            streamlit run app.py