import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8668276795:AAE1cKzog34pQP6zEyLdE8Q9xmQp_dOkNUI"
WEATHER_API = "20fdfb87d84c26c97626e51736606b17"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши город 🌍")

async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()

    if data.get("list"):
        text = f"📅 Прогноз на 5 дней для {city}:\n\n"

        # берем по одному значению в день (каждые 8 записей ≈ 24 часа)
        for i in range(0, 40, 8):
            day = data["list"][i]
            date = day["dt_txt"].split(" ")[0]
            temp = day["main"]["temp"]
            desc = day["weather"][0]["description"]

            text += f"{date}\n🌡 {temp}°C | ☁️ {desc}\n\n"
    else:
        text = "❌ Город не найден"

    await update.message.reply_text(text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))

    print("Бот запущен...")
    app.run_polling()
