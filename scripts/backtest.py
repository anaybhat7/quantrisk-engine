import pandas as pd
import numpy as np
from data.fetcher import DataFetcher
from data.preprocessor import DataPreprocessor
from engine.estimators import RiskEstimator
import matplotlib.pyplot as plt

def run_backtest(tickers, weights, confidence_level=0.95, window=252):
    """
    Backtests the Historical VaR model over the past year.
    """
    # 1. Fetch 2 years of data (enough for a 1-year window + 1-year backtest)
    fetcher = DataFetcher()
    raw_data = fetcher.fetch_stock_prices(tickers)
    
    preprocessor = DataPreprocessor()
    returns = preprocessor.get_risk_ready_data(raw_data)
    
    portfolio_rets = returns.dot(weights)
    
    # 2. Setup Backtest Loop
    # We start after 'window' days and predict VaR for the next day
    results = []
    actual_returns = portfolio_rets.iloc[window:]
    
    print(f"Starting Backtest for {len(actual_returns)} days...")
    
    for i in range(window, len(portfolio_rets)):
        # Lookback window for the model
        lookback_slice = returns.iloc[i-window:i]
        
        # Estimate VaR for 'today' based on the lookback
        estimator = RiskEstimator(lookback_slice, weights)
        h_var = estimator.historical_var(confidence_level)
        
        # The actual return we are comparing against
        actual_ret = portfolio_rets.iloc[i]
        
        # Check for Exception (Loss > VaR)
        # Note: VaR is stored as a positive loss number
        is_exception = 1 if actual_ret < -h_var else 0
        
        results.append({
            'Date': portfolio_rets.index[i],
            'Actual_Return': actual_ret,
            'VaR_Estimate': -h_var,
            'Exception': is_exception
        })

    # 3. Analyze Results
    backtest_df = pd.DataFrame(results).set_index('Date')
    total_exceptions = backtest_df['Exception'].sum()
    failure_rate = total_exceptions / len(backtest_df)
    
    print("-" * 30)
    print(f"Backtest Results ({confidence_level*100}% VaR)")
    print(f"Total Days: {len(backtest_df)}")
    print(f"Exceptions: {total_exceptions}")
    print(f"Failure Rate: {failure_rate:.2%}")
    print(f"Target Rate: {1 - confidence_level:.2%}")
    print("-" * 30)

    # 4. Visualization (Great for your GitHub README)
    plt.figure(figsize=(12, 6))
    plt.plot(backtest_df['Actual_Return'], label='Daily Return', alpha=0.5)
    plt.plot(backtest_df['VaR_Estimate'], label=f'{confidence_level*100}% VaR', color='red', linestyle='--')
    
    # Highlight Exceptions
    exceptions = backtest_df[backtest_df['Exception'] == 1]
    plt.scatter(exceptions.index, exceptions['Actual_Return'], color='black', label='Exception', zorder=5)
    
    plt.title(f"Portfolio VaR Backtest: {', '.join(tickers)}")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Example: A 60/40 Equity/Tech portfolio
    my_tickers = ['SPY', 'QQQ']
    my_weights = [0.6, 0.4]
    run_backtest(my_tickers, my_weights)