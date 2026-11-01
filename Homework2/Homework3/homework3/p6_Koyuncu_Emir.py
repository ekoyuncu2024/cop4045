"""Homework 3, Problem 6: represent and recursively search a file hierarchy."""

from __future__ import annotations


class Entry:
    """Represent a named entry with an optional parent entry."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize the entry's name and parent reference."""
        self.name = name
        self._parent = parent

    def parent(self) -> Entry | None:
        """Return this entry's parent, or None for a root entry."""
        return self._parent

    def size(self) -> int:
        """Require subclasses to provide their size in bytes."""
        raise NotImplementedError("Subclasses must implement size().")

    def absolute_path(self) -> list[Entry]:
        """Recursively return entries from this entry back to the root."""
        if self._parent is None:
            return [self]
        return [self] + self._parent.absolute_path()


class File(Entry):
    """Represent a file that occupies a nonnegative number of bytes."""

    def __init__(
        self, name: str, bytes_used: int, parent: Entry | None = None
    ) -> None:
        """Initialize a file, rejecting a negative byte size."""
        super().__init__(name, parent)
        if bytes_used < 0:
            raise ValueError("A file's byte size cannot be negative.")
        self.bytes_used = bytes_used

    def size(self) -> int:
        """Return the number of bytes occupied by this file."""
        return self.bytes_used


class Folder(Entry):
    """Represent a folder containing file and folder entries."""

    def __init__(self, name: str, parent: Entry | None = None) -> None:
        """Initialize an empty folder with a name and optional parent."""
        super().__init__(name, parent)
        self._children: list[Entry] = []

    def add(self, entry: Entry) -> None:
        """Add an entry as a child and set its parent to this folder."""
        self._children.append(entry)
        entry._parent = self

    def children(self) -> tuple[Entry, ...]:
        """Return an immutable tuple of this folder's children."""
        return tuple(self._children)

    def size(self) -> int:
        """Return the total size of all children using their size methods."""
        return sum(child.size() for child in self._children)


def find_large_files(entry: Entry, minimum_size: int) -> list[File]:
    """Recursively find files at least minimum_size bytes, in child order."""
    if isinstance(entry, File):
        if entry.size() >= minimum_size:
            return [entry]
        return []

    matches: list[File] = []
    if isinstance(entry, Folder):
        for child in entry.children():
            matches.extend(find_large_files(child, minimum_size))
    return matches


def main() -> None:
    """Demonstrate nested sizes, file searches, paths, and student ID input."""
    homework = Folder("homework")
    lectures = Folder("lectures")
    projects = Folder("projects")
    python = Folder("python")
    program = File("program.py", 1200)

    homework.add(File("readme.txt", 200))
    homework.add(lectures)
    homework.add(projects)
    lectures.add(File("notes.txt", 800))
    projects.add(python)
    python.add(program)
    python.add(File("program_test.py", 600))

    print("Homework 3, Problem 6 - File Hierarchy")
    print("Folder hierarchy (file sizes are in bytes):")
    print("homework/")
    print("  readme.txt (200)")
    print("  lectures/")
    print("    notes.txt (800)")
    print("  projects/")
    print("    python/")
    print("      program.py (1200)")
    print("      program_test.py (600)")

    # One call dispatches to File.size() or Folder.size() for each child.
    print(f"\nTotal size of homework: {homework.size()} bytes")

    for threshold in (600, 1000):
        print(f"\nFiles using at least {threshold} bytes:")
        for file in find_large_files(homework, threshold):
            print(f"  {file.name}: {file.size()} bytes")

    path = program.absolute_path()
    print("\nAbsolute path entries (current entry to root):")
    print(" -> ".join(entry.name for entry in path))

    student_id = input("\nEnter your FAU student ID: ")
    print(f"FAU student ID: {student_id}")


if __name__ == "__main__":
    main()
