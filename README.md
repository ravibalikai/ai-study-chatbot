# 📚 Study Assistant RAG

An AI-powered study assistant that reads your PDFs, text notes, and websites to answer your questions instantly. Built using Retrieval-Augmented Generation (RAG).

## 🚀 Features
- **Multi-Source Loading:** Reads PDFs, TXT files, and live Websites.
- **Smart Retrieval:** Uses MMR (Maximal Marginal Relevance) to fetch diverse context.
- **Source Citations:** Shows exactly which document or website the answer came from.
- **Web Interface:** Built with Streamlit for a clean, interactive chat experience.

## 🛠️ Tech Stack
- **Framework:** LangChain
- **LLM:** Groq (Llama-3)
- **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Database:** ChromaDB
- **UI:** Streamlit

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/study-assistant-rag.git
   cd study-assistant-rag
