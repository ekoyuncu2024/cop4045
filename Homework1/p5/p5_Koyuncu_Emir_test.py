"""Unit tests for the Caesar cipher homework functions."""

import unittest

from p5_Koyuncu_Emir import caesar_cipher, caesar_decipher, letter_frequency


class CaesarCipherTest(unittest.TestCase):
    """Check encryption, decryption, and letter counting."""

    def test_cipher_preserves_case_and_nonletters(self):
        self.assertEqual(caesar_cipher("Hello, World! 123", 3),
                         "Khoor, Zruog! 123")

    def test_cipher_wraps_around(self):
        self.assertEqual(caesar_cipher("XyZ xyz", 3), "AbC abc")

    def test_cipher_negative_shift(self):
        self.assertEqual(caesar_cipher("AbC", -2), "YzA")

    def test_cipher_large_shift(self):
        self.assertEqual(caesar_cipher("AbZ", 53), "BcA")
        self.assertEqual(caesar_cipher("AbZ", -53), "ZaY")

    def test_cipher_zero_shift(self):
        self.assertEqual(caesar_cipher("Hello!", 0), "Hello!")

    def test_decipher_known_message(self):
        self.assertEqual(caesar_decipher("Khoor, Zruog! 123", 3),
                         "Hello, World! 123")

    def test_cipher_and_decipher_round_trip(self):
        message = "A Zebra!\nTwo\tlines, 123."
        for shift in [-53, -3, 0, 3, 26, 53]:
            with self.subTest(shift=shift):
                ciphertext = caesar_cipher(message, shift)
                self.assertEqual(caesar_decipher(ciphertext, shift), message)

    def test_empty_cipher_and_decipher(self):
        self.assertEqual(caesar_cipher("", 3), "")
        self.assertEqual(caesar_decipher("", 3), "")

    def test_letter_frequency_ignores_case_and_nonletters(self):
        expected = dict.fromkeys("abcdefghijklmnopqrstuvwxyz", 0)
        expected["a"] = 3
        expected["b"] = 2
        expected["z"] = 1
        self.assertEqual(letter_frequency("AaA, bB! Z 123\n"), expected)

    def test_letter_frequency_all_letters(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.assertEqual(letter_frequency(alphabet + alphabet.upper()),
                         dict.fromkeys(alphabet, 2))

    def test_letter_frequency_empty_or_nonletters(self):
        expected = dict.fromkeys("abcdefghijklmnopqrstuvwxyz", 0)
        self.assertEqual(letter_frequency(""), expected)
        self.assertEqual(letter_frequency("123 !?\n\t"), expected)


if __name__ == "__main__":
    unittest.main()
