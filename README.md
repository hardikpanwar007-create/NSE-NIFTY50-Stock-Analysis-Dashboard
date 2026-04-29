# NIFTY50 Stock Analysis Dashboard
**21 Years · 62 Stocks · 18 Sectors · NSE India (2003–2024)**

---

## Project Structure

```
nifty50-analysis/
│
├── nifty50_analysis.py       # Main Python script — data collection + metrics
├── nifty50_analysis.xlsx     # Output Excel file (3 sheets)
│   ├── Stock Metrics         # 62 stocks × 11 financial metrics
│   ├── Correlation           # Long-format correlation matrix
│   └── Price History         # Weekly indexed prices (long format)
├── NIFTY50_Dashboard.pbix    # Power BI dashboard file
└── README.md
```

---

## What This Project Does

1. **Data Collection** - Fetches 21 years of daily adjusted closing prices for 64 NIFTY50 stocks (current + historical constituents) directly from NSE via `yfinance`

2. **Metric Computation** - Computes 9 financial metrics per stock in Python

3. **Excel Export** - Outputs clean structured data across 3 sheets ready for Power BI

4. **Power BI Dashboard** - 4-page interactive dashboard with sector slicers, scatter plots, bar charts, treemaps and a 21-year indexed price history line chart

---

## Financial Metrics Computed

| Metric | Description |
|---|---|
| CAGR (%) | Compound Annual Growth Rate using log returns |
| Annual Volatility (%) | Std dev of daily returns × √252 |
| Sharpe Ratio | (CAGR − 6.5% risk-free rate) / Volatility |
| Coefficient of Variation | Volatility / CAGR — benchmark-free risk metric |
| Positive Days (%) | % of trading days stock closed higher than previous day |
| 52W High Distance (%) | How far current price is below 52-week high |
| 52W Low Distance (%) | How far current price is above 52-week low |
| Avg Daily Volume | Average shares traded per day — liquidity proxy |
| Current Price (₹) | Latest available closing price |

**Risk-free rate used:** 6.5% (Indian 10Y Government Bond yield proxy, 2024)

---

## Key Findings

| | Stock | Value |
|---|---|---|
| Highest CAGR | ADANIENT | 65.65% |
| Best Sharpe Ratio | HAVELLS | 0.85 |
| Average CAGR (all stocks) | - | 23.38% |
| Stocks above 20% CAGR | - | 38 out of 62 |
| Sectors covered | - | 18 |

**Best performing sector by avg CAGR:** Conglomerate (43.5%)
**Best performing sector by avg CV:** Consumer (1.03)

---

## Dashboard Pages

**Page 1 — Overview**
KPI cards, sector slicer, avg CAGR by sector bar chart, full stock summary table

**Page 2 — Return Analysis**
CAGR ranked bar chart + risk-return scatter plot (CAGR vs Volatility, colour coded by sector)

**Page 3 — Risk Analysis**
Sharpe ratio ranking, Sharpe vs Volatility scatter, CV treemap, volatility band stacked bar

**Page 4 — Sector Breakdown**
Total sectors, Best & Worst sector analysis, Sector Treemap

---

## Notes

- Data source: NSE via Yahoo Finance (`yfinance`)
- Stocks with more than 80% missing data are automatically dropped
- Prices are forward-filled for minor gaps (trading halts, holidays)
- Price History is resampled to **weekly** frequency to keep file size manageable
- All returns use **adjusted closing prices** (accounts for dividends and splits)

---

## Author

**Hardik Parmar**
[LinkedIn](https://www.linkedin.com/in/hardiksinghparmar) · [GitHub](https://github.com/hardikpanwar007-create)
