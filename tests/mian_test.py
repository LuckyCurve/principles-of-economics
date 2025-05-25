import json

import yfinance as yf

# 获取苹果公司（AAPL）的股票数据
apple = yf.Ticker("AAPL")

info = apple.info

print(json.dumps(info))
