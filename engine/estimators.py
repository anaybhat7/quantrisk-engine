import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Union

class RiskEstimator:
    """
    Core engine for calculating Portfolio Value-at-Risk (VaR) and 
    Expected Shortfall (ES).
    """

    def __init__(self, returns: pd.DataFrame, weights: Union[np.array, list]):
        self.returns = returns
        self.weights = np.array(weights)
        
        if len(self.weights) != returns.shape[1]:
            raise ValueError("Weights length must match number of assets in returns DataFrame.")
            
        # Calculate daily portfolio returns
        self.portfolio_returns = self.returns.dot(self.weights)

    def parametric_var(self, confidence_level: float = 0.95) -> float:
        """
        Calculates Parametric VaR using the Variance-Covariance method.
        Assumes normality of returns.
        """
        mu = self.portfolio_returns.mean()
        sigma = self.portfolio_returns.std()
        
        # norm.ppf gives the percent point function (inverse of CDF)
        z_score = norm.ppf(1 - confidence_level)
        
        # VaR as a positive number (loss)
        var_val = -(mu + z_score * sigma)
        return float(var_val)

    def historical_var(self, confidence_level: float = 0.95) -> float:
        """
        Calculates Historical VaR (non-parametric).
        Does not assume any specific distribution.
        """
        # Sort returns and find the quantile
        var_val = -np.percentile(self.portfolio_returns, (1 - confidence_level) * 100)
        return float(var_val)

    def expected_shortfall(self, confidence_level: float = 0.95) -> float:
        """
        Calculates Expected Shortfall (Conditional VaR).
        Average loss in the worst (1 - alpha)% of cases.
        """
        # First, find the historical VaR threshold
        h_var = self.historical_var(confidence_level)
        
        # Filter returns that are worse (lower) than the negative VaR
        tail_losses = self.portfolio_returns[self.portfolio_returns <= -h_var]
        
        # ES is the average of those tail losses (returned as a positive value)
        es_val = -tail_losses.mean()
        return float(es_val)