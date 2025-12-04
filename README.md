# whatsapp-forex-bot


# WhatsApp Forex Bot (Python + Meta Cloud API)

A fully automated WhatsApp chatbot built using Python and the WhatsApp Cloud API.  
It processes incoming WhatsApp messages, responds with real-time forex information  
(BTC/USD, market updates), and is deployed on Render using a Flask backend.

## ✨ Features
- Instant WhatsApp replies using Meta Cloud API
- Forex price lookup (BTCUSD)
- Flask webhook server for message handling
- Deployed using Render (free tier)
- Extendable logic for more commands or AI responses

## 🧱 Tech Stack
- Python 3
- Flask
- Gunicorn
- Render Hosting
- Meta WhatsApp Cloud API
- TwelveData / Binance price API

## 🚀 Deployment
1. Create a WhatsApp App in Meta Developers
2. Get `WHATSAPP_TOKEN`, `PHONE_NUMBER_ID`, and `VERIFY_TOKEN`
3. Deploy Flask app on Render
4. Add Render webhook URL in Meta console
5. Subscribe to "messages"
6. Test by messaging the WhatsApp test number

## 📬 How It Works
User → WhatsApp → Meta API → Flask webhook  
Flask → API call → Reply → WhatsApp → User

## 📚 Future Enhancements
- Add more currency pairs
- Add AI responses using ChatGPT API
- Support message templates
- Full trading dashboard integration
