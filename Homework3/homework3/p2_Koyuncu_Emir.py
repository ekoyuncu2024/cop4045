"""Homework 3, Problem 2: university parking permits."""


class ParkingPermit:
    """Represent a parking permit with a configurable fee schedule."""

    def __init__(self, owner: str, months: int,
                 fees: dict[str, float]) -> None:
        """Store owner, term, and fee schedule for a valid permit.

        The term must be positive, and all schedule amounts nonnegative.
        """
        if not isinstance(months, int) or months <= 0:
            raise ValueError("Months must be a positive integer")
        if any(amount < 0 for amount in fees.values()):
            raise ValueError("Fees cannot be negative")
        self.owner = owner
        self.months = months
        self.fees = dict(fees)

    def cost(self) -> float:
        """Return the permit cost, as implemented by each subclass."""
        raise NotImplementedError("Use StudentPermit or FacultyPermit")

    def __str__(self) -> str:
        """Return a readable description of the base permit."""
        return "Parking permit for {} ({} months)".format(
            self.owner, self.months)

    def __repr__(self) -> str:
        """Return a representation showing the constructor arguments."""
        return "ParkingPermit({!r}, {!r}, {!r})".format(
            self.owner, self.months, self.fees)


class StudentPermit(ParkingPermit):
    """Parking permit for a student with one or more vehicles."""

    def __init__(self, owner: str, months: int,
                 fees: dict[str, float], vehicles: int) -> None:
        """Initialize a student permit and the registered vehicle count."""
        super().__init__(owner, months, fees)
        if not isinstance(vehicles, int) or vehicles < 1:
            raise ValueError("At least one vehicle is required")
        self.vehicles = vehicles

    def cost(self) -> float:
        """Charge student monthly fees and extra-vehicle fees once."""
        return (self.months * self.fees["student_monthly"]
                + (self.vehicles - 1) * self.fees["extra_vehicle"])

    def __str__(self) -> str:
        """Return a human-readable student permit description."""
        return "Student permit: {}, {} month(s), {} vehicle(s)".format(
            self.owner, self.months, self.vehicles)

    def __repr__(self) -> str:
        """Return a representation with all constructor arguments."""
        return "StudentPermit({!r}, {!r}, {!r}, {!r})".format(
            self.owner, self.months, self.fees, self.vehicles)


class FacultyPermit(ParkingPermit):
    """Parking permit for faculty, optionally including garage access."""

    def __init__(self, owner: str, months: int,
                 fees: dict[str, float], garage: bool) -> None:
        """Initialize the faculty permit and optional garage access."""
        super().__init__(owner, months, fees)
        self.garage = garage

    def cost(self) -> float:
        """Charge faculty monthly fees and monthly garage fees if used."""
        monthly = self.fees["faculty_monthly"]
        if self.garage:
            monthly += self.fees["garage_monthly"]
        return self.months * monthly

    def __str__(self) -> str:
        """Return a readable description of the faculty permit."""
        garage_text = "with garage" if self.garage else "without garage"
        return "Faculty permit: {}, {} month(s), {}".format(
            self.owner, self.months, garage_text)

    def __repr__(self) -> str:
        """Return a representation with all constructor arguments."""
        return "FacultyPermit({!r}, {!r}, {!r}, {!r})".format(
            self.owner, self.months, self.fees, self.garage)


def summarize_list(permits: list[ParkingPermit]) -> float:
    """Print each owner and permit cost; return the total revenue."""
    total = 0.0
    for permit in permits:
        print("{}: ${:.2f}".format(str(permit), permit.cost()))
        total += permit.cost()
    return total


def main() -> None:
    """Illustrate inheritance, representations, and polymorphic cost calls."""
    fees = {"student_monthly": 25.0,
            "extra_vehicle": 10.0,
            "faculty_monthly": 40.0,
            "garage_monthly": 15.0}
    permits = [StudentPermit("Alex", 3, fees, 2),
               FacultyPermit("Jordan", 3, fees, True),
               StudentPermit("Sam", 2, fees, 1),
               FacultyPermit("Taylor", 1, fees, False)]

    print("Permits:")
    for permit in permits:
        print(str(permit))
        print("repr:", repr(permit))
    print("\nOwner totals:")
    total = summarize_list(permits)
    print("Total permit revenue: ${:.2f}".format(total))
    print("FAU student ID:", input("Enter your FAU student ID: "))


if __name__ == "__main__":
    main()
