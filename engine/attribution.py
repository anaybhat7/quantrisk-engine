import pandas as pd
import numpy as np
import statsmodels.api as sm
from typing import Dict

class FactorAttributor:
    """
    Analyzes portfolio risk drivers using Linear Regression and 
    Marginal Contribution to Risk (MCTR).
    """

    def __init__(self, portfolio_returns: pd.Series, factor_returns: pd.DataFrame):
        self.port_rets = portfolio_returns
        self.factors = factor_returns
        
        # Ensure dates align perfectly for regression
        combined = pd.concat([self.port_rets, self.factors], axis=1).dropna()
        self.y = combined.iloc[:, 0]
        self.X = combined.iloc[:, 1:]

    def perform_factor_regression(self) -> Dict[str, float]:
        """
        Runs an OLS regression to find Alpha and Factor Betas.
        """
        X_const = sm.add_constant(self.X)
        model = sm.OLS(self.y, X_const).fit()
        
        return model.params.to_dict()

    @staticmethod
    def calculate_risk_contribution(returns: pd.DataFrame, weights: np.array) -> pd.DataFrame:
        """
        Calculates MCTR and Percentage Contribution to Risk for each asset.
        """
        weights = np.array(weights)
        vcv = returns.cov()
        
        # Portfolio Volatility
        port_vol = np.sqrt(weights.T @ vcv @ weights)
        
        # Marginal Contribution to Risk (MCTR)
        mctr = (vcv @ weights) / port_vol
        
        # Total Risk Contribution (TRC)
        trc = weights * mctr
        
        # Percentage Contribution to Risk (PCR)
        pcr = trc / port_vol
        
        risk_df = pd.DataFrame({
            'Weight': weights,
            'MCTR': mctr,
            'Risk_Contribution': trc,
            'Pct_Contribution': pcr
        }, index=returns.columns)
        
        return risk_df