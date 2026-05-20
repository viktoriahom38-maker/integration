"""
Тесты для проверки всех 25 базовых типов интегрирования
"""

from integration import integrate
from formatter import format_output
import unittest


class TestTableIntegrals(unittest.TestCase):
    """тестирование табличных интегралов"""

    def test1(self):
        expr, var, expected = ("1", "x", "∫ (1) dx = x + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test2(self):
        expr, var, expected = ("5", "x", "∫ (5) dx = 5x + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test3(self):
        expr, var, expected = ("x", "x", "∫ (x) dx = 1/2x^2 + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test4(self):
        expr, var, expected = ("x^3", "x", "∫ (x^3) dx = x^4/4 + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test5(self):
        expr, var, expected = ("1/x^2", "x", "∫ (1/x^2) dx = -1/x + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test6(self):
        expr, var, expected = ("1/sqrt(x)", "x", "∫ (1/sqrt(x)) dx = 2*sqrt(x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test7(self):
        expr, var, expected = ("sqrt(x)", "x", "∫ (sqrt(x)) dx = 2/3x^(3/2) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test8(self):
        expr, var, expected = ("1/x", "x", "∫ (1/x) dx = ln|x| + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test9(self):
        expr, var, expected = ("1/(x+3)", "x", "∫ (1/(x+3)) dx = ln|x+3| + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test10(self):
        expr, var, expected = ("1/(x-2)", "x", "∫ (1/(x-2)) dx = ln|x-2| + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test11(self):
        expr, var, expected = ("e^x", "x", "∫ (e^x) dx = e^x + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test12(self):
        expr, var, expected = ("2^x", "x", "∫ (2^x) dx = 2^x/ln(2) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test13(self):
        expr, var, expected = ("cos(x)", "x", "∫ (cos(x)) dx = sin(x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test14(self):
        expr, var, expected = ("cos(2x)", "x", "∫ (cos(2x)) dx = 1/2sin(2x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test15(self):
        expr, var, expected = ("sin(x)", "x", "∫ (sin(x)) dx = -cos(x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test16(self):
        expr, var, expected = ("sin(2x)", "x", "∫ (sin(2x)) dx = -1/2cos(2x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test17(self):
        expr, var, expected = ("1/cos(x)^2", "x", "∫ (1/cos(x)^2) dx = tg(x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test18(self):
        expr, var, expected = ("1/sin(x)^2", "x", "∫ (1/sin(x)^2) dx = -ctg(x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test19(self):
        expr, var, expected = ("1/sqrt(1-x^2)", "x", "∫ (1/sqrt(1-x^2)) dx = arcsin(x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test20(self):
        expr, var, expected = ("1/(1+x^2)", "x", "∫ (1/(1+x^2)) dx = arctg(x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test21(self):
        expr, var, expected = ("tg(x)", "x", "∫ (tg(x)) dx = -ln|cos(x)| + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test22(self):
        expr, var, expected = ("ctg(x)", "x", "∫ (ctg(x)) dx = ln|sin(x)| + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test23(self):
        expr, var, expected = ("e^(2x)", "x", "∫ (e^(2x)) dx = 1/2e^(2x) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test24(self):
        expr, var, expected = ("1/sqrt(9-x^2)", "x", "∫ (1/sqrt(9-x^2)) dx = arcsin(x/3) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test25(self):
        expr, var, expected = ("1/(4+x^2)", "x", "∫ (1/(4+x^2)) dx = 1/2arctg(x/2) + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test26(self):
        expr, var, expected = ("1/(x^2-4)", "x", "∫ (1/(x^2-4)) dx = 1/4ln|(x-2)/(x+2)| + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test27(self):
        expr, var, expected = ("1/sqrt(x^2+4)", "x", "∫ (1/sqrt(x^2+4)) dx = ln|x + sqrt(x^2+4)| + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)

    def test28(self):
        expr, var, expected = ("1/sqrt(x^2-4)", "x", "∫ (1/sqrt(x^2-4)) dx = ln|x + sqrt(x^2-4)| + C")
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        self.assertEqual(output, expected)