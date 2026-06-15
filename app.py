import os
import streamlit as st
from qdrant_client import QdrantClient
from google import genai

# ==========================================
# WINDOWS FIX
# ==========================================
os.environ["FASTEMBED_CACHE_PATH"] = "./local_model_cache"
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"

# ==========================================
# UI SETUP
# ==========================================
st.set_page_config(page_title="My Private AI", page_icon="💻")
st.title("💻 My Private RAG Assistant")
st.write("Ask questions based entirely on my custom dataset.")

# Enter API key in the UI instead of hardcoding it
api_key = st.text_input("Enter your Gemini API Key to start:", type="password")

# ==========================================
# DATABASE INITIALIZATION
# ==========================================
@st.cache_resource
def setup_database():
    try:
        # Read the external text file
        with open("knowledge_base.txt", "r", encoding="utf-8") as file:
            raw_text = file.read()
            # Split the text by double spaces (paragraphs) to create chunks
            dataset = [chunk.strip() for chunk in raw_text.split("\n\n") if chunk.strip()]
    except FileNotFoundError:
        return None
    
    # Initialize Qdrant and inject data
    db = QdrantClient(":memory:")
    db.add(collection_name="my_dataset", documents=dataset)
    return db

db_client = setup_database()

# ==========================================
# APP LOGIC
# ==========================================
# Check if the text file is missing
if db_client is None:
    st.warning("⚠️ Please create a 'knowledge_base.txt' file in this folder and add your data!")

# Only run the chat if the user has provided an API key
elif api_key:
    ai_client = genai.Client(api_key=api_key)
    
    # Create a chat input box at the bottom of the screen
    user_query = st.chat_input("Ask a question about the data...")
    
    if user_query:
        # 1. Display the user's message on screen
        st.chat_message("user").write(user_query)
        
        # Show a loading spinner while the AI thinks
        with st.spinner("Searching database..."):
            
            # 2. Retrieve Context from Qdrant
            search_results = db_client.query(
                collection_name="my_dataset",
                query_text=user_query,
                limit=1
            )
            retrieved_context = search_results[0].document
            
            # 3. Generate Answer with Gemini
            prompt = f"""
            You are a helpful assistant. Use ONLY the provided context to answer the user's query. 
            If the answer is not contained in the context, say exactly "I don't know".
            
            Context: {retrieved_context}
            
            User Query: {user_query}
            """
            
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
        
        # 4. Display the AI's answer
        st.chat_message("assistant").write(response.text)
        
        # 5. The "Show Your Work" feature!
        with st.expander("🔍 View Retrieved Context"):
            st.info(retrieved_context)