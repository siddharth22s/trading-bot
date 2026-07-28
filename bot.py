from flask import Flask, request
import requests

app = Flask(__name__)

# Aapka Telegram Bot Token aur Chat ID
TELEGRAM_BOT_TOKEN = "8544853109:AAF12GfyXNjChOk6FxxmHzRicGjVwq1MUfE"
TELEGRAM_CHAT_ID = "1900882734"


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending message: {e}")


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # TradingView se data aayega
    if data:
        # Data extract karna
        symbol = data.get("symbol", "N/A")
        action = str(data.get("action", "N/A")).upper()
        price = data.get("price", "N/A")
        timeframe = data.get("timeframe", "N/A")

        # Telegram message format
        msg = f"🚨 <b>TRADINGVIEW SIGNAL</b> 🚨\n\n"
        msg += f"📈 <b>Symbol:</b> {symbol}\n"
        msg += f"⚡ <b>Action:</b> {action}\n"
        msg += f"💰 <b>Price:</b> {price}\n"
        msg += f"⏰ <b>Timeframe:</b> {timeframe}\n"

        # Telegram par notification bhejna
        send_telegram_message(msg)

        print(f"Alert sent to Telegram for {symbol} ({action})")
        return "Notification Sent!", 200

    return "No Data", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)