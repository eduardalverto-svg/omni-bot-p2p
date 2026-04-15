import os
import requests

token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
gemini_key = os.getenv('GEMINI_API_KEY')

def ejecutar():
    try:
        # 1. Ver precios en Binance
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()
        precio = res['price']
        
        # 2. Pedir consejo a Gemini
        url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}"
        prompt = {"contents": [{"parts": [{"text": f"El BTC está en {precio}. Dame un consejo de trading corto."}]}]}
        ai_res = requests.post(url_gemini, json=prompt).json()
        consejo = ai_res['candidates'][0]['content']['parts'][0]['text']
        
        # 3. Enviar a Telegram
        mensaje = f"🤖 **BOT ACTIVO**\n📈 BTC: ${precio}\n💡 IA: {consejo}"
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar()
