from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4
from .utils import create_completions, guardar_info, consulta_rag, respuesta_general
from .config import init_client
import json

client, collection = init_client()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    conversation_id: str

conversations = []

@app.post("/conversations")
async def create_conversation():
    conversation_id = str(uuid4())
    conversations.append(conversation_id)
    return {"conversation_id": conversation_id}

@app.get("/conversations")
async def get_conversations():
    return {"conversation_ids": conversations}

@app.get("/conversations/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    print("***********")
    print("Recuperando desde conversations contenido en conversacion con id:", conversation_id)
    try:
        result = collection.get(ids=[f"__HISTORIAL__{conversation_id}"])
        print("results:", result)
        if result["documents"] and result["documents"][0]:
            historial = json.loads(result["documents"][0])  # usar json.loads, no eval
            return {"messages": historial}
    except Exception as e:
        print(f"Error al recuperar historial exacto: {e}")
    return {"messages": []}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    print("***********")
    print("Recuperando desde chat endpoint contenido en conversacion con id:", request.conversation_id)

    historial = []
    try:
        result = collection.get(ids=[f"__HISTORIAL__{request.conversation_id}"])
        if result["documents"] and result["documents"][0]:
            historial = json.loads(result["documents"][0])  # usar json.loads, no eval
    except Exception as e:
        print(f"Error al recuperar historial exacto: {e}")

    query = request.query
    output, action = create_completions(client, query, historial)

    if action == "guardar_info":
        guardar_info(output, collection)
        final_response = "Información guardada correctamente."
    elif action == "consulta_rag":
        final_response = consulta_rag(collection, query, client)
    else:
        final_response = respuesta_general(output)

    historial.append((query, final_response))

    historial_string = json.dumps(historial)

    print("***********")
    print("Indexando contenido en conversacion con id:", request.conversation_id)

    collection.upsert(
        documents=[historial_string],
        metadatas=[{"type": "chat_history"}],
        ids=[f"__HISTORIAL__{request.conversation_id}"]
    )
    return {"response": final_response, "conversation_id": request.conversation_id}
