"""Unit tests for Homework 3, Problem 6."""

import unittest

from p6_Koyuncu_Emir import Entry, File, Folder, find_large_files


class FileHierarchyTests(unittest.TestCase):
    """Test recursive searches, paths, sizes, and parent relationships."""

    def setUp(self) -> None:
        """Build a hierarchy with three folder levels and boundary sizes."""
        self.root = Folder("root")
        self.middle = Folder("middle")
        self.inner = Folder("inner")
        self.empty = Folder("empty")
        self.zero = File("zero.txt", 0)
        self.small = File("small.txt", 99)
        self.exact = File("exact.txt", 100)
        self.large = File("large.txt", 101)

        self.root.add(self.zero)
        self.root.add(self.small)
        self.root.add(self.middle)
        self.root.add(self.empty)
        self.middle.add(self.exact)
        self.middle.add(self.inner)
        self.inner.add(self.large)

    def test_find_nested_files_at_boundary(self) -> None:
        """Include files equal to and above the threshold in nested folders."""
        self.assertEqual(find_large_files(self.root, 100), [self.exact, self.large])

    def test_find_zero_threshold(self) -> None:
        """Include every file, including a zero-byte file, at threshold zero."""
        self.assertEqual(
            find_large_files(self.root, 0),
            [self.zero, self.small, self.exact, self.large],
        )

    def test_find_above_largest_size(self) -> None:
        """Return an empty list when no file reaches the threshold."""
        self.assertEqual(find_large_files(self.root, 102), [])

    def test_find_empty_folder(self) -> None:
        """Return an empty list for an empty folder even at threshold zero."""
        self.assertEqual(find_large_files(self.empty, 0), [])

    def test_find_single_file(self) -> None:
        """Handle a File directly with thresholds below, at, and above its size."""
        self.assertEqual(find_large_files(self.exact, 99), [self.exact])
        self.assertEqual(find_large_files(self.exact, 100), [self.exact])
        self.assertEqual(find_large_files(self.exact, 101), [])

    def test_find_only_inside_selected_folder(self) -> None:
        """Search only the supplied folder and its descendants."""
        self.assertEqual(find_large_files(self.inner, 0), [self.large])

    def test_path_of_root(self) -> None:
        """A root entry's path contains only that entry."""
        self.assertEqual(self.root.absolute_path(), [self.root])

    def test_path_of_nested_file(self) -> None:
        """Return actual Entry objects in order from a nested file to the root."""
        path = self.large.absolute_path()
        self.assertIsInstance(path, list)
        expected = [self.large, self.inner, self.middle, self.root]
        self.assertEqual(len(path), len(expected))
        for actual, entry in zip(path, expected):
            self.assertIs(actual, entry)

    def test_path_of_nested_folder(self) -> None:
        """Include each ancestor when the starting entry is a folder."""
        self.assertEqual(
            self.inner.absolute_path(), [self.inner, self.middle, self.root]
        )

    def test_path_of_standalone_file(self) -> None:
        """A file with no parent has a one-entry path."""
        standalone = File("standalone.txt", 10)
        self.assertEqual(standalone.absolute_path(), [standalone])

    def test_parent_references(self) -> None:
        """Adding files or folders sets the correct parent reference."""
        self.assertIsNone(self.root.parent())
        self.assertIs(self.small.parent(), self.root)
        self.assertIs(self.middle.parent(), self.root)
        self.assertIs(self.inner.parent(), self.middle)
        self.assertIs(self.large.parent(), self.inner)

    def test_children_tuple(self) -> None:
        """Expose children in insertion order as a tuple."""
        self.assertIsInstance(self.root.children(), tuple)
        self.assertEqual(
            self.root.children(),
            (self.zero, self.small, self.middle, self.empty),
        )
        self.assertEqual(self.empty.children(), ())

    def test_recursive_folder_size(self) -> None:
        """One outer size call totals direct and nested files polymorphically."""
        self.assertEqual(self.root.size(), 300)
        self.assertEqual(self.middle.size(), 201)
        self.assertEqual(self.inner.size(), 101)
        self.assertEqual(self.empty.size(), 0)

    def test_file_size_boundaries(self) -> None:
        """Accept zero bytes and reject negative byte sizes with ValueError."""
        self.assertEqual(self.zero.size(), 0)
        self.assertEqual(self.exact.size(), 100)
        with self.assertRaises(ValueError):
            File("invalid.txt", -1)

    def test_base_entry(self) -> None:
        """Store a base entry's name and parent and require a size override."""
        entry = Entry("entry", self.root)
        self.assertEqual(entry.name, "entry")
        self.assertIs(entry.parent(), self.root)
        self.assertEqual(entry.absolute_path(), [entry, self.root])
        with self.assertRaises(NotImplementedError):
            entry.size()


if __name__ == "__main__":
    unittest.main()
