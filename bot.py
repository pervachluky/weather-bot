import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8668276795:AAE1cKzog34pQP6zEyLdE8Q9xmQp_dOkNUI"
WEATHER_API = "20fdfb87d84c26c97626e51736606b17"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет 👋 Напиши город, и я покажу погоду 🌤️")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text

    # текущая погода
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"
    data = requests.get(url).json()

    # прогноз
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API}&units=metric"
    forecast_data = requests.get(forecast_url).json()

    if data.get("main"):
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        translations = {
            "clear sky": "ясно ☀️",
            "overcast clouds": "пасмурно ☁️",
            "few clouds": "малооблачно 🌤️",
            "scattered clouds": "облачно 🌥️",
            "broken clouds": "облачно ☁️",
            "light rain": "небольшой дождь 🌧️",
            "rain": "дождь 🌧️",
            "snow": "снег ❄️"
        }

        desc = translations.get(desc, desc)

        forecast_text = "\n\nПрогноз:\n"

        if forecast_data.get("list"):
            for i in range(0, 40, 8):
                item = forecast_data["list"][i]
                date = item["dt_txt"].split(" ")[0]
                t = item["main"]["temp"]
                d = item["weather"][0]["description"]

                d = translations.get(d, d)

                forecast_text += f"{date}: {t}°C, {d}\n"

        await update.message.reply_text(
            f"Сейчас в {city}: {temp}°C, {desc}{forecast_text}"
        )

    else:
        await update.message.reply_text("Город не найден 😢")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()