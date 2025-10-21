from flask import Flask, request, jsonify
import pandas as pd
import os
from telegram import Bot

app = Flask(__name__)

# تحميل متغيرات البيئة
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
LOG_CSV = os.getenv("LOG_CSV", "alerts_log.csv")
ENABLE_SELENIUM_AUTOMATION = os.getenv("ENABLE_SELENIUM_AUTOMATION", "False") == "True"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data.get("secret") != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid secret"}), 403

    # تسجيل الإشارة
    df = pd.DataFrame([data])
    if os.path.exists(LOG_CSV):
        df.to_csv(LOG_CSV, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_CSV, index=False)

    # إرسال إشعار لتليجرام
    message = f"""📈 TradingView Signal
Symbol: {data.get('symbol')}
Action: {data.get('action')}
Price: {data.get('price')}"""
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
