📚 AI Study Assistant (RAG Chatbot)

A chatbot that answers questions from your own documents: PDFs, text notes, and web pages. It uses Retrieval-Augmented Generation (RAG), so every answer is based on retrieved passages and the app shows which sources were used.

Built with LangChain, Groq, ChromaDB, Hugging Face embeddings, and Streamlit.

<!-- Add a screenshot after running the app: ![App screenshot](docs/screenshot.png) -->
Features
Multi-source loading: reads PDFs and .txt files from the documents/ folder, plus web pages listed in app.py.
Grounded answers: the prompt tells the model to answer only from the retrieved context, and to reply "I could not find the answer in the documents." when the context does not contain the answer.
Diverse retrieval: uses MMR (Maximal Marginal Relevance) so the retrieved chunks are relevant but not repetitive.
Source display: an expandable "View Sources" section lists the file or URL behind each answer.
Chat interface: Streamlit chat UI with conversation history for the session.
Persistent vector store: embeddings are saved in chroma_db/, so documents are not re-embedded on every launch.
How it works
PDFs / TXT / Web pages
        │  load
        ▼
Split into chunks (800 characters, 100 overlap)
        │  embed (all-MiniLM-L6-v2)
        ▼
ChromaDB vector store (persisted in chroma_db/)
        │  question → MMR retrieval (top 4 chunks)
        ▼
Prompt = context + question  →  Groq LLM  →  Answer + sources
Tech stack
Component	Choice
Framework	LangChain
LLM	Groq API, model openai/gpt-oss-20b (temperature 0)
Embeddings	Hugging Face all-MiniLM-L6-v2
Vector database	ChromaDB
UI	Streamlit
Language	Python
Settings (in app.py)
Setting	Value
Chunk size / overlap	800 / 100 characters
Retrieval	MMR, k=4, fetch_k=10, lambda_mult=0.5
Web sources	WEBSITES list at the top of app.py
Local documents	documents/ folder (.pdf and .txt)
Getting started

Requirements: Python 3.10 or newer and a free Groq API key.

Clone the repository
bash
   git clone https://github.com/ravibalikai/ai-study-chatbot.git
   cd ai-study-chatbot
Create a virtual environment and install dependencies
bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
Add your API key. Create a file named .env in the project folder:
   GROQ_API_KEY=your_key_here
Add your documents. Create a documents/ folder and put your PDFs and .txt files in it. To use web pages, edit the WEBSITES list in app.py.
Run the app
bash
   streamlit run app.py

The first run builds the vector store, which can take a few minutes. Later runs load it from chroma_db/.

Project structure
ai-study-chatbot/
├── app.py             # Streamlit app: loading, retrieval, prompt, chat UI
├── requirements.txt   # Python dependencies
├── documents/         # Your PDFs and .txt files (create this folder)
├── chroma_db/         # Vector store, created on first run (not committed)
└── .env               # GROQ_API_KEY (not committed)
Limitations
The vector store is built once. If you add or change documents later, delete the chroma_db/ folder and restart the app to re-index them.
Answer quality has not been formally evaluated yet. A test set of questions with expected answers is planned.
Chat history lives in the Streamlit session only. It is not saved between runs, and the retriever does not use earlier turns when searching.
Web sources are set in code, not in the UI.
Planned improvements
Add a small test set of questions with expected answers and report results.
Containerise the app with Docker and deploy it on Azure.
Let users upload documents from the UI and re-index without deleting chroma_db/.
