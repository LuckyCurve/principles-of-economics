import matplotlib.pyplot as plt
import pandas


def matplotlib_show(df: pandas.DataFrame, index_name: str, freq: str = "monthly"):
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 指定默认字体为黑体
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示为方块的问题

    df["Date"] = pandas.to_datetime(df["Date"])
    df.index = df["Date"]

    # 根据频率设置不同样式
    if freq == "monthly":
        bar_width = 20
        line_style = "-"
        title_suffix = "月度"
    else:
        bar_width = 5
        line_style = "-"
        title_suffix = "周度"

    # 创建主图和子图
    fig, ax1 = plt.subplots(figsize=(16, 8))  # 调整图表大小

    # 绘制指数
    ax1.plot(
        df["Date"],
        df.iloc[:, 1],
        label=f"{index_name}指数",
        color="navy",
        linewidth=2.5,
        linestyle=line_style
    )
    ax1.set_xlabel("日期", fontsize=12)
    ax1.set_ylabel(f"{index_name}指数", color="navy", fontsize=12)
    ax1.tick_params(axis="y", labelcolor="navy", labelsize=10)
    ax1.tick_params(axis="x", labelsize=10, rotation=45)

    # 创建共享x轴的第二个y轴
    ax2 = ax1.twinx()
    colors = df["Rate"].apply(lambda x: "limegreen" if x > 0 else "tomato")
    ax2.bar(
        df["Date"],
        df["Rate"],
        label=f"{title_suffix}变化率",
        color=colors,
        alpha=0.7,
        width=bar_width
    )
    ax2.set_ylabel(f"{title_suffix}变化率 (%)", color="red", fontsize=12)
    ax2.tick_params(axis="y", labelcolor="red", labelsize=10)

    # 添加统计信息
    avg_rate = df["Rate"].mean()
    max_rate = df["Rate"].max()
    min_rate = df["Rate"].min()
    
    # 添加水平基准线
    ax2.axhline(y=0, color="gray", linestyle="--", linewidth=1, label="基准线")
    ax2.axhline(y=avg_rate, color="purple", linestyle=":", linewidth=1.5, label=f"平均 {avg_rate:.2f}%")
    
    # 标记极值点
    max_idx = df["Rate"].idxmax()
    min_idx = df["Rate"].idxmin()
    ax2.annotate(f"峰值: {max_rate:.2f}%",
                xy=(max_idx, max_rate),
                xytext=(10, 20),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->"))
    ax2.annotate(f"谷值: {min_rate:.2f}%",
                xy=(min_idx, min_rate),
                xytext=(10, -30),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->"))

    # 设置图表标题
    plt.title(f"{index_name}{title_suffix}变化率 (平均: {avg_rate:.2f}%)", fontsize=14, pad=20)

    # 添加图例
    fig.legend(
        loc="upper left",
        bbox_to_anchor=(0.1, 0.95),
        fontsize=10,
        framealpha=0.9
    )

    # 添加网格线
    ax1.grid(True, linestyle="--", alpha=0.3)

    # 自动调整子图参数
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)  # 为x轴标签留出空间

    plt.show()
