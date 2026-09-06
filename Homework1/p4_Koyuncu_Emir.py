"""Homework 1, Problem 4: Function visualization."""

import math

import matplotlib.pyplot as plt


def plot_function(fun_str, domain, ns):
    """Print a value table and plot a function over the given domain."""
    xmin, xmax = domain
    step = (xmax - xmin) / (ns - 1)
    xs = [xmin + i * step for i in range(ns)]
    ys = []

    for x in xs:
        y = eval(fun_str)
        ys.append(y)

    print("{:>12} {:>12}".format("x", "y"))
    print("{:>12} {:>12}".format("------------", "------------"))
    for x, y in zip(xs, ys):
        print("{:+12.4f} {:+12.4f}".format(x, y))

    plt.figure()
    plt.plot(xs, ys, marker="o", markersize=3)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(fun_str)
    plt.grid(True)
    plt.show()


def main():
    """Read the function, sample count, and domain from the terminal."""
    fun_str = input("Enter function with variable x: ")
    ns = int(input("Enter number of samples: "))
    xmin = float(input("Enter xmin: "))
    xmax = float(input("Enter xmax: "))
    plot_function(fun_str, (xmin, xmax), ns)


if __name__ == "__main__":
    main()
