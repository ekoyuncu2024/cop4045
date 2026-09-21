"""Homework 2, Problem 3: A simplified social network."""

import csv
import os


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Add a user with no friends and return whether the user was added."""
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except (TypeError, AttributeError) as error:
        print("Could not add the user:", error)
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Add a mutual friend link and return whether both users were found."""
    try:
        if user1 not in sn or user2 not in sn or user1 == user2:
            return False

        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)
        return True
    except (TypeError, IndexError, KeyError, AttributeError) as error:
        print("Could not add the friend link:", error)
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list[str]:
    """Return all friends up to the requested link distance."""
    try:
        if user1 not in sn:
            return []
        if not isinstance(distance, int) or distance <= 0:
            raise ValueError("distance must be a positive integer")

        visited = {user1}
        current_level = [user1]
        friends = []

        for unused_level in range(distance):
            next_level = []
            for username in current_level:
                for friend in sn[username][1]:
                    if friend not in visited:
                        visited.add(friend)
                        friends.append(friend)
                        next_level.append(friend)
            current_level = next_level
            if not current_level:
                break

        return friends
    except (TypeError, IndexError, KeyError, ValueError) as error:
        print("Could not get the friend list:", error)
        raise


def save_network(filename: str, sn: dict) -> None:
    """Save a social network dictionary to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["username", "full_name", "friends"])
            for username in sorted(sn):
                full_name, friends = sn[username]
                writer.writerow([username, full_name] + friends)
    except (OSError, csv.Error, TypeError, ValueError) as error:
        print("Could not save the social network:", error)
        raise


def load_network(filename: str) -> dict:
    """Load and return a social network saved by save_network."""
    try:
        social_network = {}
        with open(filename, "r", newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)
            if header != ["username", "full_name", "friends"]:
                raise ValueError("the CSV file has an invalid heading")

            for row in reader:
                if len(row) < 2:
                    raise ValueError("the CSV file has an invalid row")
                social_network[row[0]] = (row[1], row[2:])

        return social_network
    except (OSError, csv.Error, StopIteration, ValueError) as error:
        print("Could not load the social network:", error)
        raise


def main() -> None:
    """Build the sample network and test all required functions."""
    try:
        social_network = {
            "alice": ("Alice Smith", ["maria"]),
            "maria": ("Maria Cortez", ["alice", "joe", "david"]),
            "joe": ("Joseph Adams", ["maria", "eve"]),
            "eve": ("Evelyn Cooper", ["joe"]),
            "david": ("David Benson", ["maria"])
        }

        print("Emir Koyuncu")
        print("Add user:", add_user(social_network,
                                    "carol", "Carol Franklin"))
        print("Add friend:", add_friend(social_network, "carol", "eve"))
        print("Alice's friends at distance 1:",
              get_friends(social_network, "alice", 1))
        print("Alice's friends at distance 2:",
              get_friends(social_network, "alice", 2))

        filename = os.path.join(os.path.dirname(__file__), "social_network.csv")
        save_network(filename, social_network)
        print("Saved network:", filename)
        print("Loaded network:", load_network(filename))
    except (OSError, csv.Error, TypeError, ValueError) as error:
        print("Problem 3 could not be completed:", error)
        raise


if __name__ == "__main__":
    main()
