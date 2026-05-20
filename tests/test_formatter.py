import unittest
from fraction import Fraction
from formatter import _term_to_string, _log_to_string, format_output, format_elementary_result


class TestFormatter(unittest.TestCase):
    """тестирование форматтера"""

    def test_term_to_string_simple(self):
        """простой член"""
        result = _term_to_string(Fraction(3, 1), 2, "x")
        self.assertEqual(result, "3x^2")

    def test_term_to_string_one(self):
        """коэффициент 1"""
        result = _term_to_string(Fraction(1, 1), 1, "x")
        self.assertEqual(result, "x")

    def test_term_to_string_negative_one(self):
        """коэффициент -1"""
        result = _term_to_string(Fraction(-1, 1), 1, "x")
        self.assertEqual(result, "-x")

    def test_term_to_string_fraction(self):
        """дробный коэффициент"""
        result = _term_to_string(Fraction(1, 2), 1, "x")
        self.assertEqual(result, "1/2x")

    def test_term_to_string_degree_zero(self):
        """нулевая степень"""
        result = _term_to_string(Fraction(3, 1), 0, "x")
        self.assertEqual(result, "3")

    def test_term_to_string_degree_one(self):
        """первая степень"""
        result = _term_to_string(Fraction(2, 1), 1, "x")
        self.assertEqual(result, "2x")

    def test_term_to_string_degree_zero_with_one(self):
        """нулевая степень с коэффициентом 1"""
        result = _term_to_string(Fraction(1, 1), 0, "x")
        self.assertEqual(result, "1")

    def test_term_to_string_negative_fraction(self):
        """отрицательный дробный коэффициент"""
        result = _term_to_string(Fraction(-1, 2), 2, "x")
        self.assertEqual(result, "-1/2x^2")

    def test_log_to_string_simple(self):
        """простой логарифм"""
        result = _log_to_string(Fraction(2, 1), "x+1")
        self.assertEqual(result, "2*ln|x+1|")

    def test_log_to_string_one(self):
        """коэффициент 1"""
        result = _log_to_string(Fraction(1, 1), "x")
        self.assertEqual(result, "ln|x|")

    def test_log_to_string_negative_one(self):
        """коэффициент -1"""
        result = _log_to_string(Fraction(-1, 1), "x")
        self.assertEqual(result, "-ln|x|")

    def test_log_to_string_fraction(self):
        """дробный коэффициент"""
        result = _log_to_string(Fraction(1, 2), "x")
        self.assertEqual(result, "1/2*ln|x|")

    def test_log_to_string_negative_fraction(self):
        """отрицательный дробный коэффициент"""
        result = _log_to_string(Fraction(-1, 2), "x+1")
        self.assertEqual(result, "-1/2*ln|x+1|")

    def test_format_output_string_result(self):
        """строковый результат"""
        result = format_output("1/x", "ln|x|", "x")
        self.assertEqual(result, "∫ (1/x) dx = ln|x| + C")

    def test_format_output_error(self):
        """сообщение об ошибке"""
        result = format_output("1/x", "Ошибка", "x")
        self.assertEqual(result, "∫ (1/x) dx = Ошибка")

    def test_format_output_not_integrable(self):
        """сообщение о неинтегрируемости"""
        result = format_output("1/x", "не интегрируется", "x")
        self.assertEqual(result, "∫ (1/x) dx = не интегрируется")

    def test_format_output_zero(self):
        """нулевой результат"""
        result = format_output("0", "0", "x")
        self.assertEqual(result, "∫ (0) dx = 0 + C")

    def test_format_output_with_poly_terms(self):
        """результат с полиномиальными членами"""
        poly_terms = [(Fraction(1, 3), 3), (Fraction(1, 2), 2)]
        log_terms = []
        result = format_output("x^2+x", (poly_terms, log_terms), "x")
        self.assertIn("x^3", result)
        self.assertIn("1/2x^2", result)

    def test_format_output_with_log_terms(self):
        """результат с логарифмическими членами"""
        poly_terms = []
        log_terms = [(Fraction(1, 1), "x")]
        result = format_output("1/x", (poly_terms, log_terms), "x")
        self.assertIn("ln|x|", result)

    def test_format_elementary_result_simple(self):
        """форматирование элементарного результата"""
        terms = [(Fraction(1, 1), "x")]
        log_terms = []
        result = format_elementary_result(terms, log_terms, "x")
        self.assertEqual(result, "x")

    def test_format_elementary_result_multiple(self):
        """форматирование нескольких членов"""
        terms = [(Fraction(2, 1), "x^2"), (Fraction(1, 1), "x")]
        log_terms = [(Fraction(1, 1), "x")]
        result = format_elementary_result(terms, log_terms, "x")
        self.assertIn("2x^2", result)
        self.assertIn("x", result)

    def test_format_elementary_result_empty(self):
        """пустой результат"""
        result = format_elementary_result([], [], "x")
        self.assertEqual(result, "0")

    def test_format_elementary_result_with_logs_only(self):
        """только логарифмические члены"""
        terms = []
        log_terms = [(Fraction(1, 1), "x")]
        result = format_elementary_result(terms, log_terms, "x")
        self.assertEqual(result, "ln|x|")

    def test_format_elementary_result_with_both(self):
        """смешанные члены"""
        terms = [(Fraction(2, 1), "x^2"), (Fraction(-1, 1), "x")]
        log_terms = [(Fraction(1, 2), "x")]
        result = format_elementary_result(terms, log_terms, "x")
        self.assertIn("2x^2", result)
        self.assertIn("-x", result)
        self.assertIn("1/2ln|x|", result)

    def test_format_integral_result_empty(self):
        """пустой результат"""
        from formatter import format_integral_result
        result = format_integral_result([], [], "x")
        self.assertEqual(result, "0")

    def test_format_linear_expression_positive(self):
        """линейное выражение с положительными коэффициентами"""
        from formatter import format_linear_expression
        result = format_linear_expression(Fraction(2, 1), Fraction(3, 1), "x")
        self.assertEqual(result, "2x+3")

    def test_format_linear_expression_negative(self):
        """линейное выражение с отрицательными коэффициентами"""
        from formatter import format_linear_expression
        result = format_linear_expression(Fraction(-2, 1), Fraction(-3, 1), "x")
        self.assertEqual(result, "(-2)x-3")

    def test_format_linear_expression_zero_a(self):
        """нулевой коэффициент при переменной"""
        from formatter import format_linear_expression
        result = format_linear_expression(Fraction(0, 1), Fraction(5, 1), "x")
        self.assertEqual(result, "5")

    def test_format_linear_expression_zero_b(self):
        """нулевой свободный член"""
        from formatter import format_linear_expression
        result = format_linear_expression(Fraction(3, 1), Fraction(0, 1), "x")
        self.assertEqual(result, "3x")