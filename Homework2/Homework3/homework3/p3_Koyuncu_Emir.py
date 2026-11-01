"""Homework 3, Problem 3: prey, predators, and humans.

Adapted from the supplied Chapter 13 program13-14.py predator-prey example.
"""

import random
import matplotlib.pyplot as plt


class Island:
    """A square grid containing prey, predators, and humans."""

    def __init__(self, n: int, prey_count: int = 0,
                 predator_count: int = 0, count_humans: int = 0) -> None:
        """Create an n-by-n grid and randomly position initial animals."""
        if n < 1 or min(prey_count, predator_count, count_humans) < 0:
            raise ValueError("Grid size and populations must be valid")
        if prey_count + predator_count + count_humans > n * n:
            raise ValueError("Initial animals exceed available grid cells")
        self.grid_size = n
        self.grid: list[list[Animal | int]] = [[0] * n for _ in range(n)]
        self.init_animals(prey_count, predator_count, count_humans)

    def init_animals(self, prey_count: int, predator_count: int,
                     count_humans: int) -> None:
        """Place the requested populations in random unoccupied cells."""
        locations = [(x, y) for x in range(self.grid_size)
                     for y in range(self.grid_size)]
        random.shuffle(locations)
        animals: list[type[Animal]] = ([Prey] * prey_count
                                       + [Predator] * predator_count
                                       + [Human] * count_humans)
        for animal_type, (x, y) in zip(animals, locations):
            self.register(animal_type(self, x, y))

    def clear_all_moved_flags(self) -> None:
        """Allow each animal to move again on the next clock tick."""
        for column in self.grid:
            for animal in column:
                if isinstance(animal, Animal):
                    animal.clear_moved_flag()

    def size(self) -> int:
        """Return the side length of the island."""
        return self.grid_size

    def register(self, animal: "Animal") -> None:
        """Place an animal at the coordinates stored in that animal."""
        self.grid[animal.x][animal.y] = animal

    def remove(self, animal: "Animal") -> None:
        """Remove an animal only if it still occupies its recorded cell."""
        if self.animal(animal.x, animal.y) is animal:
            self.grid[animal.x][animal.y] = 0

    def animal(self, x: int, y: int) -> "Animal | int":
        """Return a cell occupant, or -1 for coordinates off the island."""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.grid[x][y]
        return -1

    def __str__(self) -> str:
        """Return the grid with O for prey, X for predators, H for humans."""
        lines = []
        for y in range(self.grid_size - 1, -1, -1):
            lines.append("  ".join(str(self.grid[x][y])
                                    if self.grid[x][y] else "."
                                    for x in range(self.grid_size)))
        return "\n".join(lines)

    def count_prey(self) -> int:
        """Return the number of prey still living on the island."""
        return self._count_type(Prey)

    def count_predators(self) -> int:
        """Return the number of predators still living on the island."""
        return self._count_type(Predator)

    def count_humans(self) -> int:
        """Return the number of humans still living on the island."""
        return self._count_type(Human)

    def _count_type(self, animal_type: type["Animal"]) -> int:
        """Count grid cells containing animals of the requested class."""
        return sum(isinstance(animal, animal_type)
                   for column in self.grid for animal in column)


class Animal:
    """Provide movement, breeding, and position for all island animals."""

    breed_time: int = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 symbol: str = "A") -> None:
        """Store the island, coordinates, display symbol, and moved flag."""
        self.island = island
        self.x = x
        self.y = y
        self.name = symbol
        self.moved = False
        self.breed_clock = self.breed_time

    def position(self) -> tuple[int, int]:
        """Return the animal's current x and y coordinates."""
        return self.x, self.y

    def __str__(self) -> str:
        """Return this type of animal's single-character grid symbol."""
        return self.name

    def check_grid(self, type_looking_for: type = int
                   ) -> tuple[int, int] | None:
        """Return first neighboring location containing the requested type."""
        offsets = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0),
                   (-1, -1), (0, -1), (1, -1)]
        for dx, dy in offsets:
            x, y = self.x + dx, self.y + dy
            if 0 <= x < self.island.size() and 0 <= y < self.island.size():
                if type(self.island.animal(x, y)) is type_looking_for:
                    return x, y
        return None

    def move(self) -> None:
        """Move once per tick to an available neighboring cell, if possible."""
        if self.moved:
            return
        location = self.check_grid()
        if location is not None:
            self.island.remove(self)
            self.x, self.y = location
            self.island.register(self)
            self.moved = True

    def breed(self) -> None:
        """Produce the same animal species in an empty neighboring cell."""
        if self.breed_clock <= 0:
            location = self.check_grid()
            if location is not None:
                self.breed_clock = self.breed_time
                newborn = self.__class__(self.island, *location)
                newborn.moved = True
                self.island.register(newborn)

    def clear_moved_flag(self) -> None:
        """Reset movement status at the beginning of each tick."""
        self.moved = False


class Prey(Animal):
    """An animal that moves and breeds without hunting another species."""

    breed_time: int = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 symbol: str = "O") -> None:
        """Initialize a prey animal at the given island coordinates."""
        super().__init__(island, x, y, symbol)

    def clock_tick(self) -> None:
        """Decrease the prey's breeding timer by one."""
        self.breed_clock -= 1


class Predator(Animal):
    """An animal that eats prey and dies if it goes too long without food."""

    breed_time: int = 6
    starve_time: int = 3

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 symbol: str = "X") -> None:
        """Initialize a predator's breeding and starvation timers."""
        super().__init__(island, x, y, symbol)
        self.starve_clock = self.starve_time

    def clock_tick(self) -> None:
        """Advance breeding/starvation timers; remove a starving predator."""
        self.breed_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)

    def eat(self) -> None:
        """Eat adjacent prey and move into its location, once per tick."""
        if self.moved:
            return
        location = self.check_grid(Prey)
        if location is not None:
            victim = self.island.animal(*location)
            self.island.remove(victim)
            self.island.remove(self)
            self.x, self.y = location
            self.island.register(self)
            self.starve_clock = self.starve_time
            self.moved = True


class Human(Animal):
    """An animal that moves, breeds, and periodically hunts predators."""

    breed_time: int = 12
    hunt_time: int = 3
    starve_time: int = 8

    def __init__(self, island: Island, x: int = 0, y: int = 0,
                 symbol: str = "H") -> None:
        """Initialize clocks for breeding, starvation, and periodic hunts."""
        super().__init__(island, x, y, symbol)
        self.starve_clock = self.starve_time
        self.hunt_clock = self.hunt_time - 1

    def hunt(self) -> None:
        """At each hunt interval, kill an adjacent predator, never prey."""
        if self.hunt_clock > 0 or self.moved:
            return
        self.hunt_clock = self.hunt_time
        location = self.check_grid(Predator)
        if location is not None:
            victim = self.island.animal(*location)
            self.island.remove(victim)
            self.island.remove(self)
            self.x, self.y = location
            self.island.register(self)
            self.starve_clock = self.starve_time
            self.moved = True

    def clock_tick(self) -> None:
        """Update all clocks and remove a human who has starved."""
        self.breed_clock -= 1
        self.hunt_clock -= 1
        self.starve_clock -= 1
        if self.starve_clock <= 0:
            self.island.remove(self)


def main(predator_breed_time: int = 6,
         predator_starve_time: int = 3,
         initial_predators: int = 10,
         prey_breed_time: int = 3,
         initial_prey: int = 50,
         size: int = 10,
         ticks: int = 1000,
         human_breed_time: int = 20,
         human_starve_time: int = 15,
         human_hunt_time: int = 7,
         initial_humans: int = 3,
         seed: int | None = 11,
         show_plot: bool = True,
         plot_path: str | None = None
         ) -> tuple[list[int], list[int], list[int]]:
    """Run the three-species simulation and plot their population histories.

    Stops after 50 consecutive ticks with unchanged counts or at the limit
    of 1000 ticks. Returns the three histories for additional testing.
    """
    periods = (predator_breed_time, predator_starve_time,
               prey_breed_time, human_breed_time, human_starve_time,
               human_hunt_time)
    if min(periods) < 1 or ticks < 0:
        raise ValueError("All periods must be positive and ticks nonnegative")
    if seed is not None:
        random.seed(seed)
    Predator.breed_time = predator_breed_time
    Predator.starve_time = predator_starve_time
    Prey.breed_time = prey_breed_time
    Human.breed_time = human_breed_time
    Human.starve_time = human_starve_time
    Human.hunt_time = human_hunt_time

    isle = Island(size, initial_prey, initial_predators, initial_humans)
    print("Initial island (tick 0):")
    print(isle)
    prey_list = [isle.count_prey()]
    predator_list = [isle.count_predators()]
    human_list = [isle.count_humans()]
    unchanged_ticks = 0

    for tick in range(1, min(ticks, 1000) + 1):
        isle.clear_all_moved_flags()
        # Take a snapshot so each living animal acts at most once per tick.
        # Newborn animals begin their first turn on the next tick.
        animals = [isle.animal(x, y) for x in range(size)
                   for y in range(size)]
        for animal in animals:
            if not isinstance(animal, Animal):
                continue
            # A neighboring hunter may have eaten this animal already.
            if isle.animal(animal.x, animal.y) is not animal:
                continue
            if isinstance(animal, Predator):
                animal.eat()
            elif isinstance(animal, Human):
                animal.hunt()
            animal.move()
            animal.breed()
            animal.clock_tick()

        counts = (isle.count_prey(), isle.count_predators(),
                  isle.count_humans())
        prey_list.append(counts[0])
        predator_list.append(counts[1])
        human_list.append(counts[2])
        if tick % 10 == 0 or tick == 1:
            print("Tick {:3d}: prey={}, predators={}, humans={}".format(
                tick, *counts))
        if counts == (prey_list[-2], predator_list[-2], human_list[-2]):
            unchanged_ticks += 1
        else:
            unchanged_ticks = 0
        if unchanged_ticks >= 50:
            print("All three populations have stabilized.")
            break

    print("\nFinal island (tick {}):".format(len(prey_list) - 1))
    print(isle)
    print("Final populations: prey={}, predators={}, humans={}".format(
        prey_list[-1], predator_list[-1], human_list[-1]))

    plt.figure(figsize=(9, 5))
    plt.plot(prey_list, label="Prey")
    plt.plot(predator_list, label="Predators")
    plt.plot(human_list, label="Humans")
    plt.xlabel("Time (clock ticks)")
    plt.ylabel("Population")
    plt.title("Prey, Predator, and Human Populations")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    if plot_path is not None:
        plt.savefig(plot_path, dpi=180)
    if show_plot:
        plt.show()
    else:
        plt.close()
    return prey_list, predator_list, human_list


if __name__ == "__main__":
    main(predator_breed_time=5, prey_breed_time=2,
         human_breed_time=80, human_starve_time=25,
         human_hunt_time=12, initial_humans=2, seed=5)
    print("FAU student ID:", input("Enter your FAU student ID: "))
