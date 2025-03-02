import yfinance as yf

if __name__ == "__main__":
    sp500 = yf.download("^GSPC", interval="1d")
    sp500.to_csv("sp500.csv")
