from Step1_scrap import scrap_data
from Step3_db import init_db, save_db
from Step2_excel import save_to_excel
#from Step4_email import send_email
from Step4_telegram import send_telegram_notification



def check_alert(rate):
    # Define threshold logic
    if rate > 3.90:
        return "MYR Weak"
    elif rate < 3.80:
        return "MYR Strong"
    return None


def main():
    print("🚀 Start Exchange Tracker...")

    init_db()

    # Step 1: Fetch data
    data = scrap_data()

    if not data:
        print("❌ API fetch failed")
        return

    rate = data["rate"]
    print(f"✅ Current Rate: {rate}")

    # Step 2: Check condition
    alert_type = check_alert(rate)

    # Step 3: Send alert if needed
    if alert_type:
        print(f"⚠️ ALERT triggered: {alert_type}")
        record = save_db(data)   # Save first so email has DB ID
        # send_email(record)
        send_telegram_notification(record, alert_type)
        
    else:
        print("✅ No alert triggered")
        record = save_db(data)

    # Step 4: Save to Excel
    save_to_excel(record)

    print("✅ Successfully run the pipeline")


if __name__ == "__main__":
    main()