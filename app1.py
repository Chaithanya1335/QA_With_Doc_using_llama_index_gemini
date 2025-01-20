import streamlit as st
from QAWithPDF.DataIngestion import DataIngestion
from QAWithPDF.model_accessing import ModelAccess
from QAWithPDF.Creagting_Vector_store import VectorStore
import speech_recognition as sr

# Set page configuration
st.set_page_config(page_title="QA With Custom Documents", page_icon="📄", layout="wide")

st.title("📄 QA With Custom Documents")
st.divider()

# Sidebar content: File uploader, button for "Upload and Process", and "New Chat" button
with st.sidebar:
    st.subheader("Upload Your Document(s) for Question Answering")
    st.write("Please upload your PDF, DOCX, or TXT file(s) to get started.")
    
    # File uploader in sidebar
    uploaded_files = st.file_uploader(
        label="Choose files to upload", type=["pdf", "txt", "docx"], accept_multiple_files=True
    )
    
    # Stylish upload button in sidebar
    upload_button = st.button("Upload and Process Documents")
    
    # "New Chat" button in sidebar
    new_chat_button = st.button("Start New Chat")

# Create a placeholder to store the chat history and query_engine
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_engine" not in st.session_state:
    st.session_state.query_engine = None

# Handle the "Start New Chat" button to reset chat, query engine, and force page reload
if new_chat_button:
    st.session_state.messages = []  # Clear chat history
    st.session_state.query_engine = None  # Clear query engine
    st.experimental_rerun()  # Forces a complete page refresh (like opening a new page)

# Handle file upload and document processing
if upload_button:
    if uploaded_files:
        with st.spinner("Ingesting documents..."):
            try:
                docs = DataIngestion().initiate_data_ingestion(uploaded_files)
                if docs:
                    st.success(f"Successfully ingested {len(docs)} document(s).")
                    # Display a preview of the first document's content for debugging
                    st.text_area("Document Preview:", docs[0].text[:500], height=150)  # Show first 500 chars
                else:
                    st.warning("No documents were loaded or there was an issue ingesting them.")
            except Exception as e:
                st.error(f"Error in data ingestion: {e}")
                docs = []

        if docs:
            with st.spinner("Initializing query engine..."):
                # Getting LLM Model
                model = ModelAccess().get_model()

                try:
                    # Getting Vector store as query engine
                    st.session_state.query_engine = VectorStore(model=model, docs=docs).get_vector_store_as_query_engine()
                    st.success("Query Engine Initialized Successfully!")
                except Exception as e:
                    st.error(f"Error in creating vector store: {e}")
        else:
            st.warning("No documents were uploaded or there was an issue ingesting them.")
    else:
        st.warning("Please upload documents first.")

# Main Content
# Section Header for Chat Interaction
st.subheader("Ask Your Question")

# Create a function to handle chat input and show responses
def display_conversation():
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.chat_message(message["role"]).markdown(f"**You:** {message['content']}", unsafe_allow_html=True)
            elif message["role"] == "assistant":
                st.chat_message(message["role"]).markdown(f"**Assistant:** {message['content']}", unsafe_allow_html=True)

# Voice Recognition Setup
def voice_input():
    recognizer = sr.Recognizer()

    # Start listening to the microphone
    with sr.Microphone() as source:
        st.info("Listening... Please speak your question.")
        audio = recognizer.listen(source)

        # Convert speech to text
        try:
            query = recognizer.recognize_google(audio)
            st.success(f"Your question: {query}")
            return query
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            st.error("There was an error with the speech recognition service.")
            return ""

# Add a button to record voice input
voice_query = None
if st.button("Record Your Question (Voice Input)"):
    voice_query = voice_input()

# Taking Query From user (either typed or voice)
query = st.chat_input("Enter Your Question Related to the Document")

# Combine text input and voice input if both are provided
final_query = voice_query if voice_query else query

if final_query and final_query.strip():  # Ensure the query is not just empty spaces
    # Add user's query to the chat history
    st.session_state.messages.append({"role": "user", "content": final_query})

    # Retrieve the Response only if query_engine is available
    if st.session_state.query_engine:
        with st.spinner("Getting response..."):
            try:
                response = st.session_state.query_engine.query(final_query)
                if hasattr(response, 'response') and response.response:
                    # Add the response from the model to the chat history
                    st.session_state.messages.append({"role": "assistant", "content": response.response})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't find an answer."})

                display_conversation()

            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Error in getting response: {e}"})
                display_conversation()
    else:
        st.warning("Query engine is not initialized. Please upload documents first.")
else:
    # Display the initial state of the conversation if no query is entered yet
    display_conversation()
