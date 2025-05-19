# src/utils.py
"""
Module to handle the generation of chatbot responses using the Gemini API and ChromaDB.

This module contains functions that interact with the Gemini client to generate 
responses for the chatbot. The `create_completions` function builds a prompt 
using a user’s query and previous interactions, then sends it to the 
Gemini model to obtain a relevant response.

Functions:
    create_completions(client, query, interaction): Generates a completion from 
        the Gemini model based on the user's query and prior interactions.
    create_response(client, query, interaction): Generates a response from the Gemini model.
    guardar_info(data, collection): Saves or updates information in ChromaDB.
    consulta_rag(collection, pregunta, client): Performs a RAG search in ChromaDB.
    respuesta_general(texto): Returns a general response.
"""

from .prompt import build_prompt, build_prompt_response
import json
import chromadb
from chromadb.utils import embedding_functions
from .config import init_client
import re

def create_completions(client, query, interaction):
    """
    Generates a chatbot completion based on the user's query and previous interactions.

    Args:
        client: GeminiClient instance used to generate content.
        query (str): The user's query.
        interaction (str): Previous interaction history.

    Returns:
        tuple: (output (str), action (str)) where output is the model's response and action is the detected action.
    """
    # Build the prompt
    prompt_text = build_prompt(query, interaction)

    # Generate the response
    response = client.generate_content(prompt_text, generation_config={"temperature": 0.7})

    # Extract and return the text
    output = response.text.strip()
    print(output)

    if "nombre" in output and "medicinas" in output:
        print("guardar_info")
        action = "guardar_info"
    elif output.lower() == "peticion rag":
        print("consulta_rag")
        action = "consulta_rag"
    else:
        print("respuesta_general")
        action = "respuesta_general"

    return output, action

def create_response(client, query, interaction):
    """
    Generates a chatbot response based on the user's query and previous interactions.

    Args:
        client: GeminiClient instance used to generate content.
        query (str): The user's query.
        interaction (str): Previous interaction history.

    Returns:
        str: The model's response.
    """
    # Build the prompt
    prompt_text = build_prompt_response(query, interaction)

    # Generate the response
    response = client.generate_content(prompt_text, generation_config={"temperature": 0.7})

    # Extract and return the text
    output = response.text.strip()
    return output

def guardar_info(data: str, collection: chromadb.Collection):
    """
    Saves or updates information in ChromaDB without overwriting previous pillbox data.

    Args:
        data (str): JSON string with name, medicines, and pillbox.
        collection (chromadb.Collection): The ChromaDB collection to update.
    """
    nombre_pattern = r'"nombre":\s*"([^"]+)"'
    medicinas_pattern = r'"medicinas":\s*\[([^\]]+)\]'
    pastillero_pattern = r'"pastillero":\s*(\{.*?\})'

    nombre_match = re.search(nombre_pattern, data)
    if nombre_match:
        nombre = nombre_match.group(1)
    else:
        print("Error: Name not found in data.")
        return

    medicinas_match = re.search(medicinas_pattern, data)
    if medicinas_match:
        medicinas = [m.strip().strip('"') for m in medicinas_match.group(1).split(",")]
    else:
        medicinas = []

    pastillero_match = re.search(pastillero_pattern, data, re.DOTALL)
    nuevo_pastillero = json.loads(pastillero_match.group(1)) if pastillero_match else {}

    # Get existing data if any
    existing_doc = collection.get(ids=[nombre])
    pastillero_final = nuevo_pastillero

    if existing_doc and existing_doc["documents"]:
        print(f"Updating document for {nombre}...")

        # Extract previous pillbox from text
        texto_existente = existing_doc["documents"][0]
        pastillero_existente_match = re.search(r'Pastillero:\s*(\{.*\})', texto_existente, re.DOTALL)
        if pastillero_existente_match:
            pastillero_existente = json.loads(pastillero_existente_match.group(1))

            # Merge without losing data
            for dia, meds in pastillero_existente.items():
                if dia in pastillero_final:
                    pastillero_final[dia] = list(set(pastillero_final[dia] + meds))
                else:
                    pastillero_final[dia] = meds
        else:
            pastillero_final = nuevo_pastillero
    else:
        print(f"Adding new document for {nombre}...")

    texto_a_indexar = f"Nombre: {nombre}, Medicinas: {', '.join(medicinas)}. Pastillero: {json.dumps(pastillero_final)}"

    if existing_doc and existing_doc["documents"]:
        collection.update(
            ids=[nombre],
            documents=[texto_a_indexar],
            metadatas=[{"nombre": nombre}]
        )
    else:
        collection.add(
            documents=[texto_a_indexar],
            metadatas=[{"nombre": nombre}],
            ids=[nombre]
        )

def consulta_rag(collection, pregunta: str, client):
    """
    Performs a RAG search in ChromaDB based on the user's question.

    Args:
        collection (chromadb.Collection): The ChromaDB collection to search.
        pregunta (str): The user's question.
        client: GeminiClient instance used to generate content.

    Returns:
        str: The found result or a not found message.
    """
    # Search by name
    results = collection.query(
        query_texts=[pregunta],
    )
    print("results", results)

    if results["documents"] and results["documents"][0]:
        return create_response(client, pregunta, results)
    else:
        return "No related records found."

def respuesta_general(texto: str):
    """
    Returns the general response.

    Args:
        texto (str): The model's response.

    Returns:
        str: The response text.
    """
    return texto