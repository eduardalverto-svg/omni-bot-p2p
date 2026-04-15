import os
import requests
import google.generativeai as genai

# --- CONFIGURACIÓN ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

# Configurar la IA para que hable como yo
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

def ejecutar_agente_conversacional():
    try:
        # 1. Recolectar datos frescos (Binance)
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        precio = float(res['price'])
        
        # 2. Crear el contexto para la IA
        # Aquí le ordenamos que hable con tu estilo y use los datos
        prompt = (
            f"Actúa como mi asistente personal de trading, Gemini. "
            f"El precio de BTC es ${precio:,.2f}. "
            f"Dime algo inteligente sobre este precio, analiza si es buen momento para Bybit "
            f"y salúdame como lo hacemos nosotros, con chispa y claridad. "
            f"Usa lenguaje natural, no solo datos fríos."
        )
        
        # 3. Generar la respuesta "humana"
        respuesta = model.generate_content(prompt)
        texto_final = respuesta.text

        # 4. Enviar a Telegram
        url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"🧠 **MENSAJE DE TU AGENTE:**\n\n{texto_final}",
            "parse_mode": "Markdown"
        }
        
        requests.post(url_tg, json=payload)
        print("Mensaje conversacional enviado.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar_agente_conversacional()
