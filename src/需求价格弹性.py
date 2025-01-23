from typing import Callable

import numpy as np
from matplotlib import pyplot as plt


def 需求曲线(q: float) -> float:
    # return -0.5 * q + 5
    return 1 / q


def 需求弹性计算(q1: float, q2: float, f: Callable[[float], float]) -> float:
    p1 = f(q1)
    p2 = f(q2)
    quality_change_rate = (q2 - q1) / ((q1 + q2) / 2)
    price_change_rate = (p2 - p1) / ((p1 + p2) / 2)
    return abs(quality_change_rate / price_change_rate)


if __name__ == "__main__":
    # 设置中文字体，确保你有这个字体
    plt.rcParams["font.family"] = "SimHei"  # 黑体
    plt.rcParams["axes.unicode_minus"] = False  # 处理负号显示问题
    x = np.linspace(0, 10, 100)  # Sample data.

    # Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
    fig, ax = plt.subplots(figsize=(5, 5), layout="constrained")
    ax.plot(x, 需求曲线(x), label="需求曲线")  # Plot some data on the Axes.
    ax.plot(
        x, 需求弹性计算(x - 0.1, x + 0.1, 需求曲线), label="quadratic"
    )  # Plot more data on the Axes...
    ax.set_xlabel("需求")  # Add an x-label to the Axes.
    ax.set_ylabel("价格")  # Add a y-label to the Axes.
    ax.set_title("价格需求曲线，同时包含需求价格")  # Add a title to the Axes.
    ax.set_xlim(0, 10)
    ax.legend()  # Add a legend.
    plt.show()
