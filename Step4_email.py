import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import json

load_dotenv()

APP_PASSWORD = os.getenv("APP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def send_email(db_data: dict) -> bool:
    record_id = db_data["id"]
    rate = db_data["rate"]
    base = db_data["base"]
    target = db_data["target"]
    created_at = db_data["created_at"]

    subject = f"Exchange Rate Alert: {base} → {target}"

    # ---- Load HTML template ----
    with open("template.html", "r") as f:
        body = f.read()

    body = body.replace("(id)", str(record_id))
    body = body.replace("(rate)", str(rate))
    body = body.replace("(base)", base)
    body = body.replace("(target)", target)
    body = body.replace("(created_at)", created_at)

    # ---- Create Email ----
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject

    # ✅ HTML format
    msg.attach(MIMEText(body, "html"))

    try:
        # ✅ Correct Gmail SSL usage
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("✅ Email sent successfully")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


if __name__ == "__main__":
    from Step1_scrap import scrap_data
    from Step3_db import init_db, save_db

    init_db()

    data = scrap_data()
    record = save_db(data)

    print(json.dumps(record, indent=2))

    send_email(record)