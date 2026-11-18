
import unittest

from clean_products import normalize_price


class EdgeCaseTests(unittest.TestCase):

    def test_czech_price_format(self):
        self.assertEqual(normalize_price("1 299,50 Kč"), "1299.50")

    def test_negative_price_is_rejected(self):
        self.assertEqual(normalize_price("-100"), "")

    def test_invalid_price_is_rejected(self):
        self.assertEqual(normalize_price("abc"), "")

    def test_empty_price_is_rejected(self):
        self.assertEqual(normalize_price(""), "")

    def test_nan_price_is_rejected(self):
        self.assertEqual(normalize_price("NaN"), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
