import matplotlib.pyplot as plt
import pandas


def matplotlib_show(df: pandas.DataFrame, index_name: str, freq: str = "monthly"):
    # 设置图表样式
    plt.style.use('bmh')  # 使用内置的 bmh 样式
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
    fig, ax1 = plt.subplots(figsize=(16, 9))  # 使用16:9的比例更适合显示

    # 绘制指数曲线
    ax1.plot(
        df["Date"],
        df.iloc[:, 1],
        label=f"{index_name}指数",
        color="#2E86C1",  # 使用更柔和的蓝色
        linewidth=2.5,
        linestyle=line_style
    )
    ax1.set_xlabel("日期", fontsize=12, fontweight='bold')
    ax1.set_ylabel(f"{index_name}指数", color="#2E86C1", fontsize=12, fontweight='bold')
    ax1.tick_params(axis="y", labelcolor="#2E86C1", labelsize=10)
    ax1.tick_params(axis="x", labelsize=10, rotation=45)

    # 创建共享x轴的第二个y轴
    ax2 = ax1.twinx()
    colors = df["Rate"].apply(lambda x: "#27AE60" if x > 0 else "#E74C3C")  # 使用更柔和的红绿色
    ax2.bar(
        df["Date"],
        df["Rate"],
        label=f"{title_suffix}变化率",
        color=colors,
        alpha=0.6,
        width=bar_width
    )
    ax2.set_ylabel(f"{title_suffix}变化率 (%)", color="#C0392B", fontsize=12, fontweight='bold')
    ax2.tick_params(axis="y", labelcolor="#C0392B", labelsize=10)

    # 添加统计信息
    avg_rate = df["Rate"].mean()
    max_rate = df["Rate"].max()
    min_rate = df["Rate"].min()
    
    # 添加水平基准线
    ax2.axhline(y=0, color="#95A5A6", linestyle="--", linewidth=1, label="基准线")
    ax2.axhline(y=avg_rate, color="#8E44AD", linestyle=":", linewidth=1.5, label=f"平均 {avg_rate:.2f}%")
    
    # 标记极值点，使用更优雅的标注样式
    max_idx = df["Rate"].idxmax()
    min_idx = df["Rate"].idxmin()
    
    bbox_props = dict(
        boxstyle="round,pad=0.5",
        fc="white",
        ec="gray",
        alpha=0.8
    )
    
    ax2.annotate(
        f"峰值: {max_rate:.2f}%",
        xy=(max_idx, max_rate),
        xytext=(10, 20),
        textcoords="offset points",
        bbox=bbox_props,
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3,rad=0.2",
            color="gray"
        )
    )
    
    ax2.annotate(
        f"谷值: {min_rate:.2f}%",
        xy=(min_idx, min_rate),
        xytext=(10, -30),
        textcoords="offset points",
        bbox=bbox_props,
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3,rad=-0.2",
            color="gray"
        )
    )

    # 设置图表标题
    plt.title(
        f"{index_name}{title_suffix}变化率 (平均: {avg_rate:.2f}%)",
        fontsize=14,
        pad=20,
        fontweight='bold'
    )

    # 添加图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(
        lines1 + lines2,
        labels1 + labels2,
        loc='upper right',
        bbox_to_anchor=(1, 1.15),
        ncol=4,  # 将图例排成一行
        fontsize=10,
        framealpha=0.9
    )

    # 添加网格线
    ax1.grid(True, linestyle="--", alpha=0.2)

    # 设置背景色
    ax1.set_facecolor("#F8F9F9")  # 浅灰色背景
    
    # 自动调整布局
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, bottom=0.15)  # 为标题和x轴标签留出空间

    plt.show()
