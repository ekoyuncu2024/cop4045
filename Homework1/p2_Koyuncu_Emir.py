"""Homework 1, Problem 2: Pythagorean numbers."""


def Pythagorean(n):
    """Return all positive Pythagorean triples with values at most n."""
    triples = []

    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a**2 + b**2 == c**2:
                    triples.append((a, b, c))

    return triples


def main():
    """Read n and display all Pythagorean triples up to n."""
    n = int(input("Enter a positive integer n: "))
    print(Pythagorean(n))


if __name__ == "__main__":
    main()
