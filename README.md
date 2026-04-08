# QuantRisk-Engine: Multi-Asset Risk & Stress-Testing Library
Final Project for ORIE 5270: Big Data Technologies.

---

## 1. Purpose of Project
**QuantRisk-Engine** is a professional-grade Python library built for the decomposition, estimation, and validation of market risk. While traditional models often treat risk as a static number, this engine provides a dynamic framework for **Risk Budgeting** and **Tail-Risk Analysis**.

### Core Functionalities:
* **Dynamic Risk Estimation:** Implementation of Parametric $VaR$, Historical $VaR$, and Expected Shortfall ($ES$) to capture non-normal "fat-tail" distributions.
* **Factor Attribution:** Calculation of **Marginal Contribution to Risk (MCTR)** to identify specific assets driving portfolio volatility.
* **Stress-Testing Engine:** Scenario analysis simulating historical "Black Swan" events (2008 Financial Crisis, 2020 COVID-19 Crash) and manual macro shocks.
* **Model Validation:** A rolling-window backtesting suite to verify the statistical integrity of risk forecasts.

---

## 2. Dataset & Big Data Tech Stack
To satisfy the ORIE 5270 "Real Dataset" requirement, the engine integrates:
* **Market Data:** Live ingestion of $N$-asset price series via the `yfinance` API.
* **Macro Indicators:** Integration with the **FRED (Federal Reserve Economic Data) API** to pull interest rate and inflation factors for stress testing.
* **Storage Efficiency:** Uses **Apache Parquet** for local data caching. Parquet’s columnar storage format allows the engine to handle 1,000+ day backtests with minimal I/O latency.
* **Statistical Libraries:** Uses `statsmodels` for OLS-based factor regressions and `scipy.stats` for distribution modeling.

---

## 3. Mathematical Methodology
The engine relies on three core mathematical pillars:

### Value-at-Risk ($VaR$) & Expected Shortfall ($ES$)
We estimate the maximum expected loss over a 1-day horizon at a confidence level $\alpha$:
$$VaR_{\alpha} = \mu_p - z_{\alpha} \sigma_p$$
Expected Shortfall addresses the "average loss" in the tail beyond the $VaR$ threshold:
$$ES_{\alpha} = E[L \mid L > VaR_{\alpha}]$$

### Marginal Contribution to Risk (MCTR)
Determines the sensitivity of the total portfolio volatility to a marginal change in an asset's weight (e.g., adding $1 to a specific position):
$$MCTR_i = \frac{\partial \sigma_p}{\partial w_i} = \frac{(\Sigma w)_i}{\sigma_p}$$
*(Where $\Sigma$ is the covariance matrix, $w$ is the weight vector, and $\sigma_p$ is the portfolio volatility).*


---

## 4. Installation & Reproducibility
This project is structured as a standard Python package. To reproduce the environment and results:

```bash
# 1. Clone & Enter Directory
git clone https://github.com/anaybhat/quantrisk-engine.git
cd quantrisk-engine

# 2. Environment Setup
python3 -m venv .venv
source .venv/bin/activate

# 3. Install Package & Dependencies
pip install -e ".[dev]"
```

---

## 5. Usage & Execution
### Running Tests (High Coverage)
The engine maintains **99% unit-test coverage**, verifying math logic, API failure handling, and dimension alignment.
```bash
python -m pytest --cov=engine tests/
```

### Running the Backtest Script
To generate a 1,000-day historical validation of a multi-asset portfolio:
```bash
python -m scripts.backtest
```

---

## 6. Interpreting the Backtest Results
The provided `backtest.py` script generates a performance visualization and a statistical summary.



### Graph Interpretation:
* **The Blue Line (Daily Returns):** Represents the realized daily PnL of the portfolio.
* **The Red Dashed Line ($VaR$ Envelope):** This is the "Risk Floor." Notice how it jumps during high-volatility periods (e.g., late 2024). This shows the model is adapting to new volatility regimes.
* **Black Dots (Exceptions):** These occur when the actual loss exceeds the $VaR$ estimate.

### Statistical Analysis (Results: 5.77% vs 5.00% Target)
In our 1,057-day test of a Tech-heavy portfolio, we observed a **5.77% failure rate**.
1.  **Basel Traffic Light Test:** According to Basel III/IV standards, a 5.77% rate for a 95% $VaR$ over ~1,000 days falls comfortably within the **"Green Zone."** 2.  **Model Robustness:** The clustering of exceptions during market "regime shifts" suggests that while the model is statistically valid, it is reactive. A $VaR$ model that fails "too little" (e.g., 1%) is actually poorly calibrated as it overestimates risk and traps capital.
3.  **Conclusion:** The engine is accurately capturing market dynamics and provides a reliable floor for capital adequacy requirements.

---

## 7. Clean File Structure
```text
quantrisk-engine/
├── data/           # API Ingestion & Parquet Caching
├── engine/         # Math Logic (VaR, ES, MCTR, Stress-Testing)
├── scripts/        # End-to-end Backtesting & Reporting
├── tests/          # Unit-Testing Suite (>80% coverage)
├── utils/          # Formatting & Helpers
├── setup.py        # Package Installation Configuration
└── .env            # Secure API Key Storage
```




