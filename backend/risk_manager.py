import math

class RiskManager:
    def __init__(self, risk_per_trade_pct=0.015, atr_sl_multiplier=1.5, rr_ratio=2.0):
        """
        risk_per_trade_pct: Maximum percentage of total account equity to risk on a single trade (e.g., 0.015 for 1.5%)
        atr_sl_multiplier: How many ATRs below entry to place the Stop Loss
        rr_ratio: Reward/Risk ratio for Take Profit (e.g., 2.0 means target 2x the risk)
        """
        self.risk_per_trade_pct = risk_per_trade_pct
        self.atr_sl_multiplier = atr_sl_multiplier
        self.rr_ratio = rr_ratio

    def calculate_position_size(self, account_equity: float, entry_price: float, stop_loss_price: float) -> int:
        """
        Calculates how many shares to buy based on risk limits.
        """
        if entry_price <= stop_loss_price:
            raise ValueError("Stop loss must be below entry price for long positions.")
            
        # Total dollar amount we are willing to lose if SL is hit
        max_dollar_risk = account_equity * self.risk_per_trade_pct
        
        # Risk per share (Dollar difference between entry and SL)
        risk_per_share = entry_price - stop_loss_price
        
        if risk_per_share <= 0:
            return 0
            
        # Number of shares we can afford to lose risk_per_share on
        shares = math.floor(max_dollar_risk / risk_per_share)
        
        # Double check we have enough buying power for the full position
        max_shares_by_equity = math.floor(account_equity / entry_price)
        
        return min(shares, max_shares_by_equity)

    def calculate_trade_parameters(self, entry_price: float, atr_value: float, account_equity: float) -> dict:
        """
        Returns the Stop-Loss, Take-Profit, and Number of Shares for a given trade.
        """
        # Calculate Stop Loss price
        stop_loss = entry_price - (atr_value * self.atr_sl_multiplier)
        
        # Calculate Take Profit price
        risk_amount = entry_price - stop_loss
        take_profit = entry_price + (risk_amount * self.rr_ratio)
        
        # Calculate Shares to buy
        shares = self.calculate_position_size(account_equity, entry_price, stop_loss)
        
        return {
            "entry_price": round(entry_price, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "qty": shares,
            "total_cost": round(shares * entry_price, 2)
        }

if __name__ == "__main__":
    rm = RiskManager(risk_per_trade_pct=0.015, atr_sl_multiplier=1.5, rr_ratio=2.0)
    # Example: $10,000 account, stock is $150, ATR is $3.50
    trade = rm.calculate_trade_parameters(entry_price=150.0, atr_value=3.50, account_equity=10000.0)
    print("Example Trade Setup:", trade)
