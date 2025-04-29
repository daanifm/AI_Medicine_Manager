# src/prompt.py
"""
This module contains the `build_prompt` function for a multi-agent medicine manager application.

The prompt instructs the model to:
- Extract structured data (JSON) from user input about patients and medicines.
- Detect queries requesting stored information (RAG queries).
- Answer general questions about medicines.

Functions:
- `build_prompt`: Constructs the prompt for the chat model based on the user's question and prior interaction history.
"""

def build_prompt(question: str, interaction: str):
    """
    Constructs the prompt to send to the chat-based model,
    instructing it to either extract information, detect a RAG query, or answer general questions.

    Parameters:
    question (str): The user's input or query.
    interaction (str): Prior interaction history, if any.

    Returns:
    list: Formatted input for the Gemini API.
    """
    system_message = (
        "Eres un agente especializado en gestionar información de medicinas para pacientes.\n\n"
        "Tienes tres responsabilidades:\n"
        
        "**1. Si el usuario proporciona datos sobre una persona, las medicinas que toma y (opcionalmente) su pastillero semanal (qué medicina toma en qué día y momento), debes devolver **unicamente** de esta forma sin tu añadir **NADA**:\n**"
        
        "{\n"
        "  \"nombre\": \"<nombre de la persona>\",\n"
        "  \"medicinas\": [\"medicina1\", \"medicina2\", ...],\n"
        "  \"pastillero\": {\n"
        "    \"Lunes Mañana\": [\"medicina\"],\n"
        "    \"Martes Tarde\": [\"medicina\"],\n"
        "    ...\n"
        "  }\n"
        "}\n\n"
        "incluye siempre el pastillero aunque este vacío, y si no se proporciona, devuelve un objeto vacío. No incluyas ningún otro texto o comentario.\n\n"

        "**2. Si detectas que el usuario hace una pregunta que busca consultar qué medicinas toma una persona  o se pregunta por en un día y momento concreto, responde SOLO con el texto: Peticion rag\n\n**"
        
        "**3. Si la pregunta no corresponde a guardar información ni a consultar medicinas específicas (por ejemplo, preguntas generales como \"¿Qué es el ibuprofeno?\"), debes contestar normalmente con una explicación clara y concisa.\n\n**"
        "**3.2. En caso de que se t pregunte por alternativas de medicinas que se puedan obtener sin receta, debes responder de forma clara y concisa, pero no debes dar alternativas a medicinas que requieran receta médica y indicar que la informacion puede contener errores y se debe consultar con su medico de cabecera.**\n\n"
        "3.3. Si te hacen preguntas que no están relacionadas con el ámbito médico, recuerda que eres un asistente especializado en la gestión de medicinas y no puedes responder preguntas fuera de ese ámbito."
        "Siempre responde de manera precisa, estructurada y profesional."
    )

    user_message = f"Interacción previa:\n{interaction}\n\nPregunta:\n{question}"

    return [
        {
            "parts": [
                {"text": system_message},
                {"text": user_message}
            ]
        }
    ]
def build_prompt_response(question: str, interaction: str):
    """
    Constructs the prompt to send to the chat-based model,
    instructing it to either extract information, detect a RAG query, or answer general questions.

    Parameters:
    question (str): The user's input or query.
    interaction (str): Prior interaction history, if any.

    Returns:
    list: Formatted input for the Gemini API.
    """
    system_message = (
        "Eres un agente especializado en gestionar información de medicinas para pacientes.\n\n"
        "Te voy a pasar la informacion y la pregunta de un paciente y quiero que responas de la forma mas clara y amable posible.\n"
    )

    user_message = f"Interacción previa:\n{interaction}\n\nPregunta:\n{question}"

    return [
        {
            "parts": [
                {"text": system_message},
                {"text": user_message}
            ]
        }
    ] 