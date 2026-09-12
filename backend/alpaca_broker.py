import os
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus

# Load environment variables
load_dotenv()

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")
PAPER_TRADING = os.getenv("APCA_PAPER_TRADING", "False").lower() == "true"

def get_trading_client() -> TradingClient:
    """Initializes and returns the Alpaca Trading Client"""
    if not API_KEY or not API_SECRET:
        raise ValueError("Missing APCA_API_KEY_ID or APCA_API_SECRET_KEY in .env file")
    
    # paper=False implies Live Trading Money
    client = TradingClient(API_KEY, API_SECRET, paper=PAPER_TRADING)
    return client

def test_connection():
    """Fetches account info to verify keys and connection without executing trades."""
    print("--- DRY RUN & CONNECTION TEST ---")
    print(f"Mode: {'PAPER (Simulation)' if PAPER_TRADING else 'LIVE MONEY'}")
    
    try:
        client = get_trading_client()
        account = client.get_account()
        
        print("\n[SUCCESS] Connected to Alpaca!")
        print(f"Account ID: {account.id}")
        print(f"Account Status: {account.status}")
        print(f"Total Portfolio Value: ${account.portfolio_value}")
        print(f"Cash Buying Power: ${account.buying_power}")
        
        # Check if the account is blocked from trading
        if account.trading_blocked:
            print("[WARNING] Trading is blocked on this account!")
            
    except Exception as e:
        print(f"\n[ERROR] Failed to connect to Alpaca: {e}")
        print("Please check your .env file keys and ensure your Alpaca account is approved for Live Trading.")

if __name__ == "__main__":
    test_connection()
