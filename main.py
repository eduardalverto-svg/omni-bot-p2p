import os
import requests

# 1. Configuración de llaves (Secrets)
token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
gemini_key = os.getenv('GEMINI_API_KEY')

def obtener_precios():
    # Conexión directa con Binance para ver la realidad del mercado
    url = "https://api.binance.com/api/v3/ticker/price"
    res = requests.get(url).json()
    # Filtramos BTC, ETH y BNB para el análisis
    precios = {i['symbol']: i['price'] for i in res if i['symbol'] in ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']}
    return precios

def pedir_analisis_gemini(datos):
    # Le enviamos los datos a Gemini para que tome una decisión
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}"
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"Eres un experto en Arbitraje P2P. Analiza estos precios de Binance: {datos}. Dame una recomendación de trading o arbitraje en 3 puntos breves y directos."
            }]
        }]
    }
    response = requests.post(url, json=prompt).json()
    return response['candidates'][0]['content']['parts'][0]['text']

def ejecutar_patrulla():
    try:
        # El bot mira el mercado
        mercado = obtener_precios()
        # El bot piensa con Gemini
        analisis = pedir_analisis_gemini(mercado)
        
        # El bot te informa el resultado
        mensaje = (
            "🤖 **AGENTE OMNI-BOT ACTIVO**\n\n"
            f"📈 **Mercado:**\n- BTC: ${mercado['BTCUSDT']}\n- ETH: ${mercado['ETHUSDT']}\n\n"
            f"🧠 **Análisis de Inteligencia:**\n{analisis}"
        )
        
        url_tg = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url_tg, json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error en la patrulla: {e}")

if __name__ == "__main__":
    ejecutar_patrulla()
