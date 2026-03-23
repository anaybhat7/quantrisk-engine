import os
import yfinance as yf
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from fredapi import Fred
import logging

# Load environment variables from .env
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    """
    Ingests market and macro data with local Parquet caching.
    """
    
    def __init__(self):
        self.fred_key = os.getenv("FRED_API_KEY")
        self.cache_dir = Path(os.getenv("DATA_CACHE_DIR", "./data/parquet_cache"))
        self.start_date = os.getenv("START_DATE", "2021-01-01")
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.fred_key:
            logger.warning("FRED_API_KEY not found in .env. Macro data will be unavailable.")

    def fetch_stock_prices(self, tickers: list, use_cache: bool = True) -> pd.DataFrame:
        """
        Fetches stock data. Checks local Parquet cache first.
        """
        cache_path = self.cache_dir / "equity_prices.parquet"
        
        if use_cache and cache_path.exists():
            logger.info("Loading equity data from local Parquet cache...")
            return pd.read_parquet(cache_path)

        logger.info(f"Fetching fresh data for: {tickers}")
        try:
            # We add auto_adjust=True to make 'Close' the adjusted price
            raw_data = yf.download(tickers, start=self.start_date, progress=False, auto_adjust=True)
            
            if raw_data.empty:
                raise ValueError("No data returned from Yahoo Finance. Check your tickers and start_date.")

            # With auto_adjust=True, 'Close' is our adjusted price
            data = raw_data['Close']
            
            # Big Data move: Save to Parquet
            data.to_parquet(cache_path)
            return data
        except Exception as e:
            logger.error(f"Failed to fetch Yahoo Finance data: {e}")
            raise

    def fetch_macro_factors(self, series_ids: list) -> pd.DataFrame:
        """
        Fetches macro indicators (e.g., 'T10Y2Y' for yield curve) from FRED.
        """
        if not self.fred_key:
            raise ValueError("FRED API Key is required for macro data.")
            
        fred = Fred(api_key=self.fred_key)
        macro_data = {}
        
        for s_id in series_ids:
            logger.info(f"Fetching {s_id} from FRED...")
            macro_data[s_id] = fred.get_series(s_id, observation_start=self.start_date)
            
        df = pd.DataFrame(macro_data)
        # Save macro data separately
        df.to_parquet(self.cache_dir / "macro_factors.parquet")
        return df