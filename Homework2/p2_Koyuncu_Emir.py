"""Homework 2, Problem 2: List and dictionary comprehensions."""


def main():
    """Create and display the requested comprehension results."""
    number_tuples = [(a, b, c, d)
                     for a in range(1, 11)
                     for b in range(1, 11)
                     for c in range(1, 11)
                     for d in range(1, 11)
                     if len({a, b, c, d}) == 4
                     and a**2 + b**2 == c**2 + d**2]

    words = ["One", "SEVEN", "three", "two", "Ten"]
    short_words = [(word.lower(), len(word))
                   for word in words if len(word) < 5]

    names = ["Christopher Ashton Kutcher", "Elizabeth Stamatina Fey"]
    abbreviated_names = [name.split()[0] + " " + name.split()[1][0]
                         + ". " + name.split()[2]
                         for name in names]

    lst1 = ["Spam", "Trams", "Elbows", "Tops", "Astral"]
    lst2 = ["Bowels", "Sample", "Altars", "Stop", "Course", "Smart"]
    anagram_pairs = [(word1, word2)
                     for word1 in lst1
                     for word2 in lst2
                     if sorted(word1.lower()) == sorted(word2.lower())]

    strings = ["one", "two", "three"]
    string_lengths = {word: len(word) for word in strings}

    text = "Hello world"
    vowel_positions = {index: character
                       for index, character in enumerate(text)
                       if character.lower() in "aeiou"}

    print("Emir Koyuncu")
    print("a)", number_tuples)
    print("b)", short_words)
    print("c)", abbreviated_names)
    print("d)", anagram_pairs)
    print("e)", string_lengths)
    print("f)", vowel_positions)


if __name__ == "__main__":
    main()
