"""Homework 1, Problem 1: Quadratic equations."""

import math

import matplotlib.pyplot as plt


NUM_POINTS = 150


def plot_quadratic(a, b, c, roots):
    """Plot y = a*x^2 + b*x + c using exactly 150 sample points."""
    if roots:
        x_min = min(roots)
        x_max = max(roots)
        if x_min == x_max:
            x_min -= 3.0
            x_max += 3.0
        else:
            margin = max(1.0, 0.25 * (x_max - x_min))
            x_min -= margin
            x_max += margin
    else:
        x_opt = -b / (2 * a)
        x_min = x_opt - 5.0
        x_max = x_opt + 5.0

    step = (x_max - x_min) / (NUM_POINTS - 1)
    xs = [x_min + i * step for i in range(NUM_POINTS)]
    ys = [a * x**2 + b * x + c for x in xs]

    plt.figure()
    plt.plot(xs, ys)
    plt.axhline(0, linewidth=0.8)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Quadratic function")
    plt.grid(True)
    plt.show(block=True)


def main():
    """Read coefficients, print real roots, and display each quadratic."""
    while True:
        a_text = input("Enter a: ")
        if a_text == "":
            break

        a = float(a_text)
        b = float(input("Enter b: "))
        c = float(input("Enter c: "))
        discriminant = b**2 - 4 * a * c
        roots = []

        if discriminant < 0:
            print("no real solutions")
        elif discriminant == 0:
            x1 = -b / (2 * a)
            roots.append(x1)
            print("one solution: {:.5f}".format(x1))
        else:
            square_root = math.sqrt(discriminant)
            x1 = (-b - square_root) / (2 * a)
            x2 = (-b + square_root) / (2 * a)
            roots.extend([x1, x2])
            print("two solutions: x1={:.5f} x2={:.5f}".format(x1, x2))

        plot_quadratic(a, b, c, roots)
        print()


if __name__ == "__main__":
    main()
