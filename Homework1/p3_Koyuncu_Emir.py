"""Homework 1, Problem 3: Duplicated substrings."""


def find_dup_str(s, n):
    """Return the first non-overlapping duplicated substring of length n."""
    if n <= 0:
        return ""

    for i in range(len(s) - n + 1):
        substring = s[i:i + n]
        for j in range(i + n, len(s) - n + 1):
            if substring == s[j:j + n]:
                return substring

    return ""


def find_max_dup(s):
    """Return the longest non-overlapping duplicated substring in s."""
    for n in range(len(s) // 2, 0, -1):
        duplicate = find_dup_str(s, n)
        if duplicate != "":
            return duplicate

    return ""


def main():
    """Run the two requested interactive tests."""
    s = input("Enter a string: ")
    n = int(input("Enter substring length: "))
    print(find_dup_str(s, n))

    s = input("Enter a string: ")
    print(find_max_dup(s))


if __name__ == "__main__":
    main()
