import yfinance as yf
import pandas as pd
import numpy as np


def fetch_and_prepare_data(ticker: str):
    """
    Downloads 5 years of daily OHLCV data for the given ticker using yfinance,
    computes technical indicators (RSI, MACD histogram, MA ratio, Volume change)
    using pure pandas, generates next-day directional labels, and returns the
    most recent 350 valid samples.
    """
    clean_ticker = ticker.strip().upper()
    if not clean_ticker:
        raise ValueError("Ticker symbol cannot be empty.")

    try:
        stock = yf.Ticker(clean_ticker)
        df = stock.history(period="5y", interval="1d", auto_adjust=True)
    except Exception as e:
        raise RuntimeError(f"Network or yfinance error while fetching '{clean_ticker}': {str(e)}")

    if df is None or df.empty:
        raise ValueError(
            f"No historical price data found for ticker '{clean_ticker}'. "
            "Please verify the ticker symbol is valid and delisted symbols are avoided."
        )

    # Flatten MultiIndex columns if returned by newer yfinance versions
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    required_cols = {"Close", "Volume"}
    if not required_cols.issubset(set(df.columns)):
        raise ValueError(f"Missing required OHLCV columns (Close, Volume) for '{clean_ticker}'.")

    df = df[["Close", "Volume"]].copy()
    df.dropna(inplace=True)

    # 1. RSI (14-day) computed with pure pandas (Wilder's / simple rolling average)
    delta = df["Close"].diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    avg_gain = gain.rolling(window=14, min_periods=14).mean()
    avg_loss = loss.rolling(window=14, min_periods=14).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["rsi_14"] = 100.0 - (100.0 / (1.0 + rs))
    df["rsi_14"] = df["rsi_14"].fillna(50.0)

    # 2. MACD histogram: (EMA12 - EMA26) minus 9-day EMA signal line
    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    df["macd_hist"] = macd_line - signal_line

    # 3. Moving average ratio = Close / SMA(20)
    sma20 = df["Close"].rolling(window=20, min_periods=20).mean()
    df["ma_ratio"] = df["Close"] / sma20

    # 4. Volume change = daily percent change in Volume
    df["vol_change"] = df["Volume"].pct_change()
    df["vol_change"] = df["vol_change"].replace([np.inf, -np.inf], np.nan)

    # 5. Label: 1 if next day's Close > today's Close, else 0
    df["next_close"] = df["Close"].shift(-1)
    df.dropna(subset=["rsi_14", "macd_hist", "ma_ratio", "vol_change", "next_close"], inplace=True)

    df["label"] = (df["next_close"] > df["Close"]).astype(int)

    # Keep the most recent 350 rows chronologically
    if len(df) < 350:
        raise ValueError(
            f"Ticker '{clean_ticker}' only has {len(df)} valid trading days after indicator calculation. "
            "At least 350 valid rows are required (250 train + 100 test)."
        )

    df_recent = df.iloc[-350:].copy()
    return df_recent
