from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import uuid
import requests

# Carrega variáveis de ambiente (se houver alguma)
load_dotenv()

# --- CONFIGURAÇÕES ---
MODELO_OLLAMA = "llama3.2"
URL_OLLAMA = "http://127.0.0.1:11434/api/chat"
# -------------------------------------


# Inicializa o aplicativo Flask
app = Flask(__name__)
app.secret_key = 'alura' 

# Define e cria a pasta para uploads, se não existir
UPLOAD_FOLDER = "imagens_temporarias"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def gerar_resposta_com_ollama(prompt_completo):
    """
    Envia um prompt para o servidor Ollama e retorna a resposta do modelo.
    """
    payload = {
        "model": MODELO_OLLAMA,
        "stream": False,
        "messages": [{"role": "user", "content": prompt_completo}]
    }
    
    try:
        # Usamos flush=True para garantir que a mensagem apareça no terminal imediatamente.
        print(f"Enviando para o modelo '{MODELO_OLLAMA}'. Aguardando...", flush=True)
        response = requests.post(URL_OLLAMA, json=payload, timeout=90.0)
        response.raise_for_status()
        result = response.json()
        print("Resposta recebida do Ollama.", flush=True)
        return result["message"]["content"]
        
    except requests.exceptions.Timeout:
        print("Erro: Timeout ao contatar o Ollama.", flush=True)
        return "Desculpe, o modelo demorou demais para responder."
    except requests.exceptions.RequestException as e:
        print(f"Erro ao se comunicar com o Ollama: {e}", flush=True)
        return f"Não consegui me conectar ao cérebro de IA. Verifique se o Ollama está rodando."
    except Exception as e:
        print(f"Erro inesperado na geração de resposta: {e}", flush=True)
        return "Ocorreu um erro inesperado ao processar sua mensagem."

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint principal do chat. Recebe a mensagem do usuário, constrói o 
    prompt e obtém a resposta do Ollama.
    """
    prompt_usuario = request.json.get("msg")
    if not prompt_usuario:
        return jsonify({"response": "Nenhuma mensagem recebida."}), 400

    print(f"\nMensagem recebida do usuário: {prompt_usuario}", flush=True)

    # --- MUDANÇA PARA DEPURAÇÃO ---
    # Para este teste, estamos enviando APENAS a mensagem do usuário,
    # sem nenhuma instrução extra. O objetivo é replicar a velocidade
    # do script 'diagnostico_ollama.py'.
    prompt_completo = prompt_usuario
    # --- FIM DA MUDANÇA ---

    resposta_bot = gerar_resposta_com_ollama(prompt_completo)
    return jsonify({"response": resposta_bot})

@app.route("/")
def home():
    """Serve a página inicial do chat."""
    return render_template("index.html")

if __name__ == "__main__":
    print("--- Servidor Flask do Chatbot Electra (MODO DE DEPURAÇÃO) ---")
    print(f"Usando o modelo Ollama: {MODELO_OLLAMA}")
    print(f"Conectando ao Ollama em: {URL_OLLAMA}")
    print("Acesse em: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False) # Debug desligado para evitar reinicializações
