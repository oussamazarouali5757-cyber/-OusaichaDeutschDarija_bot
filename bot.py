import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from gtts import gTTS
import datetime
import os

# فعّل السجل باش تعرف الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# حط هنا التوكن ديالك من BotFather
TOKEN = "حط_التوكن_ديالك_هنا"

# قائمة الكلمات اليومية (تقدر تزيد)
words = [
    {"de": "Hallo", "ma": "سلام", "audio": "hallo.mp3"},
    {"de": "Danke", "ma": "شكراً", "audio": "danke.mp3"},
    {"de": "Guten Morgen", "ma": "صباح الخير", "audio": "guten_morgen.mp3"},
]

# إنشاء المجلد ديال الصوت إذا ما كاينش
if not os.path.exists("audio"):
    os.mkdir("audio")

# توليد الصوتيات تلقائياً
for w in words:
    path = f"audio/{w['audio']}"
    if not os.path.exists(path):
        tts = gTTS(w["de"], lang="de")
        tts.save(path)

# أمر البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Willkommen! مرحبا بك فـ بوت تعلم الألمانية باللهجة المغربية 🇩🇪🇲🇦.\n\nكل نهار غادي توصلك كلمة + الصوت + الترجمة.")

# أمر كلمة اليوم
async def word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = datetime.datetime.now().day % len(words)
    word = words[index]
    await update.message.reply_text(f"🇩🇪 {word['de']} → 🇲🇦 {word['ma']}")
    with open(f"audio/{word['audio']}", "rb") as audio:
        await update.message.reply_voice(audio)

# إعداد التطبيق
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("word", word))

if __name__ == "__main__":
    print("🚀 البوت خدام...")
    app.run_polling()
