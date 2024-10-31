from flask import Flask, render_template, request, jsonify
import requests
from groq import Groq

app = Flask(__name__)

API_KEY = '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'  # Reemplaza con tu clave de API
client = Groq(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data['message']

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": message}],
        "temperature": 1,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": True,
        "stop": None
    }

    try:
        completion = client.chat.completions.create(**payload)
        reply = ""
        for chunk in completion:
            reply += chunk.choices[0].delta.content or ""
        print("Respuesta del chatbot:", reply)
    except requests.exceptions.HTTPError as errh:
        print("Error HTTP:", errh)
        reply = 'Error HTTP al conectarse con la API'
    except requests.exceptions.ConnectionError as errc:
        print("Error de conexión:", errc)
        reply = 'Error de conexión al conectarse con la API'
    except requests.exceptions.Timeout as errt:
        print("Error de tiempo de espera:", errt)
        reply = 'Error de tiempo de espera al conectarse con la API'
    except requests.exceptions.RequestException as err:
        print("Error general:", err)
        reply = 'Error al conectarse con la API'

    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(port=3000)
