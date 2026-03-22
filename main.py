import telebot
import requests
import os

# Configuración de variables
TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

def get_prices():
    try:
        # Consulta directa a APIs de Binance y Bybit
        bn = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BNBUSDT", timeout=10).json()
        bb = requests.get("https://api.bybit.com/v5/market/tickers?category=spot&symbol=BNBUSDT", timeout=10).json()
        pb, py = float(bn['price']), float(bb['result']['list'][0]['lastPrice'])
        # Calculamos la diferencia
        spread = abs(((py - pb) / pb) * 100)
        return pb, py, spread
    except Exception:
        return None, None, None

@bot.message_handler(commands=['reporte'])
def send_report(message):
    pb, py, sp = get_prices()
    if pb:
        msg = f"📊 **MONITOR BNB**\n\n🔸 Binance: ${pb}\n🔹 Bybit: ${py}\n🚨 Spread: {sp:.2f}%"
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "❌ Error de conexión con los Exchanges.")

print("🚀 Monitor Activo...")
bot.infinity_polling()
