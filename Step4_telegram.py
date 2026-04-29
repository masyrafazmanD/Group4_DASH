# ============================================================
# Step5_telegram.py
# WHAT  : Send Telegram notification for Exchange Rate Alert
#
# SETUP (do this once):
#   1. Open Telegram → search @BotFather → send /newbot
#   2. Copy BOT TOKEN
#   3. Start chat with your bot (send any message)
#   4. Visit:
#      https://api.telegram.org/bot<TOKEN>/getUpdates
#   5. Copy "chat.id"
#   6. Add both to your .env file:
#
#      TELEGRAM_BOT_TOKEN=xxxx
#      TELEGRAM_CHAT_ID=xxxx
# ============================================================

import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_telegram_notification(record: dict, alert_type: str) -> bool:
    """
    Send Telegram alert message for exchange rate monitoring.

    Args:
        record: dict with keys
            { id, base, target, rate, created_at }
        alert_type: "HIGH" or "LOW"

    Returns:
        True if sent successfully, False otherwise
    """

    record_id  = record["id"]
    base       = record["base"]
    target     = record["target"]
    rate       = record["rate"]
    created_at = record["created_at"]

    # Choose icon based on condition
    icon = "🔴" if alert_type == "HIGH" else "🔵"

    message = (
        f"{icon} <b>Exchange Alert Triggered</b>\n\n"
        f"<b>Condition:</b> {alert_type}\n\n"

        f"<b>Record ID:</b> <code>{record_id}</code>\n"
        f"<b>Time:</b> {created_at}\n\n"

        f"<b>Currency:</b> {base} → {target}\n"
        f"<b>Rate:</b> <code>{rate}</code>\n\n"

        f"📊 Data saved to system (DB + Excel)"
    )

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        print("[TELEGRAM] Sending notification...")

        response = requests.post(
            TELEGRAM_API_URL,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

        print(f"[TELEGRAM] ✅ Sent (chat_id: {TELEGRAM_CHAT_ID})")
        return True

    except requests.exceptions.HTTPError as e:
        print(f"[TELEGRAM] HTTP error: {e} — Response: {response.text}")
        return False

    except Exception as e:
        print(f"[TELEGRAM] Failed to send notification: {e}")
        return False


# ✅ Test block
if __name__ == "__main__":
    test_record = {
        "id": 1,
        "base": "USD",
        "target": "MYR",
        "rate": 4.82,
        "created_at": "2026-04-22 10:50:00"
    }

    send_telegram_notification(test_record, "HIGH")