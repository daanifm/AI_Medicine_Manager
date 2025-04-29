
# src/config.py
"""
    Client to interact with the Google Gemini API using HTTP requests.
"""
import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions


def init_client():
    """
    Initializes the ChromaDB client, creates or retrieves the collection,
    and returns both the GeminiClient and the collection.

    Returns:
        tuple: (GeminiClient instance, ChromaDB collection)
    """
    # Initialize ChromaDB client
    chroma_client = chromadb.Client()
    # Create or get the collection
    collection = chroma_client.get_or_create_collection(name="medicina_manager")
    api_key = "Your gemini api key"
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-2.0-flash')
    return model,collection
