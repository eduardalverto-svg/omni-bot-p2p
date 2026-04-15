import os
import requests

# Carga de llaves desde tus Secrets guardados
token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
gemini_key = os.getenv('GEMINI_API_KEY')

def obtener_datos_mercado():
    # Sacamos precio de Bitcoin y Ethereum de Binance
    url = "https://api.binance.com/api/v3/ticker/price"
    precios = requests.get(url).json()
    # Filtramos solo los que nos interesan
    data = {item['symbol']: item['price'] for item in precios if item['symbol'] in ['BTCUSDT', 'ETHUSDT']}
    return data

def pedir_analisis_gemini(datos):
    # Aquí es donde Gemini actúa como tu analista personal
    url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}"
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"Analiza estos precios de Binance: {datos}. Dame un consejo rápido de arbitraje o trading en 2 frases."
            }]
        }]
    }
    res = requests.post(url_gemini, json=prompt)
    return res.json()['candidates'][0]['content']['parts'][0]['text']

def ejecutar_bot_autonomo():
    try:
        mercado = obtener_datos_mercado()
        analisis = pedir_analisis_gemini(mercado)
        
        mensaje = (
            "🤖 **OMNI-BOT AUTÓNOMO**\n\n"
            f"📈 **Precios:**\n- BTC: ${mercado['BTCUSDT']}\n- ETH: ${mercado['ETHUSDT']}\n\n"
            f"💡 **Análisis de Gemini:**\n{analisis}"
        )
        
        url_tg = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url_tg, json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    ejecutar_bot_autonomo()
