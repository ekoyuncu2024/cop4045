"""Encrypt, decrypt, and count letters in messages using a Caesar cipher."""


def caesar_cipher(text, shift):
    """Return text with English letters shifted, preserving other characters.

    Args:
        text: The message to encrypt.
        shift: The integer number of alphabet positions to shift.

    Returns:
        The encrypted message with its original capitalization.
    """
    lowercase = "abcdefghijklmnopqrstuvwxyz"
    uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encrypted = ""

    for character in text:
        if character in lowercase:
            index = lowercase.index(character)
            encrypted += lowercase[(index + shift) % 26]
        elif character in uppercase:
            index = uppercase.index(character)
            encrypted += uppercase[(index + shift) % 26]
        else:
            encrypted += character

    return encrypted


def caesar_decipher(cyphertext, shift):
    """Return the clear text by reversing the given integer shift."""
    return caesar_cipher(cyphertext, -shift)


def letter_frequency(text):
    """Return counts for a-z, ignoring case and non-English-letter characters."""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies = {}

    for letter in alphabet:
        frequencies[letter] = 0

    for character in text:
        letter = character.lower()
        if letter in frequencies:
            frequencies[letter] += 1

    return frequencies


def main():
    """Run an interactive menu for encrypting and deciphering messages."""
    while True:
        print("\nCaesar Cipher Menu")
        print("1. Encrypt and decipher a message")
        print("2. Quit")
        choice = input("Enter your choice: ").strip()

        if choice == "2":
            print("Goodbye!")
            break
        if choice != "1":
            print("Please enter 1 or 2.")
            continue

        message = input("Enter a message: ")
        while True:
            try:
                shift = int(input("Enter an integer shift: "))
                break
            except ValueError:
                print("Please enter a valid integer.")

        ciphertext = caesar_cipher(message, shift)
        print("Ciphered text:", ciphertext)
        print("Letter frequencies in the ciphered text:")
        frequencies = letter_frequency(ciphertext)
        for letter in frequencies:
            print(f"{letter}: {frequencies[letter]}")
        print("Deciphered text:", caesar_decipher(ciphertext, shift))


if __name__ == "__main__":
    main()
