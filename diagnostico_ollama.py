import requests
import time

# Endpoint direto do seu servidor Ollama
URL_OLLAMA = "http://localhost:11434/api/chat"

# Modelo que você está usando.
# IMPORTANTE: Se o teste com 'llama3.2' for muito lento,
# troque para um modelo bem menor, como 'tinyllama' ou 'gemma:2b'.
# Certifique-se de ter baixado o modelo menor antes com: ollama pull tinyllama
MODELO_TESTE = "llama3.2" 

# Payload simples para o teste
PAYLOAD = {
    "model": MODELO_TESTE,
    "stream": False,
    "messages": [
        {"role": "user", "content": "Olá"}
    ]
}

print(f"--- Iniciando teste de diagnóstico com o modelo: {MODELO_TESTE} ---")
print("Enviando uma requisição simples para o Ollama...")

try:
    # Medindo o tempo de resposta
    start_time = time.time()
    
    # Fazendo a requisição com um timeout de 60 segundos
    response = requests.post(URL_OLLAMA, json=PAYLOAD, timeout=60.0)
    
    end_time = time.time()
    
    # Verificando se a requisição foi bem-sucedida
    response.raise_for_status()
    
    result = response.json()
    
    print("\n--- SUCESSO! ---")
    print(f"O Ollama respondeu em: {end_time - start_time:.2f} segundos.")
    print("\nResposta recebida do modelo:")
    print(result["message"]["content"])

except requests.exceptions.Timeout:
    print("\n--- ERRO: Timeout ---")
    print("A requisição demorou mais de 60 segundos para responder.")
    print("Isso indica que o modelo está demorando demais para processar.")
    print("Causa provável: Recursos insuficientes (CPU/RAM) para o modelo selecionado.")

except requests.exceptions.RequestException as e:
    print(f"\n--- ERRO: Falha na Conexão ---")
    print(f"Não foi possível se conectar ao Ollama em {URL_OLLAMA}.")
    print("Verifique se o servidor Ollama está rodando corretamente.")
    print(f"Detalhes do erro: {e}")

except Exception as e:
    print(f"\n--- ERRO: Inesperado ---")
    print(f"Ocorreu um erro inesperado: {e}")

