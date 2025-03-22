import matplotlib.pyplot as plt
import pandas


def matplotlib_show(df: pandas.DataFrame, index_name: str):
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 指定默认字体为黑体
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示为方块的问题

    df["Date"] = pandas.to_datetime(df["Date"])
    df.index = df["Date"]

    # 创建主图和子图
    fig, ax1 = plt.subplots(figsize=(14, 7))  # 调整图表大小

    # 绘制指数
    ax1.plot(
        df["Date"], df.iloc[:, 1], label=index_name, color="blue", linewidth=2
    )  # 增加线条宽度
    ax1.set_xlabel("日期", fontsize=12)  # 设置字体大小
    ax1.set_ylabel(index_name, color="blue", fontsize=12)
    ax1.tick_params(axis="y", labelcolor="blue", labelsize=10)  # 设置刻度标签大小
    ax1.tick_params(axis="x", labelsize=10)

    # 创建共享x轴的第二个y轴
    ax2 = ax1.twinx()
    colors = df["Rate"].apply(lambda x: "green" if x > 0 else "red")
    ax2.bar(df["Date"], df["Rate"], label="变化率", color=colors, alpha=0.6, width=8)
    ax2.set_ylabel("变化率 (%)", color="red", fontsize=12)
    ax2.tick_params(axis="y", labelcolor="red", labelsize=10)

    # 添加水平基准线
    ax2.axhline(y=0, color="gray", linestyle="--", linewidth=1, label="基准线")

    # 设置图表标题
    plt.title(f"{index_name}变化率", fontsize=14)

    # 添加图例
    fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.95), fontsize=10)

    # 添加网格线
    ax1.grid(True, linestyle="--", alpha=0.5)

    # 自动调整子图参数, 使之填充整个图像区域
    plt.tight_layout()

    plt.show()
