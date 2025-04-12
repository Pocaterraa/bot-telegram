import logging
import json
import nest_asyncio
import os
import asyncio
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

nest_asyncio.apply()
logging.basicConfig(level=logging.INFO)

# IDs de los canales autorizados
ALLOWED_CHANNEL_IDS = [
    -1001600499562,
    -1002325651346,
]

# Firma embebida
FOOTER = (
    "➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
    '<a href="http://t.me/exeiolinks">➡️ 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙏𝙐𝙏𝙊𝙍𝙄𝘼𝙇𝙎</a>\n\n'
    '<a href="http://t.me/packscereza">❤️ 𝙈𝙊𝙍𝙀 𝘾𝙃𝘼𝙉𝙉𝙀𝙇𝙎</a>\n\n'
    '<a href="https://freefans.sell.app/product/telegram-membership">💛 Tired of ads? Buy the VIP and get rid of them NOW.</a>\n'
    "➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
)

# Manejador de mensajes de canales
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.channel_post:
        return

    message = update.channel_post
    chat_id = message.chat_id

    # Validar si el canal está autorizado
    if chat_id not in ALLOWED_CHANNEL_IDS:
        logging.info(f"Canal no autorizado: {chat_id}")
        return

    # Obtener texto o caption
    original_text = message.text or message.caption
    if not original_text:
        return

    new_text = f"{original_text}\n\n{FOOTER}"

    try:
        if message.text:
            # Mensaje de solo texto
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message.message_id,
                text=new_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        elif message.caption:
            # Mensaje con multimedia y caption
            await context.bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message.message_id,
                caption=new_text,
                parse_mode=ParseMode.HTML,
            )
        logging.info(f"Mensaje editado en canal {chat_id}")
    except Exception as e:
        logging.error(f"Error al editar el mensaje: {e}")

# Lambda handler
def lambda_handler(event, context):
    logging.info("Evento recibido: %s", json.dumps(event))

    if "body" in event:
        update_data = json.loads(event["body"])

        app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
        app.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, handle_message))

        asyncio.run(run_app(app, update_data))

    return {
        "statusCode": 200,
        "body": json.dumps("OK")
    }

async def run_app(app, update_data):
    await app.initialize()
    await app.process_update(Update.de_json(update_data, app.bot))
    await app.shutdown()

