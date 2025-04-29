import requests
import json

# Reemplazar esta línea:
# client = build("gemini", "v1", credentials=credentials)

# Nueva implementación para usar el modelo de Gemini
def call_gemini_model(api_key, prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt_text
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Ejemplo de uso
api_key = "AIzaSyAv7fekn85pn48vzYYLjqIx0bpL90CsTZU"
prompt_text = "Write a story about a magic backpack."
response = call_gemini_model(api_key, prompt_text)
print(response)