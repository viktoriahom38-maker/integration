from polynomial import Polynomial
from fraction import Fraction
from formatter import format_linear_expression
from function_integrator import FunctionIntegrator
from function_parser import is_elementary_function
from parser import preprocess, parse_to_polynomials
from validator import validate
from typing import List, Tuple, Union


def integrate(expression: str, variable: str) -> Union[str, Tuple[List, List]]:
    """
    Главная функция интегрирования

    expression - строковое выражение
    variable - переменная

    возвращает результат интегрирования (строку или кортеж)
    """

    if is_elementary_function(expression, variable):
        integrator = FunctionIntegrator(expression, variable)
        result = integrator.integrate()
        if result is not None:
            return result

    processed = preprocess(expression, variable)
    validate(processed, variable)
    num, den = parse_to_polynomials(processed, variable)
    return integrate_rational(num, den, variable)


def integrate_rational(numerator: Polynomial, denominator: Polynomial,
                       variable: str) -> Union[str, Tuple[List, List]]:
    """
    Интегрирует рациональную функцию P(x)/Q(x)

    numerator - числитель
    denominator - знаменатель
    variable - переменная

    возвращает кортеж (poly_terms, log_terms) или строку с ошибкой
    """
    if denominator.is_zero():
        return "Ошибка: знаменатель не может быть равен нулю"

    denom_deg = denominator.degree()

    if denom_deg > 2:
        return "Эта функция не интегрируется в рамках задачи на данный момент"

    if denom_deg == 0:
        const = denominator.coefficient(0)
        if const.numerator == 0:
            return "Ошибка: знаменатель равен нулю"
        new_num = Polynomial()
        for deg, coef in numerator.terms.items():
            new_num.add_term(deg, coef / const)
        return integrate_polynomial(new_num, variable)

    if denom_deg == 1:
        return integrate_rational_fraction(numerator, denominator, variable)

    if denom_deg == 2:
        return integrate_quadratic_denominator(numerator,
                                               denominator, variable)

    return integrate_rational_fraction(numerator, denominator, variable)


def integrate_quadratic_denominator(
        numerator: Polynomial, denominator: Polynomial, variable: str) -> (
                Union)[str, Tuple[List, List]]:
    """
    Интегрирует дроби с квадратным знаменателем

    numerator - числитель
    denominator - знаменатель степени 2
    variable - переменная

    возвращает кортеж (poly_terms, log_terms)
    """
    if numerator.degree() > 0:
        return "Эта функция не интегрируется в рамках задачи на данный момент"

    const = numerator.coefficient(0)
    a = denominator.coefficient(2)
    b = denominator.coefficient(1)
    c = denominator.coefficient(0)

    if b.numerator != 0:
        return "Эта функция не интегрируется в рамках задачи на данный момент"

    a_val = a.numerator / a.denominator
    c_val = c.numerator / c.denominator

    if c_val > 0:
        a_sqrt = (c_val ** 0.5)
        if a_sqrt == 1:
            return ([], [(Fraction(1, 1), f"arctg({variable})")])
        else:
            coef = Fraction(1, int(a_sqrt * a_val))
            return ([], [(coef, f"arctg({variable}/{int(a_sqrt)})")])

    return "Эта функция не интегрируется в рамках задачи на данный момент"


def integrate_polynomial(poly: Polynomial, variable: str) -> Tuple[List, List]:
    """
    Интегрирует многочлен по степенному правилу

    poly - многочлен для интегрирования
    variable - переменная

    возвращает (list_poly_terms, empty_list)
    """
    if poly.is_zero():
        return [], []

    result_terms = []
    for degree, coef in poly.terms.items():
        new_coef = coef / (degree + 1)
        result_terms.append((new_coef, degree + 1))

    return result_terms, []


def integrate_rational_fraction(numerator: Polynomial,
                denominator: Polynomial, variable: str) -> Tuple[List, List]:
    """
    Интегрирует правильную рациональную дробь через деление многочленов

    numerator - числитель
    denominator - знаменатель
    variable - переменная

    возвращает (list_poly_terms, list_log_terms)
    """
    quotient, remainder = numerator.divide_with_remainder(denominator)

    poly_terms = []
    log_terms = []

    if not quotient.is_zero():
        q_terms, _ = integrate_polynomial(quotient, variable)
        poly_terms.extend(q_terms)

    if not remainder.is_zero() and denominator.degree() == 1:
        log_result = integrate_linear_denominator(remainder, denominator, variable)
        if log_result:
            log_terms.append(log_result)

    return poly_terms, log_terms


def integrate_linear_denominator(numerator: Polynomial,
        denominator: Polynomial, variable: str) -> (
            Union)[Tuple[Fraction, str], None]:
    """
    Интегрирует выражение вида Const / (ax + b)

    numerator - константный числитель
    denominator - линейный знаменатель
    variable - переменная

    возвращает (coef, arg) для логарифма или None
    """
    a = denominator.coefficient(1)
    b = denominator.coefficient(0)

    if numerator.degree() > 0:
        return None

    const = numerator.coefficient(0)
    coef = const / a

    arg = format_linear_expression(a, b, variable)

    return (coef, arg)
