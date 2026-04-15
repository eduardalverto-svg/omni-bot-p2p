import os
import requests
from pybit.unified_trading import HTTP
from langchain_google_genai import ChatGoogleGenerativeAI

# --- SECRETOS ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

def ejecutar_super_bot():
    try:
        # 1. Datos de Mercado (Binance Gratis)
        btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()['price']
        
        # 2. Sentimiento (Scraping rápido)
        res_news = requests.get("https://api.coingecko.com/api/v3/search/trending").json()
        top_coin = res_news['coins'][0]['item']['name']
        
        # 3. Inteligencia Pro con LangChain (Gemini 1.5 Pro)
        # Usamos LangChain para que el razonamiento sea más profundo
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_KEY)
        
        analisis = llm.invoke(
            f"Actúa como un trader experto. BTC está en {btc}. La moneda tendencia es {top_coin}. "
            f"Dime en 2 oraciones qué estrategia usar en Bybit y si el P2P de Binance está en riesgo."
        )

        # 4. Enviar al HUD de Telegram
        mensaje = (
            f"👑 **SÚPER BOT AUTÓNOMO V2**\n\n"
            f"📈 BTC: ${float(btc):,.2f}\n"
            f"🔥 Trending: {top_coin}\n\n"
            f"🧠 **ANÁLISIS PRO:**\n{analisis.content}"
        )
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar_super_bot()
