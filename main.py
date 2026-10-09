import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message and update.message.entities:
            for e in update.message.entities:
                if e.type in ["url","text_link","mention"]:
                    await update.message.delete()
                    return
        if update.message and (update.message.forward_from or update.message.forward_from_chat):
            await update.message.delete()
    except: pass

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.NEW_CHAT_MEMBERS, protect))
    app.run_polling()

flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot is Online!"

if __name__ == "__main__":
    Thread(target=run_bot).start()
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
