import os

import matplotlib.pyplot as plt
import pandas
import yfinance as yf

# 统一的CSV文件目录
CSV_DIR = "data/csv"


def download_to_csv_monthly():
    """下载恒生指数数据并统计"""
    # 下载恒生指数数据
    hsi = yf.download("^HSI", auto_adjust=True)

    # 按月重采样并计算变化率
    monthly_close = hsi["Close"].resample("ME").last()
    monthly_close["^HSI"] = monthly_close["^HSI"].round(2)
    monthly_close["Rate"] = (monthly_close.pct_change().dropna() * 100).round(2)

    # 保存到统一目录
    os.makedirs(CSV_DIR, exist_ok=True)
    monthly_close.to_csv(os.path.join(CSV_DIR, "hsi_monthly_change.csv"))


def download_to_csv_weekly():
    """下载恒生指数数据并统计"""
    # 下载恒生指数数据
    hsi = yf.download("^HSI", auto_adjust=True)

    # 按周重采样并计算变化率
    weekly_close = hsi["Close"].resample("W").last()
    weekly_close["^HSI"] = weekly_close["^HSI"].round(2)
    weekly_close["Rate"] = (weekly_close.pct_change().dropna() * 100).round(2)

    # 保存到统一目录
    os.makedirs(CSV_DIR, exist_ok=True)
    weekly_close.to_csv(os.path.join(CSV_DIR, "hsi_weekly_change.csv"))


def matplotlib_show(df: pandas.DataFrame):
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 指定默认字体为黑体
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示为方块的问题

    df["Date"] = pandas.to_datetime(df["Date"])
    df.index = df["Date"]

    # 创建主图和子图
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 绘制恒生指数
    ax1.plot(df["Date"], df["^HSI"], label="恒生指数", color="blue")
    ax1.set_xlabel("日期")
    ax1.set_ylabel("恒生指数", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # 创建共享x轴的第二个y轴
    ax2 = ax1.twinx()
    ax2.plot(df["Date"], df["Rate"], label="变化率", color="red")
    ax2.set_ylabel("变化率 (%)", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # 添加水平基准线
    ax2.axhline(y=0, color="gray", linestyle="--", linewidth=1, label="基准线")

    # 设置图表标题
    plt.title("恒生指数变化率")

    # 添加图例
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95))

    # 添加网格线
    ax1.grid(True, linestyle="--", alpha=0.5)

    # 自动调整子图参数, 使之填充整个图像区域
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    download_to_csv_monthly()
    download_to_csv_weekly()
    matplotlib_show(pandas.read_csv(os.path.join(CSV_DIR, "hsi_weekly_change.csv")))
    matplotlib_show(pandas.read_csv(os.path.join(CSV_DIR, "hsi_monthly_change.csv")))
