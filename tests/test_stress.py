import pytest
import pandas as pd
import numpy as np
from engine.stress_tester import StressTester

@pytest.fixture
def stress_data():
    """
    Creates a reproducible 100-day return series for 3 assets.
    """
    np.random.seed(42)
    dates = pd.date_range('2020-01-01', periods=100)
    returns = pd.DataFrame(
        np.random.normal(0, 0.01, (100, 3)),
        index=dates,
        columns=['AAPL', 'MSFT', 'GOOGL']
    )
    weights = np.array([0.4, 0.3, 0.3])
    return returns, weights

def test_apply_macro_shock(stress_data):
    """
    Verifies that a manual price shock correctly scales by asset weights.
    Formula: Impact = Sum(Weight_i * Shock_i)
    """
    returns, weights = stress_data
    tester = StressTester(returns, weights)
    
    # 10% drop in AAPL (Weight 0.4) should result in a 4% portfolio drop
    shocks = {'AAPL': -0.10}
    impact = tester.apply_macro_shock(shocks)
    
    assert np.isclose(impact, -0.04)

def test_correlation_spike_logic(stress_data):
    """
    Ensures that spiking the VCV matrix (correlation) 
    increases the Parametric VaR.
    """
    returns, weights = stress_data
    tester = StressTester(returns, weights)
    
    var_normal = tester.correlation_spike_stress(spike_factor=1.0)
    var_stressed = tester.correlation_spike_stress(spike_factor=2.0)
    
    # Stressed VaR must be higher than normal VaR when volatility is scaled
    assert var_stressed > var_normal

def test_historical_replay_missing_scenario(stress_data):
    """
    Tests error handling for undefined crisis scenarios.
    """
    returns, weights = stress_data
    tester = StressTester(returns, weights)
    
    with pytest.raises(ValueError, match="Scenario unknown_crash not defined"):
        tester.historical_replay("unknown_crash")

def test_historical_replay_functionality(stress_data):
    """
    Verifies that historical replay returns the minimum (worst) 
    portfolio return in the specified window.
    """
    # Create specific 'crash' data for the 2020 COVID window
    returns, weights = stress_data
    # Force a -50% day in the COVID window
    returns.loc['2020-03-16'] = [-0.5, -0.5, -0.5] 
    
    tester = StressTester(returns, weights)
    worst_loss = tester.historical_replay("2020_covid")
    
    # The portfolio loss should be exactly -0.5 since all weights sum to 1
    assert worst_loss == -0.5