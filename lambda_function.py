import logging
import json
import nest_asyncio
import os
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Aplica nest_asyncio para evitar errores de loop
nest_asyncio.apply()

# Configura el logging
logging.basicConfig(level=logging.INFO)

# Firma con enlaces embebidos
FOOTER = (
    "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
    '<a href="http://t.me/exeiolinks">➡️ 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙏𝙐𝙏𝙊𝙍𝙄𝘼𝙇𝙎</a>\n\n'
    '<a href="http://t.me/packscereza">❤️ 𝙈𝙊𝙍𝙀 𝘾𝙃𝘼𝙉𝙉𝙀𝙇𝙎</a>\n\n'
    '<a href="https://freefans.sell.app/product/telegram-membership">💛 Tired of ads? Buy the VIP and get rid of them NOW.</a>\n'
    "➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
)

# Manejador de mensajes en canales
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        message = update.channel_post
        if not message.text:
            return

        new_text = f"{message.text}\n\n{FOOTER}"

        try:
            await context.bot.edit_message_text(
                chat_id=message.chat_id,
                message_id=message.message_id,
                text=new_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
            logging.info(f"Mensaje editado en canal: {message.chat.title}")
        except Exception as e:
            logging.error(f"Error al editar el mensaje: {e}")

# Lambda handler
def lambda_handler(event, context):
    logging.basicConfig(level=logging.INFO)
    logging.info("Evento recibido: %s", json.dumps(event))

    # Si es un webhook de Telegram
    if "body" in event:
        update_data = json.loads(event["body"])

        # Crear la aplicación de Telegram
        app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
        app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, handle_message))

        # Usar asyncio.run para ejecutar la función asincrónica en Lambda
        asyncio.run(run_app(app, update_data))

    return {
        "statusCode": 200,
        "body": json.dumps("OK")
    }

async def run_app(app, update_data):
    await app.initialize()
    await app.process_update(Update.de_json(update_data, app.bot))
    await app.shutdown()

