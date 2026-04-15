import os
import requests
from pybit.unified_trading import HTTP
from langchain_google_genai import ChatGoogleGenerativeAI
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN DE LLAVES ---
token = os.getenv('TELEGRAM_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')
gemini_key = os.getenv('GEMINI_API_KEY')

# --- 1. MÓDULO BYBIT (Tu Balance Real) ---
# Aquí usaremos tus llaves de Bybit que debes agregar a "Secrets" pronto
def consultar_bybit():
    try:
        # Por ahora simulamos hasta que metas tus API Keys de Bybit en GitHub
        return "Balance en Bybit: 1,250 USDT. Posición abierta: BTC/USDT Long."
    except Exception as e:
        return f"Error en Bybit: {e}"

# --- 2. MÓDULO SENTIMIENTO (Web Scraping) ---
def analizar_sentimiento():
    try:
        # Escaneamos una fuente de noticias crypto
        res = requests.get("https://cryptopanic.com/news/bitcoin/")
        soup = BeautifulSoup(res.text, 'html.parser')
        titulares = [t.text for t in soup.find_all('h2')[:3]]
        return f"Últimas noticias: {'. '.join(titulares)}"
    except:
        return "No se pudo obtener el sentimiento actual."

# --- 3. INTELIGENCIA CON LANGCHAIN (Gemini 1.5 Pro) ---
def super_cerebro(datos_mercado, sentimiento, balance):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=gemini_key)
    prompt = f"""
    Eres un Agente Autónomo de Trading. 
    Datos: {datos_mercado}
    Sentimiento: {sentimiento}
    Mi Balance: {balance}
    Analiza y dime: ¿Compro, Vendo o Espero en Bybit? Resumen corto para Telegram.
    """
    respuesta = llm.invoke(prompt)
    return respuesta.content

# --- EJECUCIÓN PRINCIPAL ---
def ejecutar_patrulla():
    # Obtener precio de Binance (lo que ya hacíamos)
    precio_binance = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT").json()['price']
    
    balance = consultar_bybit()
    noticias = analizar_sentimiento()
    decision = super_cerebro(precio_binance, noticias, balance)
    
    mensaje = f"🚀 **REPORTE SÚPER BOT**\n\n📊 BTC/USDT: ${precio_binance}\n📰 {noticias}\n💰 {balance}\n\n🧠 **DECISIÓN IA:**\n{decision}"
    
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", json={"chat_id": chat_id, "text": mensaje, "parse_mode": "Markdown"})

if __name__ == "__main__":
    ejecutar_patrulla()
