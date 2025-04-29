# src/app.py
"""
This module defines the chatbot interface using Gradio, handles user interactions,
and manages the conversation history.

Functions:
    chatbot_interface(query, history, client, collection): Handles user input, fetches the response from the chatbot, and updates the conversation history.
    launch_gradio_interface(client, collection): Sets up and launches the Gradio interface for the chatbot, defining the UI components and connecting them to the chatbot logic.

Dependencies:
    - gradio
    - utils (create_completions, guardar_info, consulta_rag, respuesta_general)
    - config (init_client)
    - interface (get_html)
    - functools (partial)
"""

import gradio as gr
from utils import create_completions, guardar_info, consulta_rag, respuesta_general
from config import init_client
from interface import get_html
from functools import partial

# Define the interaction history as an empty list
interaccion = []  # Global interaction history

def chatbot_interface(query, history, client, collection):
    """
    Handles user input, gets the response from the chatbot, and updates the conversation history.

    Args:
        query (str): The user's query input.
        history (list): The current conversation history.
        client: GeminiClient instance used to generate content.
        collection: ChromaDB collection instance.

    Returns:
        tuple: (history, history) - The updated conversation history for display and state.
    """
    global interaccion  # Use the global interaction history
    # Get the response and action from the chatbot
    output, action = create_completions(client, query, interaccion)

    if action == "guardar_info":
        print("output", output)
        guardar_info(output, collection)
        final_response = "Información guardada correctamente."
    elif action == "consulta_rag":
        final_response = consulta_rag(collection, query, client)
    else:
        final_response = respuesta_general(output)

    history.append((query, final_response))
    interaccion.append((query, final_response))
    return history, history

def launch_gradio_interface(client, collection):
    """
    Sets up and launches the Gradio interface for the chatbot.
    Loads the external CSS, creates the necessary components, and links the button and text input to the chatbot logic.

    Args:
        client: GeminiClient instance used to generate content.
        collection: ChromaDB collection instance.

    Returns:
        None
    """
    chatbot_css = get_html()
    # Load the external CSS and define the interface
    with gr.Blocks(title="My Custom Chatbot") as demo:
        # Title of the application
        gr.HTML(chatbot_css)
        gr.Markdown("# 🤖 AI Medicine Manager", elem_id="header")
        # Chatbot interface area
        chatbot = gr.Chatbot(elem_id="chatbot")
        # Row with the input box and the button
        with gr.Row(elem_id="input_row"):
            query_input = gr.Textbox(
                placeholder="Type your message here...",
                show_label=False,
                elem_id="query_input"
            )
            submit_button = gr.Button("Send", elem_id="submit_button")
        # Connect the button to the chatbot interface logic
        chatbot_interface_with_client = partial(chatbot_interface, client=client, collection=collection)

        submit_button.click(
            chatbot_interface_with_client,
            inputs=[query_input, chatbot],
            outputs=[chatbot, chatbot]
        )
        # Allow pressing 'Enter' as a submit action
        query_input.submit(
            chatbot_interface_with_client,
            inputs=[query_input, chatbot],
            outputs=[chatbot, chatbot]
        )

    # Launch the interface
    demo.launch()
