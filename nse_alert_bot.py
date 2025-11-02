import yfinance as yf
import time
from telegram import Bot
from datetime import datetime

# ✅ Your Bot Token & Chat ID
BOT_TOKEN = "8098667464:AAEFoceyJSdjuXJiZezoJijd-vTACPS79UM"
CHAT_ID = "6445643551"

bot = Bot(token=BOT_TOKEN)

# ✅ Step 1: Fixed NSE Stocks List (3 + top additions later)
stocks = ["YESBANK.NS", "IDEA.NS", "CANBK.NS"]

def check_stock(stock):
    data = yf.download(stock, period="2d", interval="1d", progress=False)

    if len(data) < 2:
        return None

    latest = float(data["Close"].iloc[-1])
    prev = float(data["Close"].iloc[-2])
    change = ((latest - prev) / prev) * 100

    # ✅ Step 2: Print live checking status in terminal
    print(f"{datetime.now().strftime('%H:%M:%S')} Checking {stock} | Price: ₹{latest:.2f} | Change: {change:.2f}%")

    if abs(change) >= 1:  # ✅ Step 3: Alert only if price moves 1% or more
        direction = "UP 📈" if change > 0 else "DOWN 📉"
        alert = f"🔥 {stock} is {direction} by {change:.2f}%\nCurrent Price: ₹{latest:.2f}"
        return alert
    return None

def start_alerts():
    print("✅ Bot Started – Sending Alerts Every 1 Hour")

    while True:
        for st in stocks:
            alert_msg = check_stock(st)
            if alert_msg:
                # ✅ Step 4: Send Telegram Message
                bot.send_message(chat_id=CHAT_ID, text=alert_msg)
                print("✅ Alert sent:", alert_msg)

        print("⏳ Waiting 1 Hour for next update...")
        time.sleep(3600)  # 1 hour

start_alerts()