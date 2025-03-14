import os

import pandas
import yfinance as yf

from utils import matplotlib_show  # Add this import

# 统一的CSV文件目录
CSV_DIR = "data/csv"


def download_to_csv():
    """下载纳斯达克指数数据并统计"""
    # 下载纳斯达克指数数据
    nasdaq = yf.download("^IXIC", auto_adjust=True)

    # 按月重采样并计算变化率
    monthly_close = nasdaq["Close"].resample("ME").last()
    monthly_close["^IXIC"] = monthly_close["^IXIC"].round(2)
    monthly_close["Rate"] = (
        monthly_close.pct_change(fill_method=None).dropna() * 100
    ).round(2)

    # 保存到CSV文件
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)
    monthly_close.to_csv(os.path.join(CSV_DIR, "nasdaq_monthly_change.csv"))

    # 按周重采样并计算变化率
    weekly_close = nasdaq["Close"].resample("W").last()
    weekly_close["^IXIC"] = weekly_close["^IXIC"].round(2)
    weekly_close["Rate"] = (
        weekly_close.pct_change(fill_method=None).dropna() * 100
    ).round(2)

    # 保存到CSV文件
    weekly_close.to_csv(os.path.join(CSV_DIR, "nasdaq_weekly_change.csv"))


if __name__ == "__main__":
    download_to_csv()
    matplotlib_show(
        pandas.read_csv(os.path.join(CSV_DIR, "nasdaq_monthly_change.csv")),
        "纳斯达克指数",
    )
    matplotlib_show(
        pandas.read_csv(os.path.join(CSV_DIR, "nasdaq_weekly_change.csv")),
        "纳斯达克指数",
    )
    matplotlib_show(
        pandas.read_csv(os.path.join(CSV_DIR, "nasdaq_monthly_change.csv")),
        "纳斯达克指数",
    )
    matplotlib_show(
        pandas.read_csv(os.path.join(CSV_DIR, "nasdaq_weekly_change.csv")),
        "纳斯达克指数",
    )
