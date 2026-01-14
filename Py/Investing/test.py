import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load ETF Data
# -----------------------------
tickers = ["VTI", "VXUS", "SCHD", "QQQM", "SGOV"]

data = yf.download(tickers, start="2011-01-01")["Adj Close"].dropna()
returns = data.pct_change().dropna()

# -----------------------------
# Portfolio Allocations
# -----------------------------
p1 = np.array([0.30, 0.10, 0.22, 0.28, 0.10])  # Your portfolio
p2 = np.array([0.20, 0.00, 0.10, 0.60, 0.10])  # Max Growth 2.0
p3 = np.array([0.35, 0.00, 0.30, 0.15, 0.20])  # Sharpe King

allocs = {
    "Portfolio 1 – Yours": p1,
    "Portfolio 2 – Max Growth": p2,
    "Portfolio 3 – Sharpe King": p3,
}

# -----------------------------
# Portfolio Performance Function
# -----------------------------
def compute_portfolio(returns, weights):
    weighted = returns.mul(weights, axis=1).sum(axis=1)
    cum_growth = (1 + weighted).cumprod()
    return weighted, cum_growth

# Build cumulative return series
portfolio_curves = {}
for name, weights in allocs.items():
    weighted, curve = compute_portfolio(returns, weights)
    portfolio_curves[name] = curve

curves_df = pd.DataFrame(portfolio_curves)

# -----------------------------
# Performance Statistics
# -----------------------------
def stats(weights):
    pr = (returns * weights).sum(axis=1)
    cagr = (1 + pr).prod() ** (252 / len(pr)) - 1
    vol = pr.std() * np.sqrt(252)
    sharpe = cagr / vol
    max_dd = (1 + pr).cumprod().div((1 + pr).cumprod().cummax()).min() - 1
    final_val = (1 + pr).cumprod()[-1] * 10000
    return [cagr, vol, sharpe, max_dd, final_val]

stats_df = pd.DataFrame(
    [stats(w) for w in allocs.values()],
    index=allocs.keys(),
    columns=["CAGR", "Volatility", "Sharpe", "Max Drawdown", "Final $10k"]
)

print("PERFORMANCE STATISTICS:")
print(stats_df)
print("\n")

# -----------------------------
# 🎯 1. Growth Curve Chart
# -----------------------------
plt.figure(figsize=(12, 6))
for col in curves_df.columns:
    plt.plot(curves_df.index, curves_df[col], label=col)

plt.title("Portfolio Growth Comparison (2011–2025)")
plt.xlabel("Year")
plt.ylabel("Growth of $1")
plt.legend()
plt.grid()
plt.show()

# -----------------------------
# 🎯 2. Rolling 3-Year Returns
# -----------------------------
rolling_df = returns.rolling(756).sum()

plt.figure(figsize=(12, 6))
for name, weights in allocs.items():
    port = (returns * weights).sum(axis=1)
    roll = (1 + port).rolling(756).apply(np.prod, raw=True) - 1
    plt.plot(roll.index, roll, label=name)

plt.title("Rolling 3-Year Returns")
plt.xlabel("Year")
plt.ylabel("Return (%)")
plt.legend()
plt.grid()
plt.show()

# -----------------------------
# 🎯 3. Drawdown Chart
# -----------------------------
plt.figure(figsize=(12, 6))
for name, weights in allocs.items():
    pr = (returns * weights).sum(axis=1)
    cum = (1 + pr).cumprod()
    dd = cum / cum.cummax() - 1
    plt.plot(dd.index, dd, label=name)

plt.title("Portfolio Drawdowns")
plt.xlabel("Year")
plt.ylabel("Drawdown (%)")
plt.legend()
plt.grid()
plt.show()

# -----------------------------
# 🎯 4. Risk Contribution
# -----------------------------
def risk_contribution(weights):
    cov = returns.cov() * 252
    portfolio_vol = np.sqrt(weights.T @ cov @ weights)
    marginal = cov @ weights
    contribution = weights * marginal / portfolio_vol
    return contribution

risk_df = pd.DataFrame(
    [risk_contribution(w) for w in allocs.values()],
    index=allocs.keys(),
    columns=tickers
)

print("RISK CONTRIBUTION TO VOLATILITY:")
print(risk_df)