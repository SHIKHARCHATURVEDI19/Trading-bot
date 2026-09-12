import time
from alpaca_broker import get_trading_client
from data_feed import DataFeed
from strategies.swing_trend import SwingTrendStrategy
from risk_manager import RiskManager
from alpaca.data.timeframe import TimeFrame
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass

# Watchlist of highly liquid US stocks
WATCHLIST = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMD"]

def run_trading_cycle():
    print("\n--- Starting 1-Minute Scalping Bot ---")
    
    # 1. Initialize Modules
    client = get_trading_client()
    feed = DataFeed()
    strategy = SwingTrendStrategy(ema_slow=21, ema_fast=9, rsi_period=14, rsi_buy_threshold=40)
    risk_mgr = RiskManager(risk_per_trade_pct=0.01, atr_sl_multiplier=1.0, rr_ratio=1.5)
    
    while True:
        print(f"\n[{time.strftime('%X')}] --- Running Scan ---")
        try:
            # 2. Get Account Info
            account = client.get_account()
            equity = float(account.equity)
            buying_power = float(account.buying_power)
            
            # 3. Get currently open positions
            open_positions = {p.symbol: p for p in client.get_all_positions()}
            print(f"Open positions: {list(open_positions.keys())}")
            
            # 4. Scan the Watchlist
            for symbol in WATCHLIST:
                if symbol in open_positions:
                    continue
                    
                # Fetch 1-minute data
                df = feed.get_historical_bars(symbol, days_back=2, timeframe=TimeFrame.Minute)
                if df.empty or len(df) < 30:
                    continue
                    
                df_signals = strategy.generate_signals(df)
                latest = df_signals.iloc[-1]
                
                print(f"[{symbol}] Close: ${latest['close']:.2f} | EMA21: ${latest.get('EMA_21', 0):.2f} | RSI: {latest.get('RSI_14', 0):.2f}")
                
                if latest['Signal'] == 1:
                    print(f"*** BUY SIGNAL TRIGGERED for {symbol} ***")
                    
                    entry_price = latest['close']
                    atr_value = latest['ATRr_14']
                    
                    trade_params = risk_mgr.calculate_trade_parameters(entry_price, atr_value, equity)
                    qty = trade_params['qty']
                    if qty <= 0:
                        continue
                        
                    print(f"Placing Bracket Order: Buy {qty} @ MKT | SL: ${trade_params['stop_loss']:.2f} | TP: ${trade_params['take_profit']:.2f}")
                    
                    order_data = MarketOrderRequest(
                        symbol=symbol, qty=qty, side=OrderSide.BUY,
                        time_in_force=TimeInForce.GTC, order_class=OrderClass.BRACKET,
                        take_profit=TakeProfitRequest(limit_price=trade_params['take_profit']),
                        stop_loss=StopLossRequest(stop_price=trade_params['stop_loss'])
                    )
                    
                    client.submit_order(order_data)
                    print(f"Order Submitted!")
                    
        except Exception as e:
            print(f"Error in cycle: {e}")
            
        print("Sleeping for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    run_trading_cycle()
