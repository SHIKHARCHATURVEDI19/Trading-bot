import os
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import DataFeed as AlpacaDataFeed

load_dotenv()

API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")

class DataFeed:
    def __init__(self):
        if not API_KEY or not API_SECRET:
            raise ValueError("Missing API keys for Alpaca Data Client")
        
        # Data client doesn't need paper=True, market data is universal
        self.client = StockHistoricalDataClient(API_KEY, API_SECRET)

    def get_historical_bars(self, symbol: str, days_back: int = 2, timeframe: TimeFrame = TimeFrame.Minute) -> pd.DataFrame:
        """
        Fetches historical OHLCV data for a specific symbol.
        """
        # Free data tier has a 15-minute delay on SIP data.
        end_time = datetime.now() - timedelta(minutes=20)
        # Fetch less days back since Minute data is much denser
        start_time = end_time - timedelta(days=days_back)

        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=timeframe,
            start=start_time,
            end=end_time,
            feed=AlpacaDataFeed.IEX  # REQUIRED for free tier accounts!
        )

        print(f"Fetching {timeframe} data for {symbol} from {start_time.date()} to {end_time.date()}...")
        bars = self.client.get_stock_bars(request_params)
        
        # Convert to pandas dataframe
        df = bars.df
        
        if df.empty:
            print(f"No data found for {symbol}.")
            return df
            
        # The dataframe returned by alpaca has a multi-index (symbol, timestamp)
        # We drop the symbol index to make it easier to work with for a single stock
        if isinstance(df.index, pd.MultiIndex):
            df = df.reset_index(level=0, drop=True)
            
        # Ensure index is sorted chronologically
        df = df.sort_index()
        
        print(f"Successfully loaded {len(df)} candles.")
        return df

if __name__ == "__main__":
    # Simple test
    feed = DataFeed()
    try:
        # Fetching 1-hour candles for Apple over the last 14 days
        df = feed.get_historical_bars("AAPL", days_back=14, timeframe=TimeFrame.Hour)
        print(df.tail())
    except Exception as e:
        print(f"Error fetching data: {e}")
        print("Make sure your API keys are set in the .env file.")
