from alpaca_broker import get_trading_client
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

def force_test_trade():
    print("Executing Forced Test Trade...")
    client = get_trading_client()
    
    order_data = MarketOrderRequest(
        symbol="AAPL",
        qty=1,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )
    
    try:
        submitted_order = client.submit_order(order_data)
        print(f"✅ Success! Bought 1 share of AAPL.")
        print(f"Order ID: {submitted_order.id}")
        print("Check your React Dashboard in ~10 seconds to see the position appear!")
    except Exception as e:
        print(f"❌ Failed to place test trade: {e}")

if __name__ == "__main__":
    force_test_trade()
