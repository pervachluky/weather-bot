import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8668276795:AAE1cKzog34pQP6zEyLdE8Q9xmQp_dOkNUI"
WEATHER_API = "20fdfb87d84c26c97626e51736606b17"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши город 🌍")

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if data.get("main"):
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        text = f"🌤 Погода в городе {city}:\n🌡 Температура: {temp}°C\n☁️ {desc}"
    else:
        text = "❌ Город не найден"

    await update.message.reply_text(text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))

    print("Бот запущен...")
    app.run_polling()
