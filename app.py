from flask import Flask, render_template, request, jsonify
import requests
from groq import Groq

app = Flask(__name__)

API_KEY = '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'
client = Groq(api_key=API_KEY)

# Variable global para guardar el historial de la conversación
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    global conversation_history
    data = request.get_json()
    user_message = data['message']

    # Añadir mensaje del usuario al historial
    conversation_history.append({"role": "user", "content": user_message})

    # Crear el payload incluyendo el historial de la conversación
    payload = {
        "model": "llama3-8b-8192",
        "messages": conversation_history,  # Aquí se incluye el historial completo
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": True,
        "stop": None
    }

    try:
        completion = client.chat.completions.create(**payload)
        bot_reply = ""
        for chunk in completion:
            bot_reply += chunk.choices[0].delta.content or ""

        # Añadir respuesta del bot al historial
        conversation_history.append({"role": "assistant", "content": bot_reply})

        print("Respuesta del chatbot:", bot_reply)
    except requests.exceptions.HTTPError as errh:
        print("Error HTTP:", errh)
        bot_reply = 'Error HTTP al conectarse con la API'
    except requests.exceptions.ConnectionError as errc:
        print("Error de conexión:", errc)
        bot_reply = 'Error de conexión al conectarse con la API'
    except requests.exceptions.Timeout as errt:
        print("Error de tiempo de espera:", errt)
        bot_reply = 'Error de tiempo de espera al conectarse con la API'
    except requests.exceptions.RequestException as err:
        print("Error general:", err)
        bot_reply = 'Error al conectarse con la API'

    return jsonify({"reply": bot_reply})

@app.route('/')  # Página inicial para cargar primero "loading.html"
def loading_page():
    return render_template('loading.html')

@app.route('/main')  # Página principal
def main_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=3000)