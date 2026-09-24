import logging
import random
import requests

from config import TELEGRAM_API, UNSPLASH_API, UNSPLASH_KEY

logger = logging.getLogger(__name__)
session = requests.Session()


def search_photo(query: str):
    try:
        r = session.get(
            UNSPLASH_API,
            params={"query": query, "page": 1, "per_page": 10},
            headers={"Authorization": f"Client-ID {UNSPLASH_KEY}"},
            timeout=15,
        )
        r.raise_for_status()
        results = r.json().get("results", [])
        return random.choice(results) if results else None
    except requests.RequestException as e:
        logger.error("Unsplash error: %s", e)
        return None


def send_photo(chat_id: int, photo_url: str, caption: str):
    try:
        session.post(
            f"{TELEGRAM_API}/sendPhoto",
            json={"chat_id": chat_id, "photo": photo_url, "caption": caption},
            timeout=15,
        )
    except requests.RequestException as e:
        logger.error("sendPhoto error: %s", e)


def send_message(chat_id: int, text: str):
    try:
        session.post(
            f"{TELEGRAM_API}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=15,
        )
    except requests.RequestException as e:
        logger.error("sendMessage error: %s", e)
