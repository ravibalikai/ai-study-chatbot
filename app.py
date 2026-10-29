import os
import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# --- 1. CONFIGURATION ---
WEBSITES = ["https://en.wikipedia.org/wiki/Artificial_intelligence"]

# --- 2. CACHE THE DATABASE ---
# This stops Streamlit from reloading everything every time you click a button
@st.cache_resource
def get_retriever():
    docs = []
    if os.path.exists("./documents"):
        pdf_loader = DirectoryLoader('./documents', glob="**/*.pdf", loader_cls=PyPDFLoader)
        txt_loader = DirectoryLoader('./documents', glob="**/*.txt", loader_cls=TextLoader)
        docs.extend(pdf_loader.load())
        docs.extend(txt_loader.load())
        
    if WEBSITES:
        web_loader = WebBaseLoader(WEBSITES)
        docs.extend(web_loader.load())

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists("chroma_db") and os.listdir("chroma_db"):
        vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)
    else:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_model, persist_directory="chroma_db")

    return vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5})

retriever = get_retriever()
llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Study Assistant. Use ONLY the provided context to answer. If not found, say 'I could not find the answer in the documents.'"),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}")
])

# --- 3. STREAMLIT UI ---
st.title("📚 Study Assistant")
st.caption("Ask questions based on your PDFs, Notes, and Websites.")

# Keep chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if query := st.chat_input("Ask a question about your documents..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            docs = retriever.invoke(query)
            context = "\n\n".join([doc.page_content for doc in docs])
            sources = set([doc.metadata.get('source', 'Unknown') for doc in docs])
            
            final_prompt = prompt.invoke({"context": context, "question": query})
            response = llm.invoke(final_prompt)
            
            # Display answer
            st.markdown(response.content)
            
            # Display sources
            with st.expander("📚 View Sources"):
                for source in sources:
                    st.write(f"- {source}")

    # Save assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": response.content})