import pytest
import pandas as pd
import numpy as np
from engine.attribution import FactorAttributor

def test_risk_contribution_sums_to_vol():
    """
    Mathematical check: The sum of Total Risk Contributions 
    must equal the total Portfolio Volatility.
    """
    np.random.seed(42)
    returns = pd.DataFrame(np.random.normal(0, 0.02, (100, 2)), columns=['A', 'B'])
    weights = np.array([0.5, 0.5])
    
    attributor = FactorAttributor
    risk_df = attributor.calculate_risk_contribution(returns, weights)
    
    port_vol = np.sqrt(weights.T @ returns.cov() @ weights)
    assert np.isclose(risk_df['Risk_Contribution'].sum(), port_vol)

def test_factor_regression_output():
    """
    Verifies that the OLS regression returns a dictionary 
    with expected factor betas and an intercept (alpha).
    """
    np.random.seed(42)
    # Create 100 days of data
    dates = pd.date_range('2023-01-01', periods=100)
    
    # Independent Factors (e.g., Mkt-RF, SMB, HML)
    factors = pd.DataFrame(np.random.normal(0, 0.01, (100, 2)), 
                           index=dates, columns=['Mkt-RF', 'SMB'])
    
    # Portfolio returns as a linear combination of factors + some noise
    # R_p = 0.001 (alpha) + 1.2 * Mkt-RF + 0.5 * SMB + noise
    port_rets = 0.001 + (1.2 * factors['Mkt-RF']) + (0.5 * factors['SMB']) + np.random.normal(0, 0.001, 100)
    port_series = pd.Series(port_rets, index=dates, name='Portfolio')

    from engine.attribution import FactorAttributor
    attributor = FactorAttributor(port_series, factors)
    betas = attributor.perform_factor_regression()

    # Check that we got all factors plus the constant (alpha)
    assert 'const' in betas
    assert 'Mkt-RF' in betas
    assert 'SMB' in betas
    
    # Check that the values are close to our input coefficients
    assert np.isclose(betas['Mkt-RF'], 1.2, atol=0.1)
    assert np.isclose(betas['SMB'], 0.5, atol=0.1)