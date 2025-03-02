import matplotlib.pyplot as plt
import pandas

if __name__ == "__main__":
    df = pandas.read_csv("sp500.csv", index_col=0).iloc[2:]
    df.index = pandas.to_datetime(df.index)
    df = df.loc[df.index[(df.index.day == 1) & (df.index.month % 3 == 0)]]
    df["changeRate"] = df["Close"].astype(float).pct_change().mul(100).round(2)
    print(df.tail(20))

    # 提取横纵轴数据
    x = df.index  # 日期索引
    y = df.iloc[:, -1]  # 最后一列数据

    # 创建画布与绘图
    plt.figure(figsize=(10, 6))  # 设置画布大小（网页5推荐比例）
    plt.plot(
        x,
        y,
        color="#2E86C1",  # 自定义颜色（网页3、网页4的配色方案）
        linestyle="--",
        marker="o",
        markersize=8,
        linewidth=2,
        label="增长率",
    )

    # 添加图表元素
    plt.title("时间序列增长率趋势", fontsize=14, pad=20)  # 标题与间距
    plt.xlabel("日期", fontsize=12)
    plt.ylabel("增长率 (%)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)  # 网格线（网页2的样式）
    plt.legend()

    # 解决中文显示问题（网页4、网页6的方案）
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    # 显示图表
    plt.tight_layout()
    plt.show()
