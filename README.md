# 💻 Private RAG Assistant

**Live Demo:** [https://custom-rag-pipeline-mwmvy5sncwei5vaxzozqkh.streamlit.app/]

This project is a custom Retrieval-Augmented Generation (RAG) pipeline built to answer queries based strictly on a private dataset. It utilizes an in-memory vector database and modern embedding models to ensure the AI's responses are highly contextual and free from hallucinations.

## 🚀 Features
* **Custom Knowledge Base:** Ingests and chunks data from a private `.txt` file.
* **Semantic Search:** Uses Qdrant and FastEmbed for lightning-fast, local vector search.
* **Strict AI Restraints:** Prompt engineering forces the Gemini model to answer *only* using the retrieved context, or explicitly state "I don't know."
* **Interactive UI:** Built with Streamlit, featuring a secure API key input and an expandable "Show Your Work" section to view the raw retrieved text.

## 🛠️ Tech Stack
* **Frontend/UI:** Streamlit
* **Vector Database:** Qdrant (In-Memory)
* **Embeddings:** FastEmbed (`bge-small-en`)
* **LLM:** Google Gemini (`gemini-2.5-flash`)

## 💻 Run it Locally
To run this project on your own machine:

1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
