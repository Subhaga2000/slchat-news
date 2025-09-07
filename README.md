# SL Chat News

A **real-time Sri Lanka news aggregator** and Telegram notifier built with **Flask** and **RSS feeds**.  

---

## 🔹 Features

- Fetches latest news from Sri Lankan RSS feeds (e.g., Ada Derana).  
- Displays news in a **user-friendly web interface** with images and links.  
- Sends news updates automatically to **Telegram**.  
- Stores sent news IDs to avoid duplicate notifications.  
- Works with your **local CSS and HTML files** for a custom design.  

---

## 🔹 Demo

Visit the live app: [Replit URL](https://145d8506-104b-4081-8c2b-5162f46c872a-00-1e0gcscf3eh4o.riker.replit.dev/)  

---

## 🔹 Requirements

- Python 3.12+  
- Flask  
- Feedparser  
- Requests  
- python-dotenv  

Install dependencies:

pip install -r requirements.txt

---

## 🔹 Clone the repository:

git clone https://github.com/Subhaga2000/slchat-news.git
cd slchat-news

---

## 🔹Create a .env file in the project root:

TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id

---

## 🔹Run the app:
python app.py



