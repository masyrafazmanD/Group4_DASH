import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_notification(record: dict, alert_type: str) -> bool:

    record_id = record["id"]
    rate = record["rate"]
    base = record["base"]
    target = record["target"]
    created_at = record["created_at"]

    icon = "🔴" if alert_type == "HIGH" else "🔵"

    message = (
        f"{icon} <b>Exchange Alert Triggered</b>\n\n"
        f"<b>Condition:</b> {alert_type}\n\n"
        f"<b>ID:</b> <code>{record_id}</code>\n"
        f"<b>Time:</b> {created_at}\n\n"
        f"<b>{base} → {target}</b>\n"
        f"<b>Rate:</b> <code>{rate}</code>\n"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(TELEGRAM_URL, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Telegram sent")
        return True

    except Exception as e:
        print("❌ Telegram failed:", e)
        return False