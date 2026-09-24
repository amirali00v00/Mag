import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
UNSPLASH_KEY = os.environ["UNSPLASH_KEY"]
SECRET_PATH = os.environ.get("SECRET_PATH", "webhook-secret")

# Render خودش این رو ست می‌کنه (مثلاً: photo-bot.onrender.com)
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL", "")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
UNSPLASH_API = "https://api.unsplash.com/search/photos"
PORT = int(os.environ.get("PORT", 10000))
