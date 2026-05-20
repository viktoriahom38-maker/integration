import unittest
from fraction import Fraction


class TestFraction(unittest.TestCase):
    """тестирование дробей"""

    def test_creation_simple(self):
        """создание простой дроби"""
        f = Fraction(3, 4)
        self.assertEqual(f.numerator, 3)
        self.assertEqual(f.denominator, 4)

    def test_creation_simplify(self):
        """сокращение дроби"""
        f = Fraction(6, 8)
        self.assertEqual(f.numerator, 3)
        self.assertEqual(f.denominator, 4)

    def test_creation_negative(self):
        """отрицательная дробь"""
        f = Fraction(-3, 4)
        self.assertEqual(f.numerator, -3)
        self.assertEqual(f.denominator, 4)

    def test_creation_negative_denominator(self):
        """отрицательный знаменатель"""
        f = Fraction(3, -4)
        self.assertEqual(f.numerator, -3)
        self.assertEqual(f.denominator, 4)

    def test_creation_integer(self):
        """целое число как дробь"""
        f = Fraction(5)
        self.assertEqual(f.numerator, 5)
        self.assertEqual(f.denominator, 1)

    def test_addition(self):
        """сложение дробей"""
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 3)
        result = f1 + f2
        self.assertEqual(result.numerator, 5)
        self.assertEqual(result.denominator, 6)

    def test_subtraction(self):
        """вычитание дробей"""
        f1 = Fraction(3, 4)
        f2 = Fraction(1, 4)
        result = f1 - f2
        self.assertEqual(result.numerator, 1)
        self.assertEqual(result.denominator, 2)

    def test_multiplication(self):
        """умножение дробей"""
        f1 = Fraction(2, 3)
        f2 = Fraction(3, 4)
        result = f1 * f2
        self.assertEqual(result.numerator, 1)
        self.assertEqual(result.denominator, 2)

    def test_division(self):
        """деление дробей"""
        f1 = Fraction(1, 2)
        f2 = Fraction(1, 4)
        result = f1 / f2
        self.assertEqual(result.numerator, 2)
        self.assertEqual(result.denominator, 1)

    def test_add_integer(self):
        """сложение с целым числом"""
        f = Fraction(1, 2)
        result = f + 3
        self.assertEqual(result.numerator, 7)
        self.assertEqual(result.denominator, 2)

    def test_equality(self):
        """равенство дробей"""
        f1 = Fraction(1, 2)
        f2 = Fraction(2, 4)
        self.assertEqual(f1, f2)

    def test_inequality(self):
        """неравенство дробей"""
        f1 = Fraction(1, 2)
        f2 = Fraction(2, 3)
        self.assertNotEqual(f1, f2)

    def test_equality_with_integer(self):
        """равенство с целым числом"""
        f = Fraction(4, 2)
        self.assertEqual(f, 2)