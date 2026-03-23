import numpy as np
import pandas as pd
from typing import Dict

class StressTester:
    """
    Simulates 'Black Swan' events and Macro Shocks on the portfolio.
    """

    def __init__(self, returns: pd.DataFrame, weights: np.array):
        self.returns = returns
        self.weights = np.array(weights)
        self.portfolio_returns = self.returns.dot(self.weights)

    def apply_macro_shock(self, asset_shocks: Dict[str, float]) -> float:
        """
        Simulates a manual price shock to specific assets.
        Example: {'AAPL': -0.15, 'TSLA': -0.20} (15% and 20% drops)
        """
        # Calculate the impact: Sum of (Weight_i * Shock_i)
        shock_impact = 0
        asset_names = self.returns.columns.tolist()
        
        for asset, shock in asset_shocks.items():
            if asset in asset_names:
                idx = asset_names.index(asset)
                shock_impact += self.weights[idx] * shock
                
        return float(shock_impact)

    def correlation_spike_stress(self, spike_factor: float = 1.5) -> float:
        """
        In a crisis, correlations tend to jump to 1.0. 
        This stresses the Covariance matrix and re-calculates Parametric VaR.
        """
        vcv = self.returns.cov()
        # Scale the off-diagonal elements (covariances)
        stressed_vcv = vcv * spike_factor
        
        # Recalculate portfolio variance
        stressed_var = self.weights.T @ stressed_vcv @ self.weights
        stressed_vol = np.sqrt(stressed_var)
        
        # 95% Confidence VaR (approx 1.65 standard deviations)
        return float(1.65 * stressed_vol)

    def historical_replay(self, scenario: str) -> float:
        """
        Applies returns from famous historical crises to the current weights.
        """
        scenarios = {
            "2020_covid": ("2020-02-20", "2020-03-23"),
            "2008_lehman": ("2008-09-01", "2008-10-31")
        }
        
        if scenario not in scenarios:
            raise ValueError(f"Scenario {scenario} not defined.")
            
        start, end = scenarios[scenario]
        # Note: This requires the DataFetcher to have fetched enough history!
        # For now, we simulate the logic:
        historical_period = self.returns.loc[start:end]
        if historical_period.empty:
            return 0.0
            
        replay_returns = historical_period.dot(self.weights)
        return float(replay_returns.min()) # The worst daily return during that crisis