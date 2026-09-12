# QuantAlgo Trading Bot 🚀📈

An institutional-grade, fully automated 1-minute scalping stock trading bot built with Python, FastAPI, and a React/TailwindCSS dashboard. It natively integrates with the [Alpaca Markets](https://alpaca.markets) API for zero-commission paper and live trading.

## ✨ Features
* **Autonomous Trading Engine**: Loops every 60 seconds to scan a watchlist of high-liquidity US Equities (AAPL, NVDA, SPY, etc.).
* **Technical Strategy (Scalping)**: Utilizes a custom `pandas_ta` strategy combining the 9 EMA, 21 EMA, and RSI to hunt for high-probability momentum dips.
* **Dynamic Risk Management**: Automatically calculates position sizing based on account equity, and sends Bracket Orders (attaching an ATR-based Stop-Loss and a Risk-to-Reward Take-Profit to every trade).
* **React Web Dashboard**: A dark-mode GUI to monitor your live portfolio value, buying power, and active positions with real-time P&L tracking.
* **Panic Button**: Features an "Emergency Liquidate" kill-switch on the dashboard that instantly closes all open positions and cancels pending orders via the REST API.

## 🛠️ Tech Stack
* **Backend Engine**: Python, `alpaca-py`, `pandas`, `pandas_ta`
* **API Bridge**: FastAPI, Uvicorn
* **Frontend Dashboard**: React, Vite, Tailwind CSS v4, Lucide Icons

---

## 🚀 Quick Start Guide

### 1. Requirements & Setup
Clone the repository and set up a Python virtual environment:
```bash
git clone https://github.com/SHIKHARCHATURVEDI19/Trading-bot.git
cd Trading-bot
python -m venv venv
# Windows: .\venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install fastapi uvicorn alpaca-py pandas pandas_ta python-dotenv
```

### 2. API Keys
Create a `.env` file in the root directory and add your Alpaca Paper Trading API keys:
```env
APCA_API_KEY_ID="PK..."
APCA_API_SECRET_KEY="abc..."
APCA_PAPER_TRADING="True"
```
*(Never commit this file to version control!)*

### 3. Launching the System
You will need three separate terminal windows to run the full stack.

**Terminal 1: Start the AI Strategy Engine**
```bash
python backend/main.py
```

**Terminal 2: Start the FastAPI Server**
```bash
python backend/api_server.py
```

**Terminal 3: Start the React Dashboard**
```bash
cd frontend-react
npm install
npm run dev
```
Navigate to `http://localhost:5173` in your browser to view your trading command center!

---

## ⚠️ Disclaimer
This software is for educational and testing purposes only. Do not use this algorithm with real money unless you fully understand the risks of algorithmic trading and have thoroughly backtested the parameters. The developers assume no responsibility for financial losses incurred.
