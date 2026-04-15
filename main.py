import os
import requests

# Estos son los secretos que ya guardaste en GitHub
token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

def enviar_saludo():
    mensaje = "🚀 ¡Omni-Bot P2P Activado con Éxito! Estoy patrullando."
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={mensaje}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Mensaje enviado")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    enviar_saludo()
