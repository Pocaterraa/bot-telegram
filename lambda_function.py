import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import nest_asyncio
import asyncio
from fastapi import FastAPI, Request  # IMPORTAR 'Request' AQUÍ
import uvicorn

# Evitar el error de event loop ya que en algunos entornos (como Render), el event loop ya está corriendo
nest_asyncio.apply()

# Configurar el bot
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear la instancia de FastAPI para recibir el webhook
app = FastAPI()

# Función de manejo para el comando /start
async def start(update: Update, context):
    await update.message.reply_text("¡Hola! Soy tu bot. ¿Cómo puedo ayudarte?")

# Función para manejar los mensajes
async def handle_message(update: Update, context):
    text = update.message.text
    chat_id = update.message.chat.id
    
    # Si el mensaje contiene texto, agregar el enlace embebido al final
    if text:
        # El texto a agregar
        additional_text = (
            "\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            "[➡️ 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙏𝙐𝙏𝙊𝙍𝙄𝘼𝙇𝙎](http://t.me/exeiolinks)\n\n"
            "[❤️ 𝙈𝙊𝙍𝙀 𝘾𝙃𝘼𝙉𝙉𝙀𝙇𝙎](http://t.me/packscereza)\n\n"
            "[💛 Tired of ads? Buy the VIP and get rid of them NOW.](https://freefans.sell.app/product/telegram-membership)\n"
            "➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
        )
        # Modificar el mensaje
        await update.message.reply_text(text + additional_text)

# Crear la aplicación de Telegram
async def main():
    application = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()

    # Agregar handlers para los comandos y mensajes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Configurar el webhook con tu dominio de webhook
    webhook_url = "https://bot-telegram-e0lh.onrender.com/webhook"
    await application.bot.set_webhook(webhook_url)

# Configurar FastAPI para el puerto adecuado
@app.post("/webhook")
async def webhook(request: Request):  # AQUÍ
    json_str = await request.json()
    update = Update.de_json(json_str, application.bot)
    application.update_queue.put(update)
    return {"status": "ok"}

# Configurar el servidor FastAPI para que escuche el puerto
if __name__ == "__main__":
    # Usar el puerto asignado por Render (o 8000 como fallback)
    port = int(os.getenv("PORT", 8000))  # Render asignará un puerto automáticamente a través de la variable de entorno 'PORT'
    
    # Ejecutar la aplicación FastAPI
    uvicorn.run(app, host="0.0.0.0", port=port)

    # Ejecutar el bot en el evento loop asíncrono
    asyncio.run(main())
