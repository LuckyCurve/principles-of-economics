import datetime
import os
import time

import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup


# --- 获取纳斯达克 100 成分股列表 ---
def get_nasdaq100_tickers():
    """从维基百科获取纳斯达克 100 成分股列表"""
    print("正在从维基百科获取纳斯达克 100 成分股列表...")
    try:
        url = "https://en.wikipedia.org/wiki/Nasdaq-100"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"id": "constituents"})
        tickers = []
        for row in table.find_all("tr")[1:]:  # 跳过表头
            ticker = row.find_all("td")[
                1
            ].text.strip()  # 纳斯达克表格中股票代码在第二列
            # yfinance 有时需要将 . 替换为 - (例如 BRK.B -> BRK-B)
            ticker = ticker.replace(".", "-")
            tickers.append(ticker)
        print(f"成功获取 {len(tickers)} 个纳斯达克 100 成分股代码。")
        return tickers
    except requests.exceptions.RequestException as e:
        print(f"获取维基百科页面失败: {e}")
        return None
    except Exception as e:
        print(f"解析维基百科页面时出错: {e}")
        return None


# --- 获取股票数据 ---
def get_stock_data(tickers):
    """使用 yfinance 获取股票的市值和市盈率"""
    print(f"正在获取 {len(tickers)} 支股票的市值和市盈率数据...")
    data = []
    batch_size = 50  # 分批获取以避免请求过多
    processed_count = 0
    valid_data_count = 0
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i : i + batch_size]
        try:
            # 一次性获取一批股票的信息
            yf_tickers = yf.Tickers(batch)
            # yf_tickers.tickers 是一个字典 {TICKER: yf.Ticker object}
            for ticker_symbol, ticker_obj in yf_tickers.tickers.items():
                try:
                    # 尝试访问 .info 属性，如果股票代码无效或数据不可用，可能会抛出异常或返回空字典
                    info = ticker_obj.info
                    market_cap = info.get("marketCap")
                    pe_ratio = info.get("forwardPE")  # 使用追踪市盈率

                    # 检查数据有效性
                    if (
                        market_cap is not None
                        and market_cap > 0
                        and pe_ratio is not None
                        and pe_ratio > 0
                    ):
                        data.append(
                            {
                                "Ticker": ticker_symbol,
                                "MarketCap": market_cap,
                                "PE": pe_ratio,
                            }
                        )
                        valid_data_count += 1

                except Exception:
                    # 处理获取单个 ticker info 可能出现的错误 (例如无效的 ticker)
                    pass  # 静默处理获取单个 Ticker 失败的情况

            processed_count += len(batch)
            print(
                f"已处理 {processed_count}/{len(tickers)}... 当前有效数据 {valid_data_count} 条"
            )
            time.sleep(1)  # 短暂暂停，避免过于频繁请求

        except Exception as e:
            print(f"获取批次 {batch} 数据时出错: {e}")
            processed_count += len(batch)  # 即使失败也更新计数器
            print(f"已处理 {processed_count}/{len(tickers)}...")

    print(f"成功获取 {len(data)} 支有效股票的数据。")
    return pd.DataFrame(data)


# --- 计算市值加权平均市盈率 ---
def calculate_weighted_pe(df):
    """计算市值加权平均市盈率"""
    if df.empty or "MarketCap" not in df.columns or "PE" not in df.columns:
        print("数据框为空或缺少必要的列，无法计算。")
        return None, 0  # 返回 None 和 总市值 0

    total_market_cap = df["MarketCap"].sum()
    if total_market_cap == 0:
        print("总市值为零，无法计算加权市盈率。")
        return None, 0  # 返回 None 和 总市值 0

    df["WeightedPE"] = (df["MarketCap"] / total_market_cap) * df["PE"]
    weighted_average_pe = df["WeightedPE"].sum()
    return weighted_average_pe, total_market_cap  # 返回计算结果和总市值


# --- 主函数 ---
def main():
    tickers = get_nasdaq100_tickers()
    if not tickers:
        print("无法获取成分股列表，程序退出。")
        return

    stock_data_df = get_stock_data(tickers)
    if stock_data_df.empty:
        print("未能获取任何有效的股票数据，程序退出。")
        return

    weighted_pe, total_market_cap = calculate_weighted_pe(stock_data_df)  # 接收总市值

    if weighted_pe is not None:
        print("\n--- 计算结果 ---")
        print(f"纳斯达克 100 成分股数量 (获取到有效数据): {len(stock_data_df)}")
        print(f"总市值 (基于有效数据): ${total_market_cap:,.0f}")  # 格式化总市值
        print(f"市值加权平均市盈率 (Forward PE): {weighted_pe:.2f}")

        # --- 将结果保存到 CSV ---
        try:
            output_csv = "data/csv/nasdaq100_weighted_pe_history.csv"
            today_date = datetime.date.today().strftime("%Y-%m-%d")
            # 将市盈率格式化为保留两位小数的字符串再保存
            new_data = pd.DataFrame(
                {"日期": [today_date], "当年市盈率": [f"{weighted_pe:.2f}"]}
            )

            if os.path.exists(output_csv):
                # 文件存在，追加数据，不写表头
                new_data.to_csv(
                    output_csv,
                    mode="a",
                    header=False,
                    index=False,
                    encoding="utf-8-sig",
                )
                print(f"\n结果已追加保存到 {output_csv}")
            else:
                # 文件不存在，创建文件，写表头
                new_data.to_csv(
                    output_csv, mode="w", header=True, index=False, encoding="utf-8-sig"
                )
                print(f"\n结果已保存到新的文件 {output_csv}")

        except Exception as e:
            print(f"\n保存 CSV 文件时出错: {e}")

    else:
        print("\n未能计算出有效的市值加权平均市盈率。")


if __name__ == "__main__":
    main()
