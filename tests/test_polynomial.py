import unittest
from fraction import Fraction
from polynomial import Polynomial


class TestPolynomial(unittest.TestCase):
    """тестирование многочленов"""

    def test_empty_polynomial(self):
        """пустой многочлен"""
        p = Polynomial()
        self.assertTrue(p.is_zero())
        self.assertEqual(p.degree(), -1)

    def test_polynomial_with_terms(self):
        """многочлен с членами"""
        p = Polynomial({2: 3, 1: 2, 0: 1})
        self.assertEqual(p.coefficient(2), Fraction(3, 1))
        self.assertEqual(p.coefficient(1), Fraction(2, 1))
        self.assertEqual(p.coefficient(0), Fraction(1, 1))

    def test_add_term(self):
        """добавление члена"""
        p = Polynomial({2: 3})
        p.add_term(1, 2)
        self.assertEqual(p.coefficient(2), Fraction(3, 1))
        self.assertEqual(p.coefficient(1), Fraction(2, 1))

    def test_addition(self):
        """сложение многочленов"""
        p1 = Polynomial({2: 3, 1: 2, 0: 1})
        p2 = Polynomial({1: 1, 0: 1})
        result = p1 + p2
        self.assertEqual(result.coefficient(2), Fraction(3, 1))
        self.assertEqual(result.coefficient(1), Fraction(3, 1))
        self.assertEqual(result.coefficient(0), Fraction(2, 1))

    def test_subtraction(self):
        """вычитание многочленов"""
        p1 = Polynomial({2: 3, 1: 2, 0: 1})
        p2 = Polynomial({1: 1, 0: 1})
        result = p1 - p2
        self.assertEqual(result.coefficient(2), Fraction(3, 1))
        self.assertEqual(result.coefficient(1), Fraction(1, 1))
        self.assertEqual(result.coefficient(0), Fraction(0, 1))

    def test_multiplication(self):
        """умножение многочленов"""
        p1 = Polynomial({2: 3, 1: 2, 0: 1})
        p2 = Polynomial({1: 1, 0: 1})
        result = p1 * p2
        self.assertEqual(result.degree(), 3)

    def test_division(self):
        """деление многочленов"""
        p1 = Polynomial({2: 3, 1: 2, 0: 1})
        p2 = Polynomial({1: 1, 0: 1})
        quotient, remainder = p1.divide_with_remainder(p2)
        self.assertEqual(quotient.coefficient(1), Fraction(3, 1))
        self.assertEqual(quotient.coefficient(0), Fraction(-1, 1))