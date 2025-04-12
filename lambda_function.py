from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
import logging
import os
from fastapi import FastAPI, Request
import uvicorn

# Configuración básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")  # Ej: https://mi-app.onrender.com
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"

FOOTER_TEXT = (
    "\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
    "[➡️ 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙏𝙐𝙏𝙊𝙍𝙄𝘼𝙇𝙎](http://t.me/exeiolinks)\n\n"
    "[❤️ 𝙈𝙊𝙍𝙀 𝘾𝙃𝘼𝙉𝙉𝙀𝙇𝙎](http://t.me/packscereza)\n\n"
    "[💛 Tired of ads? Buy the VIP and get rid of them NOW.](https://freefans.sell.app/product/telegram-membership)\n"
    "➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
)

app = FastAPI()
telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

@telegram_app.post_init
async def setup_webhook(application):
    await application.bot.set_webhook(url=WEBHOOK_URL)
    logger.info(f"Webhook establecido en {WEBHOOK_URL}")

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post
    if not message:
        return

    try:
        if message.text:
            # Mensaje de solo texto → lo editamos
            new_text = f"{message.text}{FOOTER_TEXT}"
            await context.bot.edit_message_text(
                chat_id=message.chat_id,
                message_id=message.message_id,
                text=new_text,
                parse_mode="Markdown"
            )
        elif message.photo or message.video or message.document:
            # Mensaje con media → respondemos debajo
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=FOOTER_TEXT,
                reply_to_message_id=message.message_id,
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Error al manejar el mensaje: {e}")

telegram_app.add_handler(
    MessageHandler(filters.UpdateType.CHANNEL_POST, handle_channel_post)
)

@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run("lambda_function:app", host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

