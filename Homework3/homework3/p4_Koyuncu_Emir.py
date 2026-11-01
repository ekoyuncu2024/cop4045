"""Homework 3, Problem 4: a small noninteractive text editor."""

import os
import tempfile
from testif import testif


def ed_read(filename: str, from_index: int = 0,
            to: int = -1) -> str:
    """Return the file's UTF-8 text in [from_index, to).

    The default to=-1 means the end of the file. Raise ValueError for
    negative or reversed positions and IndexError if a position exceeds
    the file length. Propagate file I/O errors without modifying the file.
    """
    if from_index < 0 or to < -1:
        raise ValueError("Positions must be nonnegative, except to=-1")
    with open(filename, "r", encoding="utf-8") as source:
        text = source.read()
    end = len(text) if to == -1 else to
    if from_index > len(text) or end > len(text):
        raise IndexError("Position exceeds file length")
    if end < from_index:
        raise ValueError("End position cannot precede start position")
    return text[from_index:end]


def ed_find(filename: str, search_str: str) -> list[int]:
    """Return starting indices of each nonoverlapping search_str match.

    An empty search string is invalid; file I/O errors are propagated.
    """
    if not search_str:
        raise ValueError("Search string cannot be empty")
    text = ed_read(filename)
    positions = []
    start = 0
    while True:
        found = text.find(search_str, start)
        if found == -1:
            break
        positions.append(found)
        start = found + len(search_str)
    return positions


def _save_text(filename: str, text: str) -> None:
    """Atomically replace a UTF-8 file after successful writing.

    A temporary file is used so a failed write does not erase the original.
    Exceptions from file operations are passed to the calling function.
    """
    directory = os.path.dirname(os.path.abspath(filename))
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="", dir=directory,
                delete=False) as output:
            temporary = output.name
            output.write(text)
        os.replace(temporary, filename)
    finally:
        if temporary is not None and os.path.exists(temporary):
            os.remove(temporary)


def ed_replace(filename: str, search_str: str,
               replace_with: str, occurrence: int = -1) -> int:
    """Replace one zero-indexed occurrence or all occurrences (-1).

    Return the number of replacements performed (zero or a positive int).
    Raise ValueError for empty search text or an invalid occurrence index.
    A replacement outside the available matches leaves the file unchanged.
    """
    if not search_str:
        raise ValueError("Search string cannot be empty")
    if occurrence < -1:
        raise ValueError("Occurrence must be -1 or nonnegative")
    text = ed_read(filename)
    positions = ed_find(filename, search_str)
    if occurrence == -1:
        # Match normal str.replace behavior for nonoverlapping occurrences.
        changes = text.count(search_str)
        updated = text.replace(search_str, replace_with)
    elif occurrence >= len(positions):
        return 0
    else:
        position = positions[occurrence]
        changes = 1
        updated = (text[:position] + replace_with
                   + text[position + len(search_str):])
    if changes:
        _save_text(filename, updated)
    return changes


def ed_append(filename: str, string: str) -> int:
    """Append a string, creating the UTF-8 file when necessary.

    Return the number of characters appended. Preserve old content if the
    write fails, and propagate any file I/O error.
    """
    if not isinstance(string, str):
        raise TypeError("Content must be a string")
    if os.path.exists(filename):
        current = ed_read(filename)
    else:
        current = ""
    _save_text(filename, current + string)
    return len(string)


def test_ed_find() -> None:
    """Use testif to verify search positions and missing strings."""
    with tempfile.TemporaryDirectory() as directory:
        filename = os.path.join(directory, "find.txt")
        ed_append(filename, "01234567890123456789")
        testif(ed_find(filename, "345") == [3, 13], "find two matches")
        testif(ed_find(filename, "356") == [], "find absent substring")
        ed_append(filename, "aaaa")
        testif(ed_find(filename, "aa") == [20, 22],
               "find repeated matches")


def test_ed_replace() -> None:
    """Use testif to verify individual/all replacements and no-op cases."""
    with tempfile.TemporaryDirectory() as directory:
        filename = os.path.join(directory, "replace.txt")
        ed_append(filename, "01234567890123456789")
        testif(ed_replace(filename, "345", "ABCDE", 1) == 1,
               "replace second occurrence")
        testif(ed_read(filename) == "0123456789012ABCDE6789",
               "second occurrence content")
        testif(ed_replace(filename, "XYZ", "z") == 0,
               "replace absent text")
        testif(ed_replace(filename, "345", "Z", 5) == 0,
               "out-of-range occurrence unchanged")
        _save_text(filename, "aaaa")
        testif(ed_replace(filename, "aa", "X", 1) == 1,
               "replace second repeated occurrence")
        testif(ed_read(filename) == "aaX",
               "second repeated occurrence content")
        _save_text(filename, "01234567890123456789")
        testif(ed_replace(filename, "345", "ABCDE") == 2,
               "replace all occurrences")
        testif(ed_read(filename) == "012ABCDE6789012ABCDE6789",
               "replace all content")


def main() -> None:
    """Demonstrate each editing command and run the requested unit tests."""
    with tempfile.TemporaryDirectory() as directory:
        filename = os.path.join(directory, "file1.txt")
        print("Append:", ed_append(filename, "0123456789"))
        print("Append again:", ed_append(filename, "0123456789"))
        print("Read [3, 9):", ed_read(filename, 3, 9))
        print("Read [3, end):", ed_read(filename, 3))
        print("Find 345:", ed_find(filename, "345"))
        print("Find 356:", ed_find(filename, "356"))
        print("Replace second 345:", ed_replace(filename, "345", "ABCDE", 1))
        print("After replacement:", ed_read(filename))
        print("\nUnit tests:")
        test_ed_find()
        test_ed_replace()
    print("FAU student ID:", input("Enter your FAU student ID: "))


if __name__ == "__main__":
    main()
