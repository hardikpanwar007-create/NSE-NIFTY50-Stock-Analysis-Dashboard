import yfinance as yf
import pandas as pd
import numpy as np
 
tickers = [
    "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS",
    "HINDUNILVR.NS","ITC.NS","SBIN.NS","BAJFINANCE.NS","MARUTI.NS",
    "WIPRO.NS","LT.NS","AXISBANK.NS","ASIANPAINT.NS","TITAN.NS",
    "SUNPHARMA.NS","TECHM.NS","ULTRACEMCO.NS","NESTLEIND.NS","HCLTECH.NS",
    "POWERGRID.NS","NTPC.NS","TATASTEEL.NS","KOTAKBANK.NS",
    "BAJAJFINSV.NS","ADANIPORTS.NS","ONGC.NS","COALINDIA.NS","JSWSTEEL.NS",
    "DRREDDY.NS","DIVISLAB.NS","CIPLA.NS","BRITANNIA.NS","APOLLOHOSP.NS",
    "EICHERMOT.NS","HEROMOTOCO.NS","INDUSINDBK.NS","BPCL.NS","IOC.NS",
    "GRASIM.NS","HINDALCO.NS","VEDL.NS","SHREECEM.NS","ADANIENT.NS",
    "TATACONSUM.NS","BAJAJ-AUTO.NS","GODREJCP.NS","MCDHOLDING.NS","UPL.NS",
    "HDFCLIFE.NS","SBILIFE.NS","BHARTIARTL.NS","M&M.NS","PIDILITIND.NS",
    "DMART.NS","LTIM.NS","HAVELLS.NS","NAUKRI.NS","COFORGE.NS",
    "TRENT.NS","JIOFIN.NS","SHRIRAMFIN.NS","MOTHERSON.NS"]


print(f"\n{len(tickers)} tickers defined")

SECTOR_MAP = {
    "RELIANCE.NS": "Energy",
    "TCS.NS": "IT",
    "INFY.NS": "IT",
    "HDFCBANK.NS": "Banking",
    "ICICIBANK.NS": "Banking",
    "HINDUNILVR.NS": "FMCG",
    "ITC.NS": "FMCG",
    "SBIN.NS": "Banking",
    "BAJFINANCE.NS": "NBFC",
    "MARUTI.NS": "Auto",
    "WIPRO.NS": "IT",
    "LT.NS": "Infra",
    "AXISBANK.NS": "Banking",
    "ASIANPAINT.NS": "Consumer",
    "TITAN.NS": "Consumer",
    "SUNPHARMA.NS": "Pharma",
    "TECHM.NS": "IT",
    "ULTRACEMCO.NS": "Cement",
    "NESTLEIND.NS": "FMCG",
    "HCLTECH.NS": "IT",
    "POWERGRID.NS": "Utilities",
    "NTPC.NS": "Utilities",
    "TATASTEEL.NS": "Metals",
    "KOTAKBANK.NS": "Banking",
    "BAJAJFINSV.NS": "NBFC",
    "ADANIPORTS.NS": "Infra",
    "ONGC.NS": "Energy",
    "COALINDIA.NS": "Energy",
    "JSWSTEEL.NS": "Metals",
    "DRREDDY.NS": "Pharma",
    "DIVISLAB.NS": "Pharma",
    "CIPLA.NS": "Pharma",
    "BRITANNIA.NS": "FMCG",
    "APOLLOHOSP.NS": "Healthcare",
    "EICHERMOT.NS": "Auto",
    "HEROMOTOCO.NS": "Auto",
    "INDUSINDBK.NS": "Banking",
    "BPCL.NS": "Energy",
    "IOC.NS": "Energy",
    "GRASIM.NS": "Conglomerate",
    "HINDALCO.NS": "Metals",
    "VEDL.NS": "Metals",
    "SHREECEM.NS": "Cement",
    "ADANIENT.NS": "Conglomerate",
    "TATACONSUM.NS": "FMCG",
    "BAJAJ-AUTO.NS": "Auto",
    "GODREJCP.NS": "FMCG",
    "MCDHOLDING.NS": "NBFC",
    "UPL.NS": "Chemicals",
    "HDFCLIFE.NS": "Insurance",
    "SBILIFE.NS": "Insurance",
    "BHARTIARTL.NS": "Telecom",
    "M&M.NS": "Auto",
    "PIDILITIND.NS": "Chemicals",
    "DMART.NS": "Retail",
    "LTIM.NS": "IT",
    "HAVELLS.NS": "Consumer",
    "NAUKRI.NS": "IT",
    "COFORGE.NS": "IT",
    "TRENT.NS": "Retail",
    "JIOFIN.NS": "NBFC",
    "SHRIRAMFIN.NS": "NBFC",
    "MOTHERSON.NS": "Auto"}

print(f"{len(SECTOR_MAP)} sector mappings defined")

data = yf.download(tickers=tickers,start="2003-01-01",end="2024-12-31",auto_adjust=True,progress=True)["Close"]
data_volume = yf.download(tickers=tickers, start="2003-01-01", end="2024-12-31", auto_adjust=True, progress=True)["Volume"]

data.columns = [col for col in data.columns]
data_volume.columns = [col for col in data_volume.columns]

print(f"\n shape: {data.shape} (rows=trading days, cols=stocks)")

threshold = 0.8
missing_per = data.isnull().mean()
to_drop = missing_per[missing_per > threshold].index.tolist()
if to_drop:
    print(f"Dropping {len(to_drop)} stocks with >80% missing: {to_drop}")
    data = data.drop(columns=to_drop) 

prices = data.ffill()
prices = prices.dropna(how="all")

print(f"  Clean data shape: {prices.shape}")
print(f"  Stocks retained: {prices.shape[1]}")
print(f"  Date range: {prices.index[0].date()} to {prices.index[-1].date()}")

per_returns = prices.pct_change().dropna(how="all")
log_returns = np.log(prices / prices.shift(1)).dropna(how="all")

print(f"  Returns shape: {per_returns.shape}")

TRADING_DAYS = 252
RISK_FREE    = 0.065   

metrics_list = []

for ticker in prices.columns:
    col_prices  = prices[ticker].dropna()
    col_returns = per_returns[ticker].dropna()
    col_log     = log_returns[ticker].dropna()

    if len(col_returns) < 252:
        continue

    annual_return = (np.exp(col_log.mean() * TRADING_DAYS) - 1) * 100
    annual_vol    = col_returns.std() * np.sqrt(TRADING_DAYS) * 100
    sharpe        = (annual_return / 100 - RISK_FREE) / (annual_vol / 100)
    cv            = (annual_vol / annual_return) if annual_return > 0 else None
    positive_days = (col_returns > 0).sum() / len(col_returns) * 100

    last_252       = col_prices.iloc[-252:] if len(col_prices) >= 252 else col_prices
    high_52w       = last_252.max()
    low_52w        = last_252.min()
    current        = col_prices.iloc[-1]
    dist_from_high = ((current - high_52w) / high_52w) * 100
    dist_from_low  = ((current - low_52w)  / low_52w)  * 100

    try:
        avg_volume = int(data_volume[ticker].dropna().mean())
    except:
        avg_volume = None

    metrics_list.append({
        "Ticker":                ticker.replace(".NS", ""),
        "Sector":                SECTOR_MAP.get(ticker, "Other"),
        "Current Price (Rs)":    round(current, 2),
        "CAGR (%)":              round(annual_return, 2),
        "Annual Volatility (%)": round(annual_vol, 2),
        "Sharpe Ratio":          round(sharpe, 3),
        "Coeff of Variation":    round(cv, 3) if cv else None,
        "Positive Days (%)":     round(positive_days, 2),
        "52W High Dist (%)":     round(dist_from_high, 2),
        "52W Low Dist (%)":      round(dist_from_low, 2),
        "Avg Daily Volume":      avg_volume,})

metrics_df = pd.DataFrame(metrics_list)
metrics_df = metrics_df.sort_values("CAGR (%)", ascending=False).reset_index(drop=True)

print(f"  Metrics computed for {len(metrics_df)} stocks")
print(f"\n  Top 5 by CAGR:")
print(metrics_df[["Ticker", "Sector", "CAGR (%)", "Sharpe Ratio", "Coeff of Variation", "Positive Days (%)"]].head().to_string(index=False))

for ticker in prices.columns:
    col_returns = per_returns[ticker].dropna()
    print(ticker, len(col_returns))

clean_names = {t: t.replace(".NS", "") for t in per_returns.columns}
corr_matrix = per_returns.rename(columns=clean_names).corr().round(3)

corr_long = corr_matrix.stack().reset_index()
corr_long.columns = ["Stock A", "Stock B", "Correlation"]
corr_long = corr_long[corr_long["Stock A"] != corr_long["Stock B"]]

print(f"  Correlation pairs: {len(corr_long)}")

prices_weekly = prices.rename(columns=clean_names).resample("W").last()

prices_long = prices_weekly.reset_index().melt(
    id_vars="Date",
    var_name="Ticker",
    value_name="Price"
).dropna()

prices_long = prices_long.sort_values(["Ticker", "Date"])
prices_long["First Price"] = prices_long.groupby("Ticker")["Price"].transform("first")
prices_long["Indexed Price"] = (prices_long["Price"] / prices_long["First Price"] * 100).round(2)
prices_long = prices_long.drop(columns="First Price")
prices_long["Price"] = prices_long["Price"].round(2)

sector_lookup = metrics_df.set_index("Ticker")["Sector"]
prices_long["Sector"] = prices_long["Ticker"].map(sector_lookup)

print(f"  Rows: {len(prices_long):,}")


OUTPUT_FILE = "nifty50_analysis.xlsx"

with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
    metrics_df.to_excel(writer, sheet_name="Stock Metrics", index=False)
    corr_long.to_excel(writer, sheet_name="Correlation", index=False)
    prices_long.to_excel(writer, sheet_name="Price History", index=False)

import os
print(f"File saved at: {os.path.abspath(OUTPUT_FILE)}")

prices.to_csv("nifty50_prices_daily.csv")