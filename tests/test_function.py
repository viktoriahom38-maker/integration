import unittest
from fraction import Fraction
from function import Function, SumFunction, ProductFunction, NegateFunction


class TestFunction(unittest.TestCase):
    """тестирование класса Function и вспомогательных классов"""

    def test_function_creation_sin(self):
        """создание функции sin"""
        f = Function("sin", "x")
        self.assertEqual(f.name, "sin")
        self.assertEqual(f.argument, "x")
        self.assertEqual(f.coefficient, Fraction(1, 1))

    def test_function_creation_with_coefficient(self):
        """создание функции с коэффициентом"""
        f = Function("cos", "x", Fraction(2, 1))
        self.assertEqual(f.coefficient, Fraction(2, 1))

    def test_function_copy(self):
        """копирование функции"""
        f = Function("ln", "x", Fraction(3, 1))
        f_copy = f.copy()
        self.assertEqual(f.name, f_copy.name)
        self.assertEqual(f.argument, f_copy.argument)
        self.assertEqual(f.coefficient, f_copy.coefficient)

    def test_function_mul_by_number(self):
        """умножение функции на число"""
        f = Function("sin", "x")
        result = f * 2
        self.assertEqual(result.coefficient, Fraction(2, 1))

    def test_function_mul_by_fraction(self):
        """умножение функции на дробь"""
        f = Function("cos", "x")
        result = f * Fraction(1, 2)
        self.assertEqual(result.coefficient, Fraction(1, 2))

    def test_function_rmul(self):
        """умножение числа на функцию"""
        f = Function("sin", "x")
        result = 3 * f
        self.assertEqual(result.coefficient, Fraction(3, 1))

    def test_function_mul_by_function(self):
        """умножение двух функций (создание ProductFunction)"""
        f1 = Function("sin", "x")
        f2 = Function("cos", "x")
        result = f1 * f2
        self.assertIsInstance(result, ProductFunction)

    def test_function_add_zero(self):
        """сложение функции с нулем"""
        f = Function("sin", "x")
        result = f + 0
        self.assertEqual(result, f)

    def test_function_add_number(self):
        """сложение функции с числом (создание SumFunction)"""
        f = Function("sin", "x")
        result = f + 2
        self.assertIsInstance(result, SumFunction)

    def test_function_sub(self):
        """вычитание функции"""
        f = Function("sin", "x")
        result = f - 2
        self.assertIsInstance(result, SumFunction)

    def test_function_neg(self):
        """унарный минус"""
        f = Function("sin", "x")
        result = -f
        self.assertEqual(result.coefficient, Fraction(-1, 1))

    def test_function_repr_zero_coefficient(self):
        """строковое представление с нулевым коэффициентом"""
        f = Function("sin", "x", Fraction(0, 1))
        self.assertEqual(str(f), "0")

    def test_function_repr_sin(self):
        """строковое представление sin(x)"""
        f = Function("sin", "x")
        self.assertEqual(str(f), "sin(x)")

    def test_function_repr_sin_with_coefficient(self):
        """строковое представление 2*sin(x)"""
        f = Function("sin", "x", Fraction(2, 1))
        self.assertEqual(str(f), "2sin(x)")

    def test_function_repr_cos(self):
        """строковое представление cos(x)"""
        f = Function("cos", "x")
        self.assertEqual(str(f), "cos(x)")

    def test_function_repr_ln(self):
        """строковое представление ln|x|"""
        f = Function("ln", "x")
        self.assertEqual(str(f), "ln|x|")

    def test_function_repr_exp(self):
        """строковое представление e^x"""
        f = Function("exp", "x")
        self.assertEqual(str(f), "e^x")

    def test_function_repr_exp_with_argument(self):
        """строковое представление e^(2x)"""
        f = Function("exp", "2x")
        self.assertEqual(str(f), "e^(2x)")

    def test_function_repr_sqrt(self):
        """строковое представление sqrt(x)"""
        f = Function("sqrt", "x")
        self.assertEqual(str(f), "sqrt(x)")

    def test_function_repr_poly(self):
        """строковое представление полинома"""
        f = Function("poly", "x^2")
        self.assertEqual(str(f), "x^2")

    def test_function_repr_negative_coefficient(self):
        """строковое представление с отрицательным коэффициентом"""
        f = Function("sin", "x", Fraction(-1, 1))
        self.assertEqual(str(f), "-sin(x)")

    def test_sum_function_repr(self):
        """строковое представление суммы"""
        f1 = Function("sin", "x")
        f2 = Function("cos", "x")
        s = SumFunction(f1, f2)
        self.assertEqual(str(s), "sin(x) + cos(x)")

    def test_sum_function_repr_negative_right(self):
        """строковое представление суммы с отрицательным правым членом"""
        f1 = Function("sin", "x")
        f2 = Function("cos", "x", Fraction(-1, 1))
        s = SumFunction(f1, f2)
        self.assertEqual(str(s), "sin(x) -cos(x)")

    def test_product_function_repr(self):
        """строковое представление произведения"""
        f1 = Function("sin", "x")
        f2 = Function("cos", "x")
        p = ProductFunction(f1, f2)
        self.assertEqual(str(p), "sin(x)cos(x)")

    def test_product_function_repr_with_poly(self):
        """строковое представление с полиномом"""
        f1 = Function("poly", "x^2")
        f2 = Function("sin", "x")
        p = ProductFunction(f1, f2)
        self.assertEqual(str(p), "x^2*sin(x)")

    def test_negate_function_repr(self):
        """строковое представление отрицательной функции"""
        f = Function("sin", "x")
        n = NegateFunction(f)
        self.assertEqual(str(n), "-sin(x)")


if __name__ == "__main__":
    unittest.main()
