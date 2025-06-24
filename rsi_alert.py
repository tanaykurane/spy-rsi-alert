import yfinance as yf
import smtplib
from email.mime.text import MIMEText
from ta.momentum import RSIIndicator
import os

# --- Config ---
SPY_TICKER = "SPY"
RSI_THRESHOLD = 30
EMAIL_SENDER = os.environ["EMAIL_SENDER"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_RECIPIENT = os.environ["EMAIL_RECIPIENT"]

def send_email_alert(rsi):
    msg = MIMEText(f"🚨 RSI Alert: SPY RSI is {rsi:.2f} (below {RSI_THRESHOLD})")
    msg["Subject"] = "SPY RSI Alert"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECIPIENT

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("Email sent.")

def check_rsi():
    df = yf.download(SPY_TICKER, period="2mo", interval="1d")
    df.dropna(inplace=True)
    rsi = RSIIndicator(close=df['Close']).rsi().iloc[-1]
    print(f"RSI: {rsi:.2f}")

    if rsi < RSI_THRESHOLD:
        send_email_alert(rsi)

# Run it
check_rsi()
