import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas
from matplotlib.ticker import FuncFormatter


def matplotlib_show(df: pandas.DataFrame, index_name: str, freq: str = "monthly"):
    """
    增强版金融数据可视化函数

    Args:
        df: 包含日期、指数值和变化率的DataFrame
        index_name: 指数名称
        freq: 频率，'monthly'或'weekly'
    """
    # 设置更现代的图表样式
    plt.style.use("seaborn-v0_8-darkgrid")  # 使用更现代的seaborn样式

    # 设置中文字体
    plt.rcParams["font.sans-serif"] = [
        "SimHei",
        "Microsoft YaHei",
        "SimSun",
        "Arial Unicode MS",
    ]
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
    plt.rcParams["font.size"] = 11  # 默认字体大小
    plt.rcParams["axes.titlesize"] = 14  # 标题字体大小
    plt.rcParams["axes.labelsize"] = 12  # 轴标签字体大小

    # 确保日期格式正确
    df["Date"] = pandas.to_datetime(df["Date"])
    df.index = df["Date"]

    # 显示数据点数量信息
    data_points = len(df)
    print(f"正在可视化 {data_points} 个数据点...")

    # 根据频率设置不同样式
    # 使用数据点数量动态调整柱状图宽度

    if freq == "monthly":
        # 动态调整柱宽，避免柱子过多过密
        if data_points > 120:  # 超过10年的月度数据
            bar_width = 15
        elif data_points > 60:  # 5-10年
            bar_width = 20
        else:  # 少于5年
            bar_width = 25

        line_style = "-"
        title_suffix = "月度"
        date_fmt_long = mdates.DateFormatter("%Y-%m")
        date_fmt_short = mdates.DateFormatter("%m")
        locator = mdates.MonthLocator()
    else:  # 周度或其他粒度
        # 动态调整柱宽，避免柱子过多过密
        if data_points > 500:  # 超过10年的周度数据
            bar_width = 2
        elif data_points > 250:  # 5-10年
            bar_width = 3
        elif data_points > 100:  # 2-5年
            bar_width = 4
        else:  # 少于2年
            bar_width = 5

        line_style = "-"
        title_suffix = "周度"
        date_fmt_long = mdates.DateFormatter("%m-%d")
        date_fmt_short = mdates.DateFormatter("%d")
        locator = mdates.WeekdayLocator()

    # 创建主图和子图 - 使用更现代的比例和DPI设置
    fig, ax1 = plt.subplots(figsize=(16, 9), dpi=100, facecolor="#FAFAFA")

    # 设置图表整体风格
    fig.patch.set_facecolor("#FAFAFA")  # 设置图表背景色

    # 绘制指数曲线 - 使用更现代的颜色和样式
    line_color = "#1A5276"  # 更深的蓝色
    ax1.plot(
        df["Date"],
        df.iloc[:, 1],
        label=f"{index_name}指数",
        color=line_color,
        linewidth=2.5,
        linestyle=line_style,
        alpha=0.9,
        zorder=5,  # 确保线在最上层
    )

    # 添加指数值的范围区域
    min_val = df.iloc[:, 1].min()
    max_val = df.iloc[:, 1].max()
    ax1.fill_between(
        df["Date"], min_val, df.iloc[:, 1], color=line_color, alpha=0.1, zorder=1
    )

    # 设置坐标轴标签
    ax1.set_xlabel("日期", fontsize=12, fontweight="bold")
    ax1.set_ylabel(
        f"{index_name}指数", color=line_color, fontsize=12, fontweight="bold"
    )
    ax1.tick_params(axis="y", labelcolor=line_color, labelsize=10)

    # 格式化y轴数值显示（添加千位分隔符）
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))

    # 自适应日期格式化 - 优化刻度生成逻辑，避免生成过多刻度
    min_date = df["Date"].min()
    max_date = df["Date"].max()
    date_range = max_date - min_date

    # 根据数据范围智能选择刻度间隔
    if date_range > datetime.timedelta(days=365 * 10):  # 超过10年
        ax1.xaxis.set_major_locator(mdates.YearLocator(base=5))  # 每5年一个刻度
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax1.xaxis.set_minor_locator(mdates.YearLocator())  # 每年一个次要刻度
    elif date_range > datetime.timedelta(days=365 * 5):  # 5-10年
        ax1.xaxis.set_major_locator(mdates.YearLocator(base=2))  # 每2年一个刻度
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax1.xaxis.set_minor_locator(mdates.YearLocator())  # 每年一个次要刻度
    elif date_range > datetime.timedelta(days=365 * 2):  # 2-5年
        ax1.xaxis.set_major_locator(mdates.YearLocator())  # 每年一个刻度
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        # 不设置次要刻度，避免过多
    elif date_range > datetime.timedelta(days=365):  # 1-2年
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # 每季度一个刻度
        ax1.xaxis.set_major_formatter(date_fmt_long)
    elif date_range > datetime.timedelta(days=180):  # 6个月-1年
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # 每2个月一个刻度
        ax1.xaxis.set_major_formatter(date_fmt_long)
    elif date_range > datetime.timedelta(days=90):  # 3-6个月
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # 每月一个刻度
        ax1.xaxis.set_major_formatter(date_fmt_long)
    else:  # 少于3个月
        # 计算合适的周间隔
        weeks = date_range.days // 7
        interval = max(1, weeks // 10)  # 最多显示约10个刻度
        ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=interval))
        ax1.xaxis.set_major_formatter(date_fmt_short)

    fig.autofmt_xdate()  # 自动格式化日期标签
    ax1.tick_params(axis="x", labelsize=10)

    # 创建共享x轴的第二个y轴
    ax2 = ax1.twinx()

    # 使用更精细的颜色映射来表示变化率
    def get_color(x):
        if x > 5:  # 大幅上涨
            return "#1E8449"  # 深绿色
        elif x > 0:  # 小幅上涨
            return "#58D68D"  # 浅绿色
        elif x > -5:  # 小幅下跌
            return "#F1948A"  # 浅红色
        else:  # 大幅下跌
            return "#C0392B"  # 深红色

    colors = df["Rate"].apply(get_color)

    # 绘制变化率柱状图
    bars = ax2.bar(
        df["Date"],
        df["Rate"],
        label=f"{title_suffix}变化率",
        color=colors,
        alpha=0.75,
        width=bar_width,
        zorder=2,
    )

    # 设置第二个y轴的标签
    rate_color = "#922B21"  # 变化率标签颜色
    ax2.set_ylabel(
        f"{title_suffix}变化率 (%)", color=rate_color, fontsize=12, fontweight="bold"
    )
    ax2.tick_params(axis="y", labelcolor=rate_color, labelsize=10)

    # 计算统计信息
    avg_rate = df["Rate"].mean()
    max_rate = df["Rate"].max()
    min_rate = df["Rate"].min()
    positive_pct = (df["Rate"] > 0).mean() * 100  # 正收益百分比

    # 添加水平基准线和平均线
    ax2.axhline(
        y=0, color="#95A5A6", linestyle="-", linewidth=1, alpha=0.7, label="基准线"
    )
    ax2.axhline(
        y=avg_rate,
        color="#8E44AD",
        linestyle=":",
        linewidth=1.5,
        alpha=0.8,
        label=f"平均 {avg_rate:.2f}%",
    )

    # 添加智能标注
    max_idx = df["Rate"].idxmax()
    min_idx = df["Rate"].idxmin()

    # 获取最大值和最小值的日期字符串
    max_date_str = max_idx.strftime("%Y-%m-%d")
    min_date_str = min_idx.strftime("%Y-%m-%d")

    texts = []
    texts.append(
        ax2.text(
            max_idx,
            max_rate * 1.05,
            f"峰值: {max_rate:.2f}%\n{max_date_str}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
        )
    )
    texts.append(
        ax2.text(
            min_idx,
            min_rate * 1.05,
            f"谷值: {min_rate:.2f}%\n{min_date_str}",
            ha="center",
            va="top",
            fontsize=9,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
        )
    )

    # 设置图表标题 - 添加更多统计信息
    plt.title(
        f"{index_name}{title_suffix}变化率分析\n"
        f"平均: {avg_rate:.2f}% | 正收益比例: {positive_pct:.1f}% | 波动范围: [{min_rate:.2f}%, {max_rate:.2f}%]",
        fontsize=14,
        pad=20,
        fontweight="bold",
    )

    # 添加图例 - 改进布局
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    # 创建自定义图例项，显示统计信息
    from matplotlib.lines import Line2D

    custom_lines = [
        Line2D(
            [0], [0], color="white", marker="o", markerfacecolor="#58D68D", markersize=8
        ),
        Line2D(
            [0], [0], color="white", marker="o", markerfacecolor="#C0392B", markersize=8
        ),
    ]
    custom_labels = [
        f"上涨期数: {(df['Rate'] > 0).sum()} ({positive_pct:.1f}%)",
        f"下跌期数: {(df['Rate'] < 0).sum()} ({100 - positive_pct:.1f}%)",
    ]

    # 合并所有图例项
    ax2.legend(
        lines1 + lines2 + custom_lines,
        labels1 + labels2 + custom_labels,
        loc="upper right",
        bbox_to_anchor=(1, 1.15),
        ncol=3,  # 使用固定列数使图例更整洁
        fontsize=10,
        framealpha=0.9,
        fancybox=True,  # 圆角边框
        shadow=True,  # 添加阴影
    )

    # 添加网格线 - 使用更细的线条
    ax1.grid(True, linestyle="--", alpha=0.2, axis="both")

    # 设置y轴范围，确保有足够空间显示标注
    y2_min, y2_max = ax2.get_ylim()
    ax2.set_ylim(y2_min * 1.1, y2_max * 1.1)

    # 添加数据来源和时间戳
    plt.figtext(
        0.01,
        0.01,
        f"数据来源: Yahoo Finance | 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        fontsize=8,
        color="gray",
    )

    # 自动调整布局和标注
    plt.tight_layout()

    # 修复 FancyArrowPatch 警告 - 使用更简单的标注方式
    # 移除之前的文本标注
    for text in texts:
        text.remove()

    # 使用 annotate 替代 text + adjust_text
    ax2.annotate(
        f"峰值: {max_rate:.2f}%\n{max_date_str}",
        xy=(max_idx, max_rate),
        xytext=(max_idx, max_rate * 1.15),  # 文本位置上移
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3,rad=0.2",
            color="gray",
            shrinkA=0,
            shrinkB=5,
            lw=1,
            alpha=0.7,
        ),
    )

    ax2.annotate(
        f"谷值: {min_rate:.2f}%\n{min_date_str}",
        xy=(min_idx, min_rate),
        xytext=(min_idx, min_rate * 1.15),  # 文本位置下移
        ha="center",
        va="top",
        fontsize=9,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8),
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3,rad=0.2",
            color="gray",
            shrinkA=0,
            shrinkB=5,
            lw=1,
            alpha=0.7,
        ),
    )

    plt.subplots_adjust(top=0.88, bottom=0.12)

    # 只调用一次plt.show()
    plt.show()
