from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import yt_dlp

TOKEN = 
"8589633230:AAG1BznTzIWgCsxLPwxGG6vb87qHHw9UCSA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a video link")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    keyboard = [
        [
            InlineKeyboardButton("144p", callback_data=f"{url}|144"),
            InlineKeyboardButton("360p", callback_data=f"{url}|360"),
            InlineKeyboardButton("720p", callback_data=f"{url}|720")
        ],
        [
            InlineKeyboardButton("1080p", callback_data=f"{url}|1080"),
            InlineKeyboardButton("4K", callback_data=f"{url}|2160")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select Quality", reply_markup=reply_markup)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    url, quality = query.data.split("|")

    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best',
        'outtmpl': 'video.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await query.message.reply_text("Downloading finished")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(download))

app.run_polling()
