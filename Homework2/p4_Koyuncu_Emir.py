"""Homework 2, Problem 4: Analyze IMDB movie CSV files."""

import csv
import os


def read_movie_keys(filename):
    """Return the title and year pairs stored in a headed movie CSV file."""
    movie_keys = set()
    with open(filename, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            movie_keys.add((row["Title"], row["Year"]))
    return movie_keys


def read_casts(filename):
    """Return cast rows indexed by each movie's title and year."""
    casts = {}
    with open(filename, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) >= 8:
                casts[(row[0], row[1])] = (row[2], row[3:8])
    return casts


def read_box_office(filename):
    """Return box-office amounts indexed by movie title and year."""
    box_office = {}
    with open(filename, "r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            money = row["USA Box Office"].replace("$", "").replace(",", "")
            box_office[(row["Title"], row["Year"])] = float(money)
    return box_office


def display_ranking(title, ranking, limit=None):
    """Display a ranking, optionally limited to its first entries."""
    print(title)
    displayed_ranking = ranking if limit is None else ranking[:limit]
    for number, entry in enumerate(displayed_ranking, start=1):
        print("{}. {}".format(number, entry))


def display_top_collaborations(casts_filename, rated_filename, limit=None):
    """Display director-actor pairs ranked by top-rated collaborations."""
    rated_movies = read_movie_keys(rated_filename)
    casts = read_casts(casts_filename)
    collaborations = {}

    for movie in rated_movies:
        if movie in casts:
            director, actors = casts[movie]
            for actor in actors:
                pair = (director, actor)
                collaborations[pair] = collaborations.get(pair, 0) + 1

    ranking = [(director, actor, count)
               for (director, actor), count in collaborations.items()]
    ranking.sort(key=lambda entry: (-entry[2], entry[0], entry[1]))
    display_ranking("Top director-actor collaborations:", ranking, limit)
    return ranking


def display_top_actors(casts_filename, grossing_filename, limit=None):
    """Display actors ranked by total box office from top-grossing movies."""
    box_office = read_box_office(grossing_filename)
    casts = read_casts(casts_filename)
    actor_totals = {}

    for movie, money in box_office.items():
        if movie in casts:
            unused_director, actors = casts[movie]
            for actor in actors:
                actor_totals[actor] = actor_totals.get(actor, 0.0) + money

    ranking = [(money, actor) for actor, money in actor_totals.items()]
    ranking.sort(key=lambda entry: (-entry[0], entry[1]))
    printable_ranking = [(actor, "${:,.0f}".format(money))
                         for money, actor in ranking]
    display_ranking("Top actors by total USA box office:",
                    printable_ranking, limit)
    return ranking


def main():
    """Display the first ten entries in both requested rankings."""
    folder = os.path.dirname(os.path.abspath(__file__))
    casts_filename = os.path.join(folder, "imdb-top-casts.csv")
    rated_filename = os.path.join(folder, "imdb-top-rated.csv")
    grossing_filename = os.path.join(folder, "imdb-top-grossing.csv")

    print("Emir Koyuncu")
    display_top_collaborations(casts_filename, rated_filename, 10)
    print()
    display_top_actors(casts_filename, grossing_filename, 10)


if __name__ == "__main__":
    main()
