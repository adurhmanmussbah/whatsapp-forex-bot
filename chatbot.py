from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Environment variables from .env
WA_TOKEN = os.getenv("WHATSAPP_TOKEN")              # Your WhatsApp access token
PHONE_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")    # Your WhatsApp phone number ID
API_KEY = os.getenv("API_KEY")                      # Your TwelveData API key

# 👇 Choose any verify token you like – MUST match what you put in Meta dashboard
VERIFY_TOKEN = "joba123"


# =========================
# Helper: send WhatsApp message
# =========================
def send_whatsapp_message(to, text):
    url = f"https://graph.facebook.com/v22.0/{PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WA_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": text}
    }

    resp = requests.post(url, json=data, headers=headers)
    print("WhatsApp API response:", resp.status_code, resp.text)


# =========================
# Helper: get price from TwelveData
# =========================
def get_price_from_twelvedata(symbol: str):
    symbol = symbol.upper().strip()

    if not API_KEY:
        print("ERROR: Missing TwelveData API_KEY in .env")
        return None

    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        print("TwelveData response:", data)

        # Expected example: {"price": "1.0862", "symbol": "EUR/USD"}
        if "price" in data:
            return float(data["price"])

        return None
    except Exception as e:
        print("Error fetching price:", e)
        return None


# =========================
# Webhook endpoint (GET = verify, POST = messages)
# =========================
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        print("GET verification received:", mode, token, challenge)

        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook verified!")
            return challenge, 200
        else:
            print("Webhook verification failed")
            return "Verification failed", 403

    if request.method == "POST":
        # ✅ Incoming WhatsApp message
        data = request.get_json(silent=True)
        print("Incoming webhook JSON:", data)

        try:
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            messages = value.get("messages", [])

            if not messages:
                return jsonify({"status": "no messages"}), 200

            message = messages[0]
            sender = message["from"]  # phone number
            text = message.get("text", {}).get("body", "").strip().upper()

            print(f"Received from {sender}: {text}")

            # Get price for the symbol
            price = get_price_from_twelvedata(text)

            if price is not None:
                reply = f"📈 Latest price for {text}: {price}"
            else:
                reply = (
                    "❌ Unknown or unsupported symbol.\n\n"
                    "Try formats like:\n"
                    "- BTCUSD\n"
                    "- ETHUSD\n"
                    "- XAUUSD (GOLD)\n"
                    "- EURUSD\n"
                    "- AUDUSD\n"
                    "- GBPUSD\n"
                    "- USDJPY\n"
                )

            send_whatsapp_message(sender, reply)

        except Exception as e:
            print("Error handling incoming message:", e)

        return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    # 0.0.0.0 makes it accessible from outside (through cloudflared)
    app.run(host="0.0.0.0", port=5000, debug=False)

