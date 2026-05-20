import unittest
from parser import preprocess, tokenize, build_polynomial_from_expr, parse_to_polynomials
from fraction import Fraction


class TestParser(unittest.TestCase):
    """тестирование парсера"""

    def test_preprocess_multiplication(self):
        """расстановка знаков умножения"""
        result = preprocess("2x+3x", "x")
        self.assertEqual(result, "2*x+3*x")

    def test_preprocess_brackets(self):
        """умножение на скобки"""
        result = preprocess("x(x+1)", "x")
        self.assertEqual(result, "x*(x+1)")

    def test_preprocess_var_var(self):
        """умножение переменной на переменную"""
        result = preprocess("xx", "x")
        self.assertEqual(result, "x*x")

    def test_preprocess_var_paren(self):
        """умножение переменной на скобку"""
        result = preprocess("x(x)", "x")
        self.assertEqual(result, "x*(x)")

    def test_preprocess_paren_var(self):
        """умножение скобки на переменную"""
        result = preprocess("(x)x", "x")
        self.assertEqual(result, "(x)*x")

    def test_preprocess_number_paren(self):
        """умножение числа на скобку"""
        result = preprocess("2(x)", "x")
        self.assertEqual(result, "2*(x)")

    def test_preprocess_remove_spaces(self):
        """удаление пробелов"""
        result = preprocess("2 x + 3 x", "x")
        self.assertEqual(result, "2*x+3*x")

    def test_preprocess_paren_paren(self):
        """скобка на скобку"""
        result = preprocess("(x)(x)", "x")
        self.assertEqual(result, "(x)*(x)")

    def test_tokenize_simple(self):
        """разбиение на токены"""
        result = tokenize("2*x+3", "x")
        self.assertEqual(result, ["2", "*", "x", "+", "3"])

    def test_tokenize_fraction(self):
        """разбиение дроби"""
        result = tokenize("1/2*x", "x")
        self.assertEqual(result, ["1/2", "*", "x"])

    def test_tokenize_with_power(self):
        """разбиение со степенью"""
        result = tokenize("x^2+3", "x")
        self.assertEqual(result, ["x", "^", "2", "+", "3"])

    def test_tokenize_with_parentheses(self):
        """разбиение со скобками"""
        result = tokenize("(x+1)*2", "x")
        self.assertEqual(result, ["(", "x", "+", "1", ")", "*", "2"])

    def test_build_polynomial(self):
        """построение многочлена"""
        poly = build_polynomial_from_expr("2*x^2+3*x+1", "x")
        self.assertEqual(poly.coefficient(2), Fraction(2, 1))
        self.assertEqual(poly.coefficient(1), Fraction(3, 1))
        self.assertEqual(poly.coefficient(0), Fraction(1, 1))

    def test_build_polynomial_simple(self):
        """построение простого многочлена"""
        poly = build_polynomial_from_expr("x^2", "x")
        self.assertEqual(poly.coefficient(2), Fraction(1, 1))

    def test_build_polynomial_constant(self):
        """построение константы"""
        poly = build_polynomial_from_expr("5", "x")
        self.assertEqual(poly.coefficient(0), Fraction(5, 1))

    def test_build_polynomial_x(self):
        """построение переменной"""
        poly = build_polynomial_from_expr("x", "x")
        self.assertEqual(poly.coefficient(1), Fraction(1, 1))

    def test_build_polynomial_negative(self):
        """отрицательный коэффициент"""
        poly = build_polynomial_from_expr("-x^2+2*x-3", "x")
        self.assertEqual(poly.coefficient(2), Fraction(-1, 1))
        self.assertEqual(poly.coefficient(1), Fraction(2, 1))
        self.assertEqual(poly.coefficient(0), Fraction(-3, 1))

    def test_build_polynomial_fraction(self):
        """дробные коэффициенты"""
        poly = build_polynomial_from_expr("1/2*x^2+2/3*x", "x")
        self.assertEqual(poly.coefficient(2), Fraction(1, 2))
        self.assertEqual(poly.coefficient(1), Fraction(2, 3))

    def test_parse_to_polynomials_simple(self):
        """парсинг простой дроби"""
        num, den = parse_to_polynomials("x/2", "x")
        self.assertEqual(num.coefficient(1), Fraction(1, 1))
        self.assertEqual(den.coefficient(0), Fraction(2, 1))

    def test_parse_to_polynomials_no_division(self):
        """парсинг без деления"""
        num, den = parse_to_polynomials("x^2+1", "x")
        self.assertEqual(num.coefficient(2), Fraction(1, 1))
        self.assertEqual(den.coefficient(0), Fraction(1, 1))

    def test_parse_to_polynomials_division_zero(self):
        """деление на ноль"""
        with self.assertRaises(ValueError):
            parse_to_polynomials("1/0", "x")

    def test_preprocess_power_with_parentheses(self):
        """степень в скобках"""
        result = preprocess("x^(2)", "x")
        self.assertEqual(result, "x^(2)")

    def test_preprocess_complex_expression(self):
        """сложное выражение"""
        result = preprocess("2x^2+3x(x+1)", "x")
        self.assertEqual(result, "2*x^2+3*x*(x+1)")

    def test_tokenize_negative_number(self):
        """отрицательное число"""
        result = tokenize("-5*x", "x")
        self.assertEqual(result, ["-", "5", "*", "x"])

    def test_tokenize_power_expression(self):
        """выражение со степенью в скобках"""
        result = tokenize("x^(2)+1", "x")
        self.assertEqual(result, ["x", "^", "(", "2", ")", "+", "1"])

    def test_build_polynomial_with_power_parentheses(self):
        """многочлен со степенью в скобках"""
        poly = build_polynomial_from_expr("x^(2)+2*x+1", "x")
        self.assertEqual(poly.coefficient(2), Fraction(1, 1))
        self.assertEqual(poly.coefficient(1), Fraction(2, 1))
        self.assertEqual(poly.coefficient(0), Fraction(1, 1))

    def test_build_polynomial_with_negative_coefficient(self):
        """отрицательные коэффициенты"""
        poly = build_polynomial_from_expr("-x^3+2*x^2-3*x+4", "x")
        self.assertEqual(poly.coefficient(3), Fraction(-1, 1))
        self.assertEqual(poly.coefficient(2), Fraction(2, 1))
        self.assertEqual(poly.coefficient(1), Fraction(-3, 1))
        self.assertEqual(poly.coefficient(0), Fraction(4, 1))

    def test_build_polynomial_with_fraction_coefficient(self):
        """дробные коэффициенты"""
        poly = build_polynomial_from_expr("1/2*x^2+2/3*x-1/4", "x")
        self.assertEqual(poly.coefficient(2), Fraction(1, 2))
        self.assertEqual(poly.coefficient(1), Fraction(2, 3))
        self.assertEqual(poly.coefficient(0), Fraction(-1, 4))

    def test_build_polynomial_without_mul_sign(self):
        """без знака умножения"""
        poly = build_polynomial_from_expr("2x^2+3x+1", "x")
        self.assertEqual(poly.coefficient(2), Fraction(2, 1))
        self.assertEqual(poly.coefficient(1), Fraction(3, 1))
        self.assertEqual(poly.coefficient(0), Fraction(1, 1))

    def test_build_polynomial_with_variable_power(self):
        """переменная в степени"""
        poly = build_polynomial_from_expr("x^3", "x")
        self.assertEqual(poly.coefficient(3), Fraction(1, 1))

    def test_build_polynomial_constant_without_variable(self):
        """константа без переменной"""
        poly = build_polynomial_from_expr("42", "x")
        self.assertEqual(poly.coefficient(0), Fraction(42, 1))

    def test_build_polynomial_with_parentheses_simple(self):
        """простое выражение в скобках"""
        poly = build_polynomial_from_expr("(x+1)", "x")
        self.assertEqual(poly.coefficient(1), Fraction(1, 1))
        self.assertEqual(poly.coefficient(0), Fraction(1, 1))

    def test_build_polynomial_with_parentheses_multiplication(self):
        """умножение скобок"""
        poly = build_polynomial_from_expr("(x+1)*(x+2)", "x")
        self.assertEqual(poly.coefficient(2), Fraction(1, 1))
        self.assertEqual(poly.coefficient(1), Fraction(3, 1))
        self.assertEqual(poly.coefficient(0), Fraction(2, 1))

    def test_build_polynomial_leading_plus(self):
        """плюс в начале"""
        poly = build_polynomial_from_expr("+x^2+2*x+1", "x")
        self.assertEqual(poly.coefficient(2), Fraction(1, 1))

    def test_build_polynomial_leading_minus(self):
        """минус в начале"""
        poly = build_polynomial_from_expr("-x^2+2*x-1", "x")
        self.assertEqual(poly.coefficient(2), Fraction(-1, 1))

    def test_build_polynomial_empty_expression(self):
        """пустое выражение"""
        poly = build_polynomial_from_expr("", "x")
        self.assertEqual(poly.coefficient(0), Fraction(0, 1))

    def test_parse_to_polynomials_complex_fraction(self):
        """сложная дробь"""
        num, den = parse_to_polynomials("(x^2+1)/(x+1)", "x")
        self.assertEqual(num.coefficient(2), Fraction(1, 1))
        self.assertEqual(den.coefficient(1), Fraction(1, 1))
        self.assertEqual(den.coefficient(0), Fraction(1, 1))

    def test_parse_to_polynomials_with_spaces(self):
        """с пробелами"""
        num, den = parse_to_polynomials(" x^2 + 1 / x + 1 ", "x")
        self.assertIsNotNone(num)
        self.assertIsNotNone(den)

    def test_tokenize_complex_expression(self):
        """сложное выражение для токенизации"""
        result = tokenize("(x+1)*(x-1)", "x")
        self.assertEqual(result, ["(", "x", "+", "1", ")", "*", "(", "x", "-", "1", ")"])

    def test_tokenize_with_power_and_parentheses(self):
        """степень в скобках при токенизации"""
        result = tokenize("x^(2)+x", "x")
        self.assertEqual(result, ["x", "^", "(", "2", ")", "+", "x"])

    def test_build_polynomial_fraction_with_variable_and_power_in_parentheses(self):
        """дробь с переменной и степенью в скобках: 1/2x^(2)"""
        poly = build_polynomial_from_expr("1/2x^(2)", "x")
        self.assertEqual(poly.coefficient(2), Fraction(1, 2))

    def test_build_polynomial_fraction_with_power_in_parentheses(self):
        """дробь со степенью в скобках: 1/2^(2)"""
        poly = build_polynomial_from_expr("1/2^(2)", "x")
        self.assertEqual(poly.coefficient(2), Fraction(1, 2))

    def test_build_polynomial_number_with_power_in_parentheses(self):
        """число со степенью в скобках: 5^(2)"""
        poly = build_polynomial_from_expr("5^(2)", "x")
        self.assertEqual(poly.coefficient(2), Fraction(5, 1))
