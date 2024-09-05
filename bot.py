import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHATBOT_API_URL = os.getenv("CHATBOT_API_URL")
CHATBOT_API_KEY = os.getenv("CHATBOT_API_KEY")

# Fungsi untuk mengirim pertanyaan ke API chatbot
def query_chatbot(question: str):
    headers = {
        "CHATBOT-API-KEY": CHATBOT_API_KEY
    }
    payload = {
        "question": question
    }

    try:
        response = requests.post(f"{CHATBOT_API_URL}/chat", headers=headers, json=payload)
        
        # Jika respons berhasil (status code 200)
        if response.status_code == 200:
            data = response.json()
            return data['answer']
        else:
            # Jika status code selain 200
            return "Salam Harmoni🙏 Maaf, terjadi kesalahan saat menghubungi chatbot, silahkan coba lagi nanti. Terimakasih."
    
    # Menangani error jika terjadi kesalahan koneksi atau request timeout
    except requests.exceptions.RequestException:
        # Pesan yang sama jika ada masalah koneksi atau error lainnya
        return "Salam Harmoni🙏 Maaf, terjadi kesalahan saat menghubungi chatbot, silahkan coba lagi nanti. Terimakasih."

# Fungsi untuk menangani pesan pengguna
async def handle_message(update: Update, context):
    question = update.message.text

    # Mengirim status "typing" selama pemrosesan
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Simulasikan jeda kecil untuk menambah realisme (opsional)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Mengirim pertanyaan ke API chatbot dan mendapatkan jawabannya
    answer = query_chatbot(question)

    # Mengirimkan jawaban ke pengguna
    await update.message.reply_text(answer)

# Fungsi untuk memulai bot
async def start(update: Update, context):
    await update.message.reply_text("Salam Harmoni🙏 Saya adalah BOT AI di Sistem Informasi PMB Undiksha, silakan ajukan pertanyaan Anda mengenai PMB Undiksha. Terimakasih.")

# Fungsi utama untuk menjalankan bot Telegram
if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Menambahkan handler untuk perintah /start
    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    # Menambahkan handler untuk menangani semua pesan
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    application.add_handler(message_handler)

    # Menjalankan bot
    application.run_polling()
