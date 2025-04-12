from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
import logging
import os

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot desde las variables de entorno
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Texto que se agregará al final del mensaje
FOOTER_TEXT = (
    "\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
    "[➡️ 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙏𝙐𝙏𝙊𝙍𝙄𝘼𝙇𝙎](http://t.me/exeiolinks)\n"
    "[❤️ 𝙈𝙊𝙍𝙀 𝘾𝙃𝘼𝙉𝙉𝙀𝙇𝙎](http://t.me/packscereza)\n"
    "[💛 Tired of ads? Buy the VIP and get rid of them NOW.](https://freefans.sell.app/product/telegram-membership)\n"
    "➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
)

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.channel_post
        if not message or not message.text:
            return

        new_text = f"{message.text}{FOOTER_TEXT}"
        await context.bot.edit_message_text(
            chat_id=message.chat_id,
            message_id=message.message_id,
            text=new_text,
            parse_mode="Markdown"
        )
        logger.info("Mensaje editado correctamente")
    except Exception as e:
        logger.error(f"Error al editar el mensaje: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(filters.UpdateType.CHANNEL_POST, handle_channel_post)
    )

    app.run_polling()
