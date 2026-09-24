import logging

import requests
from flask import Flask, request, jsonify

from config import (
    TELEGRAM_API,
    SECRET_PATH,
    RENDER_EXTERNAL_URL,
    PORT,
)
from services import search_photo, send_photo, send_message

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# ---------- ست کردن Webhook روی تلگرام ----------
def set_webhook():
    if not RENDER_EXTERNAL_URL:
        logger.warning("RENDER_EXTERNAL_URL ست نشده! Webhook ثبت نشد.")
        return

    webhook_url = f"{RENDER_EXTERNAL_URL.rstrip('/')}/{SECRET_PATH}"

    try:
        r = requests.post(
            f"{TELEGRAM_API}/setWebhook",
            json={"url": webhook_url, "drop_pending_updates": True},
            timeout=10,
        )
        logger.info("setWebhook: %s", r.json())
    except requests.RequestException as e:
        logger.error("setWebhook failed: %s", e)


# ---------- هندل پیام ----------
def handle_message(message: dict):
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()

    if not chat_id or not text:
        return

    logger.info("📩 chat=%s text=%s", chat_id, text)

    if text.startswith("/start"):
        send_message(chat_id, "سلام 👋\nبرای گرفتن عکس بفرست:\n/photo cat")
        return

    if text.startswith("/photo"):
        query = text[len("/photo"):].strip()

        if not query:
            send_message(chat_id, "مثلاً بفرست:\n/photo cat")
            return

        photo = search_photo(query)

        if not photo:
            send_message(chat_id, "عکسی پیدا نشد 😕")
            return

        send_photo(
            chat_id,
            photo["urls"]["regular"],
            f"📸 عکاس: {photo['user']['name']}\n🔎 جستجو: {query}",
        )


# ---------- Webhook ----------
@app.route(f"/{SECRET_PATH}", methods=["POST"])
def webhook():
    update = request.get_json(silent=True) or {}
    msg = update.get("message")
    if msg:
        handle_message(msg)
    return jsonify(ok=True), 200


# ---------- Health ----------
@app.route("/", methods=["GET"])
def health():
    return "OK", 200


# 👇 موقع import توی gunicorn هم وبهوک ست بشه
set_webhook()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
