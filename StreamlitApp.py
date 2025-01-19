import streamlit as st
from QAWithPDF.data_ingestion import DataIngestion
from QAWithPDF.model_accessing import ModelAccess
from QAWithPDF.Creagting_Vector_store import VectorStore

# Set page configuration
st.set_page_config(page_title="QA With Custom Documents", page_icon="📄")

st.title("QA With Custom Documents")
st.divider()

# Create a placeholder to store the chat history and query_engine
if "messages" not in st.session_state:
    st.session_state.messages = []
if "query_engine" not in st.session_state:
    st.session_state.query_engine = None

# File uploader
uploaded_files = st.file_uploader(
    label="Upload the document you want to use for QA", accept_multiple_files=True
)

# Handle file upload and create query engine
if st.button("Upload and use the document for QA"):
    if uploaded_files:
        # Getting Data From uploaded files
        try:
            docs = DataIngestion().initiate_data_ingestion(uploaded_files)
            print(docs[1].text)
            st.success(f"Successfully ingested {len(docs)} documents.")
        except Exception as e:
            st.error(f"Error in data ingestion: {e}")
            docs = []

        if docs:
            # Getting LLM Model
            model = ModelAccess().get_model()

            # Getting Vector store as query engine
            try:
                st.session_state.query_engine = VectorStore(model=model, docs=docs).get_vector_store_as_query_engine()
                st.write("Query Engine Initialized:", st.session_state.query_engine)

            except Exception as e:
                st.error(f"Error in creating vector store: {e}")
        else:
            st.warning("No documents were uploaded or there was an issue ingesting them.")
    else:
        st.warning("Please upload documents first.")

# Create a function to handle chat input and show responses
def display_conversation():
    if st.session_state.messages:
        for message in st.session_state.messages:
            st.chat_message(message["role"]).markdown(message["content"], unsafe_allow_html=True)

# Taking Query From user
query = st.chat_input("Enter Your Question Related to the Document")

if query:
    if query.strip():  # Ensure the query is not just empty spaces
        # Add user's query to the chat history
        st.session_state.messages.append({"role": "user", "content": query})

        # Retrieve the Response only if query_engine is available
        if st.session_state.query_engine:
            try:
                response = st.session_state.query_engine.query(query)
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
        st.warning("Please enter a valid question.")  # In case of an empty query
else:
    # Display the initial state of the conversation if no query is entered yet
    display_conversation()
