import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from downloader import download_video

TOKEN = os.environ.get("BOT_TOKEN")  # توکن از محیط یا Render

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 لینک ویدیوی یوتیوب رو بفرست!\nبرای دریافت فقط صدا بنویس: /audio [لینک]")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("⏬ در حال دانلود و ارسال فایل...")
    try:
        file_path = download_video(url)
        await update.message.reply_video(video=open(file_path, 'rb'))
        os.remove(file_path)
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {str(e)}")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        url = context.args[0]
        await update.message.reply_text("🎧 در حال دانلود فایل صوتی...")
        try:
            file_path = download_video(url, only_audio=True)
            await update.message.reply_audio(audio=open(file_path, 'rb'))
            os.remove(file_path)
        except Exception as e:
            await update.message.reply_text(f"❌ خطا: {str(e)}")
    else:
        await update.message.reply_text("لطفاً لینک یوتیوب را هم وارد کن.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("audio", handle_audio))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
