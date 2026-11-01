"""Homework 3, Problem 1: N-dimensional vectors."""

from numbers import Real
from testif import testif


class NVector:
    """Store a vector of real numbers in an independent Python list."""

    def __init__(self, *values: Real | list[Real] | tuple[Real, ...]) -> None:
        """Create a vector from a sequence or from two or more numbers.

        A single argument must be an iterable of numbers. The elements
        are copied so editing the original sequence cannot change the vector.
        Raises TypeError for unsupported arguments.
        """
        if len(values) == 1:
            try:
                self.elements = list(values[0])
            except TypeError as error:
                raise TypeError(
                    "A single argument must be a sequence") from error
        elif len(values) >= 2:
            self.elements = list(values)
        else:
            raise TypeError("Supply a sequence or at least two numbers")

        if any(not isinstance(value, Real) for value in self.elements):
            raise TypeError("Vector elements must be real numbers")

    def __len__(self) -> int:
        """Return the number of elements in this vector."""
        return len(self.elements)

    def __getitem__(self, index: int) -> Real:
        """Return an element, allowing positive or negative list indices."""
        return self.elements[index]

    def __setitem__(self, index: int, value: Real) -> None:
        """Replace an element; raise IndexError for invalid indices."""
        if not isinstance(value, Real):
            raise TypeError("Vector elements must be real numbers")
        self.elements[index] = value

    def __str__(self) -> str:
        """Return an easily readable representation of the vector."""
        return "NVector({})".format(self.elements)

    def __eq__(self, other: object) -> bool:
        """Compare dimensions and corresponding elements of two vectors."""
        return (isinstance(other, NVector)
                and self.elements == other.elements)

    def __ne__(self, other: object) -> bool:
        """Return True exactly when two vectors are not equal."""
        return not self.__eq__(other)

    def __add__(self, other: "NVector | Real") -> "NVector":
        """Add a number to each element, or add another vector elementwise.

        Vectors must have matching dimensions. Raise ValueError otherwise.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have equal dimensions")
            return NVector([a + b for a, b in
                            zip(self.elements, other.elements)])
        if isinstance(other, Real):
            return NVector([a + other for a in self.elements])
        return NotImplemented

    def __radd__(self, other: Real) -> "NVector":
        """Support adding a scalar to the left of a vector."""
        return self.__add__(other)

    def __mul__(self, other: "NVector | Real") -> Real:
        """Return a dot product, or the sum of scalar-scaled elements.

        When multiplying two vectors, dimensions must be equal.
        """
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have equal dimensions")
            return sum(a * b for a, b in
                       zip(self.elements, other.elements))
        if isinstance(other, Real):
            return sum(a * other for a in self.elements)
        return NotImplemented

    def __rmul__(self, other: Real) -> Real:
        """Support a scalar on the left of the multiplication operator."""
        return self.__mul__(other)

    @classmethod
    def zeros(cls, n: int) -> "NVector":
        """Return a vector containing n zeroes; n must be nonnegative."""
        if not isinstance(n, int) or n < 0:
            raise ValueError("Dimension must be a nonnegative integer")
        return cls([0] * n)


def main() -> None:
    """Exercise each required vector operation using the supplied testif."""
    original = [3, 0, 1, -1]
    v = NVector(original)
    original[0] = 99
    testif(v[0] == 3, "constructor copies the input")
    testif(NVector((3, 0, 1, -1)) == v, "tuple constructor")
    testif(NVector(3, 0, 1, -1) == v, "multiple arguments")
    testif(len(v) == 4, "vector length")
    testif(v[1] == 0 and v[-2] == 1, "positive and negative indices")
    v[2] = 5
    testif(v[2] == 5, "indexed assignment")
    testif(str(v) == "NVector([3, 0, 5, -1])", "string conversion")
    testif(v != NVector(3, 0, 1, -1), "not-equal operation")

    a = NVector(3, 0, 1, -1)
    b = NVector(1, 2, 3, 4)
    testif(a + b == NVector(4, 2, 4, 3), "vector addition")
    testif(a + 10 == NVector(13, 10, 11, 9), "scalar addition")
    testif(10 + a == NVector(13, 10, 11, 9), "reflected addition")
    testif(a * b == 2, "dot product")
    testif(a * 2 == 6 and 2 * a == 6, "scalar multiplication")
    testif(NVector.zeros(4) == NVector(0, 0, 0, 0), "zeros method")
    try:
        v[99] = 1
        testif(False, "invalid index raises IndexError")
    except IndexError:
        testif(True, "invalid index raises IndexError")
    print("Example vector:", a)
    print("FAU student ID:", input("Enter your FAU student ID: "))


if __name__ == "__main__":
    main()
