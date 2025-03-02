import matplotlib.pyplot as plt
import pandas
import yfinance as yf


def download_to_csv():
    """下载标普500数据并统计"""
    # 下载标普500数据
    # sp500 = yf.download("^GSPC", start="2000-01-01")
    sp500 = yf.download("^GSPC")

    # 按月重采样并计算变化率
    monthly_close = sp500["Close"].resample("ME").last()
    monthly_close["^GSPC"] = monthly_close["^GSPC"].round(2)
    monthly_close["Rate"] = (monthly_close.pct_change().dropna() * 100).round(2)

    monthly_close.to_csv("sp500_monthly_change.csv")


def matplotlib_show():
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 指定默认字体为黑体
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示为方块的问题

    df = pandas.read_csv("sp500_monthly_change.csv")
    df["Date"] = pandas.to_datetime(df["Date"])
    df.index = df["Date"]
    df.plot(x="Date", y="^GSPC")
    ax = df.plot(x="Date", y="Rate")
    ax.axhline(y=0, color="r", linestyle="--", linewidth=2, label="基准线")
    ax.legend()
    plt.show()


matplotlib_show()
