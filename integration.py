from polynomial import Polynomial
from fraction import Fraction
from formatter import format_linear_expression


def integrate(numerator: Polynomial, denominator: Polynomial, variable: str):
    """
    Главная функция интегрирования рациональной функции P(x)/Q(x)

    numerator числитель
    denominator знаменатель
    variable переменная

    tuple кортеж (list_poly_terms, list_log_terms) для форматирования
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

    return integrate_rational(numerator, denominator, variable)


def integrate_polynomial(poly: Polynomial, variable: str):
    """
    Интегрирует многочлен по степенному правилу ∫ x^n dx = x^(n+1)/(n+1)

    poly - многочлен для интегрирования
    variable - переменная

    tuple: (list_of_tuples_coeffs_degs, empty_list_for_logs)
    """
    if poly.is_zero():
        return [], []

    result_terms = []
    for degree, coef in poly.terms.items():
        new_coef = coef / (degree + 1)
        result_terms.append((new_coef, degree + 1))

    return result_terms, []


def integrate_rational(numerator: Polynomial, denominator: Polynomial, variable: str):
    """
    Интегрирует правильную рациональную дробь через деление многочленов
    (x^2 + 1)/(x) -> x + 1/x -> 1/2x^2 + ln|x| + C

    numerator - числитель
    denominator - знаменатель
    variable - переменная

    tuple: (list_poly_terms, list_log_terms)
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


def integrate_linear_denominator(numerator: Polynomial, denominator: Polynomial, variable: str):
    """
    Интегрирует выражение вида Const / (ax + b)

    numerator - константный числитель
    denominator - линейный знаменатель
    variable - переменная

    tuple: (coefficient_fraction, argument_string) для логарифма, или None
    """
    a = denominator.coefficient(1)
    b = denominator.coefficient(0)

    if numerator.degree() > 0:
        return None

    const = numerator.coefficient(0)
    coef = const / a

    arg = format_linear_expression(a, b, variable)

    return (coef, arg)