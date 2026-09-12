from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from alpaca_broker import get_trading_client
import uvicorn

app = FastAPI(title="Trading Bot API")

# Allow frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
def get_status():
    try:
        client = get_trading_client()
        account = client.get_account()
        return {
            "status": "online",
            "account_id": account.id,
            "mode": "paper",
            "equity": float(account.equity),
            "buying_power": float(account.buying_power),
            "day_trade_count": account.daytrade_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/positions")
def get_positions():
    try:
        client = get_trading_client()
        positions = client.get_all_positions()
        
        result = []
        for p in positions:
            result.append({
                "symbol": p.symbol,
                "qty": float(p.qty),
                "market_value": float(p.market_value),
                "avg_entry_price": float(p.avg_entry_price),
                "current_price": float(p.current_price),
                "unrealized_pl": float(p.unrealized_pl),
                "unrealized_plpc": float(p.unrealized_plpc) * 100  # Percentage
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/emergency_kill")
def emergency_kill():
    """
    Panic button: Closes all open positions and cancels all open orders instantly.
    """
    try:
        client = get_trading_client()
        # Cancel all open orders (stop losses, take profits, pending buys)
        cancel_statuses = client.cancel_orders()
        # Liquidate all open positions at market price
        close_statuses = client.close_all_positions(cancel_orders=True)
        return {"status": "success", "message": "All positions liquidated and orders cancelled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting API Server on port 8000...")
    uvicorn.run("api_server:app", host="127.0.0.1", port=8000, reload=True)
