import unittest
from integration import integrate, integrate_rational, integrate_polynomial, integrate_linear_denominator
from polynomial import Polynomial
from fraction import Fraction


class TestIntegration(unittest.TestCase):
    """тестирование интегратора"""

    def test_integrate_constant(self):
        """интеграл от константы"""
        result = integrate("5", "x")
        self.assertIsNotNone(result)

    def test_integrate_polynomial(self):
        """интеграл от многочлена"""
        result = integrate("x^2+2*x+1", "x")
        self.assertIsNotNone(result)

    def test_integrate_rational_simple(self):
        """интеграл от простой дроби"""
        result = integrate("1/x", "x")
        self.assertIsNotNone(result)

    def test_integrate_rational_linear(self):
        """интеграл от линейной дроби"""
        result = integrate("1/(x+3)", "x")
        self.assertIsNotNone(result)

    def test_integrate_elementary(self):
        """интеграл от элементарной функции"""
        result = integrate("sin(x)", "x")
        self.assertIsNotNone(result)

    def test_integrate_elementary_exp(self):
        """интеграл от экспоненты"""
        result = integrate("e^x", "x")
        self.assertIsNotNone(result)

    def test_integrate_invalid_variable(self):
        """недопустимая переменная"""
        with self.assertRaises(ValueError):
            result = integrate("x^2", "y")

    def test_integrate_rational_function(self):
        """интеграл от рациональной функции"""
        result = integrate("(x+1)/(x-1)", "x")
        self.assertIsNotNone(result)

    def test_integrate_quadratic_denominator(self):
        """интеграл с квадратным знаменателем"""
        result = integrate("1/(x^2+1)", "x")
        self.assertIsNotNone(result)

    def test_integrate_polynomial_function(self):
        """интеграл от полинома"""
        poly = Polynomial({3: Fraction(1, 1), 1: Fraction(2, 1)})
        result = integrate_polynomial(poly, "x")
        self.assertEqual(len(result[0]), 2)

    def test_integrate_polynomial_empty(self):
        """интеграл от пустого полинома"""
        poly = Polynomial()
        result = integrate_polynomial(poly, "x")
        self.assertEqual(result, ([], []))

    def test_integrate_linear_denominator(self):
        """интеграл от линейного знаменателя"""
        num = Polynomial({0: Fraction(1, 1)})
        den = Polynomial({1: Fraction(1, 1), 0: Fraction(1, 1)})
        result = integrate_linear_denominator(num, den, "x")
        self.assertIsNotNone(result)

    def test_integrate_linear_denominator_with_constant(self):
        """интеграл от линейного знаменателя с константой"""
        num = Polynomial({0: Fraction(5, 1)})
        den = Polynomial({1: Fraction(2, 1), 0: Fraction(1, 1)})
        result = integrate_linear_denominator(num, den, "x")
        self.assertIsNotNone(result)

    def test_integrate_rational_with_division_by_zero(self):
        """деление на ноль"""
        num = Polynomial({1: Fraction(1, 1)})
        den = Polynomial({0: Fraction(0, 1)})
        result = integrate_rational(num, den, "x")
        self.assertEqual(result, "Ошибка: знаменатель не может быть равен нулю")

    def test_integrate_rational_denominator_zero(self):
        """знаменатель равен нулю"""
        num = Polynomial({0: Fraction(1, 1)})
        den = Polynomial({0: Fraction(0, 1)})
        result = integrate_rational(num, den, "x")
        self.assertEqual(result, "Ошибка: знаменатель не может быть равен нулю")

    def test_integrate_rational_high_degree(self):
        """знаменатель высокой степени"""
        num = Polynomial({0: Fraction(1, 1)})
        den = Polynomial({3: Fraction(1, 1)})
        result = integrate_rational(num, den, "x")
        self.assertEqual(result, "Эта функция не интегрируется в рамках задачи на данный момент")

    def test_integrate_quadratic_denominator_positive(self):
        """квадратный знаменатель с положительным c"""
        num = Polynomial({0: Fraction(1, 1)})
        den = Polynomial({2: Fraction(1, 1), 0: Fraction(4, 1)})
        result = integrate_rational(num, den, "x")
        self.assertIsNotNone(result)

    def test_integrate_quadratic_denominator_with_b(self):
        """квадратный знаменатель с линейным членом"""
        num = Polynomial({0: Fraction(1, 1)})
        den = Polynomial({2: Fraction(1, 1), 1: Fraction(1, 1), 0: Fraction(1, 1)})
        result = integrate_rational(num, den, "x")
        self.assertEqual(result, "Эта функция не интегрируется в рамках задачи на данный момент")

    def test_integrate_rational_constant_denominator(self):
        """постоянный знаменатель"""
        num = Polynomial({1: Fraction(1, 1), 0: Fraction(2, 1)})
        den = Polynomial({0: Fraction(5, 1)})
        result = integrate_rational(num, den, "x")
        self.assertIsNotNone(result)
