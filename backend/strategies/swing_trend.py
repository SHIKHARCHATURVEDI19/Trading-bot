import pandas as pd
import pandas_ta as ta

class SwingTrendStrategy:
    def __init__(self, ema_slow=21, ema_fast=9, rsi_period=14, rsi_buy_threshold=40):
        self.ema_slow = ema_slow
        self.ema_fast = ema_fast
        self.rsi_period = rsi_period
        self.rsi_buy_threshold = rsi_buy_threshold

    def apply_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates indicators and appends them to the dataframe.
        """
        # Ensure we have enough data
        if len(df) < self.ema_slow:
            print(f"Warning: Not enough data for {self.ema_slow} EMA calculation.")
            return df
            
        df = df.copy()
        
        # Calculate EMAs
        df.ta.ema(length=self.ema_slow, append=True)
        df.ta.ema(length=self.ema_fast, append=True)
        
        # Calculate RSI
        df.ta.rsi(length=self.rsi_period, append=True)
        
        # Calculate ATR (Average True Range) for stop-loss placing
        df.ta.atr(length=14, append=True)
        
        # Rename columns to standard names for easier access
        ema_slow_col = f'EMA_{self.ema_slow}'
        ema_fast_col = f'EMA_{self.ema_fast}'
        rsi_col = f'RSI_{self.rsi_period}'
        atr_col = 'ATRr_14'
        
        # We need the previous day's RSI to check for the bounce
        df['RSI_prev'] = df[rsi_col].shift(1)
        
        return df

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates buy/sell signals based on Trend Pullback + Momentum rules.
        """
        df = self.apply_indicators(df)
        
        # Define column names based on pandas_ta default generation
        ema_slow_col = f'EMA_{self.ema_slow}'
        ema_fast_col = f'EMA_{self.ema_fast}'
        rsi_col = f'RSI_{self.rsi_period}'
        
        if ema_slow_col not in df.columns:
            return df
            
        df['Signal'] = 0  # 0 = Hold, 1 = Buy, -1 = Sell
        
        # Trend Filter: Price must be above 200 EMA
        is_uptrend = df['close'] > df[ema_slow_col]
        
        # Pullback Trigger: Price is touching or near the 20 EMA
        # Let's say if the low of the candle goes below 20 EMA but close is near it
        pullback = df['low'] <= df[ema_fast_col]
        
        # Momentum Trigger: RSI was below threshold (oversold) and is now pointing up
        rsi_bounce = (df['RSI_prev'] < self.rsi_buy_threshold) & (df[rsi_col] > df['RSI_prev'])
        
        # BUY Logic
        buy_condition = is_uptrend & pullback & rsi_bounce
        df.loc[buy_condition, 'Signal'] = 1
        
        # NOTE: Sell (Exit) signals are handled by the Risk Manager using Stop-Loss and Take-Profit,
        # but we could add a structural sell signal here if the trend breaks.
        trend_break = df['close'] < df[ema_slow_col]
        df.loc[trend_break, 'Signal'] = -1
        
        return df

if __name__ == "__main__":
    print("SwingTrendStrategy initialized. Import to use.")
