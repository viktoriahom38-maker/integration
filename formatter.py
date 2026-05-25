from typing import List, Tuple
from fraction import Fraction


def format_output(original_expr: str, result: str | Tuple[List, List], variable: str) -> str:
    """
    Формирует итоговую строку вывода интеграла

    original_expr - исходное выражение пользователя
    result - результат интегрирования
    variable - переменная интегрирования

    возвращает форматированную строку
    """
    if isinstance(result, str):
        if "Ошибка" in result or "не интегрируется" in result:
            return f"∫ ({original_expr}) d{variable} = {result}"
        return f"∫ ({original_expr}) d{variable} = {result} + C"

    poly_terms, log_terms = result

    if isinstance(poly_terms, list) and len(poly_terms) > 0 and isinstance(poly_terms[0], tuple):
        if len(poly_terms[0]) == 2 and isinstance(poly_terms[0][1], int):
            result_str = format_integral_result(poly_terms, log_terms, variable)
            return f"∫ ({original_expr}) d{variable} = {result_str} + C"

    if not poly_terms and not log_terms:
        return f"∫ ({original_expr}) d{variable} = 0 + C"

    result_str = format_elementary_result(poly_terms, log_terms, variable)
    return f"∫ ({original_expr}) d{variable} = {result_str} + C"


def format_elementary_result(terms: list, log_terms: list, variable: str) -> str:
    """Форматирует результат для элементарных функций"""
    parts = []
    for coef, func in terms:
        if isinstance(coef, Fraction):
            if coef.numerator == 1 and coef.denominator == 1:
                coef_str = ""
            elif coef.numerator == -1 and coef.denominator == 1:
                coef_str = "-"
            else:
                coef_str = str(coef)
        else:
            if coef == 1:
                coef_str = ""
            elif coef == -1:
                coef_str = "-"
            else:
                coef_str = str(coef)
        parts.append(f"{coef_str}{func}")
    for coef, arg in log_terms:
        if isinstance(coef, Fraction):
            if coef.numerator == 1 and coef.denominator == 1:
                coef_str = ""
            elif coef.numerator == -1 and coef.denominator == 1:
                coef_str = "-"
            else:
                coef_str = str(coef)
        else:
            if coef == 1:
                coef_str = ""
            elif coef == -1:
                coef_str = "-"
            else:
                coef_str = str(coef)
        parts.append(f"{coef_str}ln|{arg}|")
    if not parts:
        return "0"
    result = parts[0]
    for p in parts[1:]:
        if p.startswith('-'):
            result += " " + p
        else:
            result += " + " + p
    return result


def format_integral_result(terms: List[Tuple[Fraction, int]], log_terms: List[Tuple[Fraction, str]], variable: str) -> str:
    """Преобразует списки членов результата в единую строку"""
    parts = []
    terms.sort(key=lambda x: x[1], reverse=True)

    for coef, degree in terms:
        if coef.numerator == 0:
            continue
        parts.append(_term_to_string(coef, degree, variable))

    for coef, arg in log_terms:
        if coef.numerator == 0:
            continue
        parts.append(_log_to_string(coef, arg))

    if not parts:
        return "0"

    result = parts[0]
    for p in parts[1:]:
        if p.startswith('-'):
            result += " " + p
        else:
            result += " + " + p

    return result


def format_linear_expression(a: Fraction, b: Fraction, var: str) -> str:
    """
    Форматирует линейное выражение ax + b для использования внутри логарифма

    a - коэффициент при переменной
    b - свободный член
    var - переменная

    возвращает строку вида "x", "2x+1", т.д.
    """
    if a.numerator == 0:
        return str(b)

    if a.numerator == 1 and a.denominator == 1:
        a_str = var
    elif a.numerator == -1 and a.denominator == 1:
        a_str = f"-{var}"
    elif a.numerator > 1 and a.denominator == 1:
        a_str = f"{a}{var}"
    else:
        a_str = f"({a}){var}"

    if b.numerator == 0:
        return a_str
    elif b.numerator > 0:
        return f"{a_str}+{b}"
    else:
        return f"{a_str}{b}"


def _term_to_string(coef: Fraction, degree: int, var: str) -> str:
    """Форматирует один член многочлена Ax^n"""
    if coef.numerator == 0:
        return ""

    sign = "-" if coef.numerator < 0 else ""
    abs_n = abs(coef.numerator)
    abs_d = coef.denominator

    if abs_d == 1:
        if abs_n == 1 and degree != 0:
            c_part = ""
        else:
            c_part = str(abs_n)
    else:
        c_part = f"{abs_n}/{abs_d}"

    if degree == 0:
        if c_part:
            return f"{sign}{c_part}"
        else:
            return f"{sign}1"
    elif degree == 1:
        v_part = var
    else:
        v_part = f"{var}^{degree}"

    return f"{sign}{c_part}{v_part}"


def _log_to_string(coef: Fraction, arg: str) -> str:
    """Форматирует логарифмический член K*ln|Arg|"""
    sign = "-" if coef.numerator < 0 else ""
    abs_n = abs(coef.numerator)
    abs_d = coef.denominator

    if abs_d == 1:
        if abs_n == 1:
            c_part = ""
        else:
            c_part = str(abs_n)
    else:
        c_part = f"{abs_n}/{abs_d}"

    if c_part == "" or c_part == "-" or c_part == 1:
        return f"{sign}ln|{arg}|"
    else:
        return f"{sign}{c_part}*ln|{arg}|"