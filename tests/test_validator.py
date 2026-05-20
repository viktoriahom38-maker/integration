import unittest
from validator import validate


class TestValidator(unittest.TestCase):
    """тестирование валидатора"""

    def test_valid_expression(self):
        """корректное выражение"""
        try:
            validate("2*x+3", "x")
        except ValueError:
            self.fail("валидатор выдал ошибку на корректном выражении")

    def test_invalid_symbol(self):
        """недопустимый символ"""
        with self.assertRaises(ValueError):
            validate("2@x+3", "x")

    def test_unbalanced_brackets_open(self):
        """несбалансированные скобки (открывающая лишняя)"""
        with self.assertRaises(ValueError):
            validate("(2*x+3", "x")

    def test_unbalanced_brackets_close(self):
        """несбалансированные скобки (закрывающая лишняя)"""
        with self.assertRaises(ValueError):
            validate("2*x+3)", "x")

    def test_double_operator_plus(self):
        """два оператора подряд (плюс)"""
        with self.assertRaises(ValueError):
            validate("2++3", "x")

    def test_double_operator_minus(self):
        """два оператора подряд (минус)"""
        with self.assertRaises(ValueError):
            validate("2--3", "x")

    def test_starts_with_operator(self):
        """выражение начинается с оператора"""
        with self.assertRaises(ValueError):
            validate("*2*x", "x")

    def test_ends_with_operator(self):
        """выражение заканчивается оператором"""
        with self.assertRaises(ValueError):
            validate("2*x+", "x")

    def test_negative_power(self):
        """отрицательная степень"""
        with self.assertRaises(ValueError):
            validate("x^-2", "x")

    def test_decimal_fraction(self):
        """десятичная дробь"""
        with self.assertRaises(ValueError):
            validate("2.5*x", "x")

    def test_multiple_division(self):
        """несколько знаков деления"""
        with self.assertRaises(ValueError):
            validate("1/2/3", "x")

    def test_valid_function(self):
        """корректное имя функции"""
        try:
            validate("sin(x)", "x")
        except ValueError:
            self.fail("валидатор выдал ошибку на корректной функции")

    def test_invalid_function(self):
        """некорректное имя функции"""
        with self.assertRaises(ValueError):
            validate("invalid(x)", "x")


    def test_power_with_non_digit(self):
        """степень с нецифрой"""
        with self.assertRaises(ValueError):
            validate("x^(2x)", "x")