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

    # 计算年平均收益率并保存 CSV 文件
    annual_close = nasdaq["Close"].resample("Y").last()
    annual_close["^IXIC"] = annual_close["^IXIC"].round(2)
    annual_close["Rate"] = (
        annual_close.pct_change(fill_method=None).dropna() * 100
    ).round(2)
    annual_close.to_csv(os.path.join(CSV_DIR, "nasdaq_annual_change.csv"))


def main():
    download_to_csv()

    # 加载并展示周度数据
    weekly_df = pandas.read_csv(os.path.join(CSV_DIR, "nasdaq_weekly_change.csv"))
    print("\n纳斯达克指数周度统计:")
    print(f"平均变化率: {weekly_df['Rate'].mean():.2f}%")
    print(f"最大涨幅: {weekly_df['Rate'].max():.2f}%")
    print(f"最大跌幅: {weekly_df['Rate'].min():.2f}%")
    matplotlib_show(weekly_df, "纳斯达克指数", freq="weekly")

    # 加载并展示月度数据
    monthly_df = pandas.read_csv(os.path.join(CSV_DIR, "nasdaq_monthly_change.csv"))
    print("\n纳斯达克指数月度统计:")
    print(f"平均变化率: {monthly_df['Rate'].mean():.2f}%")
    print(f"最大涨幅: {monthly_df['Rate'].max():.2f}%")
    print(f"最大跌幅: {monthly_df['Rate'].min():.2f}%")
    matplotlib_show(monthly_df, "纳斯达克指数", freq="monthly")

    # 加载并展示年度数据
    annually_df = pandas.read_csv(os.path.join(CSV_DIR, "nasdaq_annual_change.csv"))
    print("\n纳斯达克指数年度统计:")
    print(f"平均变化率: {annually_df['Rate'].mean():.2f}%")
    print(f"最大涨幅: {annually_df['Rate'].max():.2f}%")
    print(f"最大跌幅: {annually_df['Rate'].min():.2f}%")
    matplotlib_show(annually_df, "纳斯达克指数", freq="yearly")


if __name__ == "__main__":
    main()
