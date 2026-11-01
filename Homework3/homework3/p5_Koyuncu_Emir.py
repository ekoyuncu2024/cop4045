"""Homework 3, Problem 5: recursion and turtle graphics."""

import time
import turtle
from testif import testif


def _straight_branch(level: int, length: float) -> None:
    """Draw a branching straight segment, then return to its start."""
    turtle.forward(length)
    if level > 0:
        turtle.left(35)
        _straight_branch(level - 1, length * 0.53)
        turtle.right(70)
        _straight_branch(level - 1, length * 0.53)
        turtle.left(35)
        _straight_branch(level - 1, length * 0.62)
    turtle.backward(length)


def draw_leaf_straight(level: int, length: float) -> None:
    """Draw a vertical recursive leaf with a straight stem.

    level must be a nonnegative integer; length must be positive.
    The turtle is oriented north, 90 degrees left from its default.
    """
    if not isinstance(level, int) or level < 0 or length <= 0:
        raise ValueError("Level must be nonnegative and length positive")
    turtle.reset()
    turtle.speed(0)
    turtle.delay(0)
    turtle.penup()
    turtle.goto(0, -270)
    turtle.setheading(90)
    turtle.pendown()
    _straight_branch(level, length)
    turtle.update()


def _curved_branch(level: int, length: float) -> None:
    """Draw recursively curving branches and restore turtle position."""
    starting_position = turtle.position()
    starting_heading = turtle.heading()
    turtle.circle(length * 2, 25)
    if level > 0:
        turtle.left(30)
        _curved_branch(level - 1, length * 0.55)
        turtle.right(65)
        _curved_branch(level - 1, length * 0.55)
        turtle.left(35)
        _curved_branch(level - 1, length * 0.60)
    turtle.penup()
    turtle.goto(starting_position)
    turtle.setheading(starting_heading)
    turtle.pendown()


def draw_leaf_curved(level: int, length: float) -> None:
    """Draw a vertically oriented recursive leaf with curved branches."""
    if not isinstance(level, int) or level < 0 or length <= 0:
        raise ValueError("Level must be nonnegative and length positive")
    turtle.reset()
    turtle.speed(0)
    turtle.delay(0)
    turtle.penup()
    turtle.goto(0, -270)
    turtle.setheading(90)
    turtle.pendown()
    _curved_branch(level, length)
    turtle.update()


def strB(n: int, base: int = 10) -> str:
    """Recursively return a nonnegative integer in base 2 through 26."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if not isinstance(base, int) or not 2 <= base <= 26:
        raise ValueError("base must be an integer from 2 to 26")
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < base:
        return digits[n]
    return strB(n // base, base) + digits[n % base]


_cnk_memo: dict[tuple[int, int], int] = {}


def Cnk_m(n: int, k: int) -> int:
    """Recursively compute n-choose-k using dictionary memoization.

    Require integers with 0 <= k <= n. Previously computed recursive
    cases are remembered in _cnk_memo. No cache decorator is used.
    """
    if not isinstance(n, int) or not isinstance(k, int):
        raise TypeError("n and k must be integers")
    if n < 0 or k < 0 or k > n:
        raise ValueError("Require 0 <= k <= n")
    if k == 0 or k == n:
        return 1
    key = (n, k)
    if key not in _cnk_memo:
        _cnk_memo[key] = Cnk_m(n - 1, k - 1) + Cnk_m(n - 1, k)
    return _cnk_memo[key]


def run_Cnk(n: int, k: int) -> int:
    """Print n-choose-k and the elapsed calculation time."""
    start = time.perf_counter()
    value = Cnk_m(n, k)
    elapsed = time.perf_counter() - start
    print("C({}, {}) = {}".format(n, k, value))
    print("Elapsed: {:.6f} seconds".format(elapsed))
    return value


def make_pairs(seq1: list, seq2: list,
               result: list[tuple] | None = None) -> list[tuple]:
    """Recursively pair matching positions using a list accumulator.

    Stop at the end of the shorter sequence. The optional result argument
    is the accumulator used by the recursive calls. No loop or list
    comprehension is used.
    """
    if result is None:
        result = []
    if not seq1 or not seq2:
        return result
    result.append((seq1[0], seq2[0]))
    return make_pairs(seq1[1:], seq2[1:], result)


def test_strB() -> None:
    """Perform four unit tests for base conversion using testif."""
    testif(strB(0, 2) == "0", "strB zero")
    testif(strB(255, 16) == "FF", "strB hexadecimal")
    testif(strB(35, 26) == "19", "strB base 26")
    testif(strB(42, 2) == "101010", "strB binary")


def test_Cnk_m() -> None:
    """Perform four unit tests for the memoized binomial function."""
    testif(Cnk_m(0, 0) == 1, "Cnk boundary zero")
    testif(Cnk_m(10, 0) == 1, "Cnk boundary k=0")
    testif(Cnk_m(10, 5) == 252, "Cnk 10 choose 5")
    testif(Cnk_m(25, 12) == 5200300, "Cnk 25 choose 12")


def test_make_pairs() -> None:
    """Perform five tests including empty and uneven input sequences."""
    testif(make_pairs([1, 2], [3, 4]) == [(1, 3), (2, 4)],
           "pairs equal length")
    testif(make_pairs([1, 2, 3], [4]) == [(1, 4)],
           "pairs shorter second list")
    testif(make_pairs([1], [2, 3]) == [(1, 2)],
           "pairs shorter first list")
    testif(make_pairs([], [1, 2]) == [], "pairs empty first list")
    testif(make_pairs([1, 2], []) == [], "pairs empty second list")


def main() -> None:
    """Run all recursion tests and print nonexample console values."""
    print("Recursion unit tests:")
    test_strB()
    test_Cnk_m()
    test_make_pairs()
    print("\nAdditional console examples:")
    print("strB(2026, 16) =", strB(2026, 16))
    print("strB(777, 7) =", strB(777, 7))
    run_Cnk(30, 15)
    run_Cnk(40, 8)
    print("make_pairs:", make_pairs(["A", "B", "C"], [1, 2]))
    print("FAU student ID:", input("Enter your FAU student ID: "))
    # Draw these separately in Spyder to capture the required screenshots:
    # draw_leaf_straight(6, 120)
    # draw_leaf_curved(6, 120)  # optional extra credit


if __name__ == "__main__":
    main()
