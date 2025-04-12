import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configuración de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Definir tu token de bot de Telegram
TOKEN = "YOUR_BOT_TOKEN"

# Función para iniciar el bot (comando /start)
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("¡Hola! Soy un bot que modifica mensajes.")

# Función para manejar los mensajes
async def handle_message(update: Update, context: CallbackContext):
    if update.message.text:  # Si el mensaje tiene texto
        await update.message.reply_text(f"Texto recibido: {update.message.text}")
    elif update.message.photo:  # Si el mensaje tiene una foto
        await update.message.reply_text(f"Imagen recibida.")
    # Aquí puedes añadir más lógica para manejar otros tipos de media si es necesario

# Función para agregar los enlaces embebidos al mensaje
async def add_links(update: Update, context: CallbackContext):
    # El texto que quieres añadir al final del mensaje
    append_text = "\n\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"\
                  "[➡️ 𝘿𝙊𝙒𝙉𝙇𝙊𝘼𝘿 𝙏𝙐𝙏𝙊𝙍𝙄𝘼𝙇𝙎](http://t.me/exeiolinks)\n\n"\
                  "[❤️ 𝙈𝙊𝙍𝙀 𝘾𝙃𝘼𝙉𝙉𝙀𝙇𝙎](http://t.me/packscereza)\n\n"\
                  "[💛 Tired of ads? Buy the VIP and get rid of them NOW.](https://freefans.sell.app/product/telegram-membership)\n"\
                  "➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
    
    # Aquí puedes revisar si el mensaje tiene media y modificarlo
    if update.message.text:
        # Modificar el mensaje de texto
        new_text = update.message.text + append_text
        await update.message.edit_text(new_text)
    elif update.message.photo:
        # Modificar el mensaje con foto (también puedes añadir texto con los enlaces embebidos)
        await update.message.edit_caption(caption="Imagen con enlaces embebidos\n" + append_text)

# Crear la aplicación y agregar los manejadores
async def main():
    application = Application.builder().token(TOKEN).build()

    # Agregar manejadores
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))  # Detecta mensajes de texto
    application.add_handler(MessageHandler(filters.PHOTO, handle_message))  # Detecta mensajes con foto

    # Ejecutar el bot para recibir mensajes
    await application.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


