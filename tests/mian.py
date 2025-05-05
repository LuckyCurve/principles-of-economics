import os

import pandas

# 统一的CSV文件目录
CSV_DIR = "data/csv"


def nasdaq_calculate_earn_rate(month: int) -> float:
    monthly_df = pandas.read_csv(os.path.join(CSV_DIR, "nasdaq_monthly_change.csv"))
    number = (10000 / (monthly_df.tail(month)["^IXIC"] * (1 - 0.0015 + 0.0062))).sum()
    last_gspc_value = monthly_df.tail(1)["^IXIC"].values[0]
    return (last_gspc_value * number - month * 10000) / (month * 10000)


def sp500_calculate_earn_rate(month: int) -> float:
    monthly_df = pandas.read_csv(os.path.join(CSV_DIR, "sp500_monthly_change.csv"))
    number = (10000 / (monthly_df.tail(month)["^GSPC"]) * (1 - 0.0002 + 0.0134)).sum()
    last_gspc_value = monthly_df.tail(1)["^GSPC"].values[0]
    return (last_gspc_value * number - month * 10000) / (month * 10000)


if __name__ == "__main__":
    for i in range(1, 121):
        print(
            f"res {i}: {round(sp500_calculate_earn_rate(i) * 100, 3)}% \t\t\t\t {round(nasdaq_calculate_earn_rate(i) * 100, 3)}%"
        )
