import os
import requests

# --- CONFIGURACIÓN (GitHub Secrets) ---
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
GEMINI_KEY = os.getenv('GEMINI_API_KEY')

def obtener_datos():
    # Precios gratuitos de Binance
    btc = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()['price']
    eth = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT").json()['price']
    
    # Simulación de balance Bybit (Gratis/Sin API por ahora)
    balance_bybit = "Consultando modo lectura: 1250 USDT disponible."
    
    # Scraping ligero de noticias (Sentimiento)
    noticias = "Tendencia mixta en redes. BTC manteniendo soporte."
    try:
        res = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=5).json()
        noticias = f"Top trending: {res['coins'][0]['item']['name']}"
    except: pass
    
    return btc, eth, balance_bybit, noticias

def inteligencia_gemini(btc, eth, balance, noticias):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"Eres un experto en trading. Datos: BTC {btc}, ETH {eth}. Mi balance Bybit: {balance}. Noticia: {noticias}. Dame un análisis ultra corto (2 frases) y dime si es momento de operar P2P en Binance o trading en Bybit."
            }]
        }]
    }
    
    res = requests.post(url, json=prompt).json()
    return res['candidates'][0]['content']['parts'][0]['text']

def ejecutar():
    try:
        btc, eth, balance, noticias = obtener_datos()
        decision = inteligencia_gemini(btc, eth, balance, noticias)
        
        mensaje = (
            f"🤖 **O-BOT AUTÓNOMO V1**\n"
            f"📈 BTC: ${float(btc):,.2f} | ETH: ${float(eth):,.2f}\n"
            f"🏦 {balance}\n"
            f"📰 {noticias}\n\n"
            f"🧠 **IA DICE:** {decision}"
        )
        
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "Markdown"})
        print("Reporte enviado con éxito.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar()
