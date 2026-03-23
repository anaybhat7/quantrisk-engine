import pytest
import pandas as pd
import numpy as np
from engine.estimators import RiskEstimator

@pytest.fixture
def sample_portfolio_data():
    """
    Creates a synthetic returns DataFrame and weights for testing.
    Using a fixed seed ensures reproducibility.
    """
    np.random.seed(42)
    dates = pd.date_range('2023-01-01', periods=100)
    # Generate random normal returns for 3 assets
    returns = pd.DataFrame(
        np.random.normal(0.001, 0.02, (100, 3)),
        index=dates,
        columns=['AAPL', 'GOOGL', 'TSLA']
    )
    weights = [0.4, 0.3, 0.3]
    return returns, weights

def test_initialization_error(sample_portfolio_data):
    """
    Test that the estimator raises ValueError if weights don't match assets.
    """
    returns, _ = sample_portfolio_data
    wrong_weights = [0.5, 0.5] # Only 2 weights for 3 assets
    
    with pytest.raises(ValueError, match="Weights length must match"):
        RiskEstimator(returns, wrong_weights)

def test_var_consistency(sample_portfolio_data):
    """
    Fundamental Risk Logic: VaR at 99% must be greater than VaR at 95%.
    """
    returns, weights = sample_portfolio_data
    estimator = RiskEstimator(returns, weights)
    
    var_95 = estimator.parametric_var(0.95)
    var_99 = estimator.parametric_var(0.99)
    
    assert var_99 > var_95
    assert var_95 > 0  # Assuming standard volatile market data

def test_expected_shortfall_property(sample_portfolio_data):
    """
    Mathematical Logic: Expected Shortfall must be strictly greater than VaR.
    $$ES_{\alpha} > VaR_{\alpha}$$
    """
    returns, weights = sample_portfolio_data
    estimator = RiskEstimator(returns, weights)
    
    alpha = 0.95
    var = estimator.historical_var(alpha)
    es = estimator.expected_shortfall(alpha)
    
    assert es > var

def test_historical_var_calculation(sample_portfolio_data):
    """
    Test historical VaR against a manual numpy calculation.
    """
    returns, weights = sample_portfolio_data
    estimator = RiskEstimator(returns, weights)
    
    # Manual calculation
    port_rets = returns.dot(weights)
    manual_var = -np.percentile(port_rets, 5) # 5th percentile for 95% CL
    
    assert np.isclose(estimator.historical_var(0.95), manual_var)