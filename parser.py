import re
from polynomial import Polynomial
from fraction import Fraction


def preprocess(expression: str, variable: str):
    """
    Удаляет пробелы и расставляет явные знаки умножения

    expression - исходное выражение
    variable - переменная интегрирования

    возвращает обработанное выражение с явными операторами '*'
    """
    expr = re.sub(r'\s+', '', expression)
    var = re.escape(variable)
    expr = re.sub(r'(\d)(' + var + r')', r'\1*\2', expr)
    expr = re.sub(r'(' + var + r')(\d)', r'\1*\2', expr)
    expr = re.sub(r'(' + var + r')(' + var + r')', r'\1*\2', expr)
    expr = re.sub(r'(' + var + r')\(', r'\1*(', expr)
    expr = re.sub(r'\)(' + var + r')', r')*\1', expr)
    expr = re.sub(r'\)\(', r')*(', expr)
    expr = re.sub(r'\)(\d)', r')*\1', expr)
    return expr


def parse_to_polynomials(expression: str, variable: str):
    """
    Парсит строку в объекты Polynomial для числителя и знаменателя

    expression - строка вида "числитель/знаменатель" или просто "числитель"
    variable - переменная интегрирования

    возвращает кортеж (числитель, знаменатель)
    """
    if '/' in expression:
        num_expr, den_expr = expression.split('/', 1)
    else:
        num_expr, den_expr = expression, "1"

    num_poly = build_polynomial_from_expr(num_expr, variable)
    den_poly = build_polynomial_from_expr(den_expr, variable)

    if den_poly.is_zero():
        raise ValueError("Знаменатель не может быть равен нулю")

    return num_poly, den_poly


def tokenize(expression: str, variable: str):
    """
    Разбивает строку выражения на токены

    expression - выражение после предобработки
    variable - переменная интегрирования

    возвращает список строк-токенов
    """
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        c = expression[i]
        if c in '*/^()+-':
            tokens.append(c)
            i += 1
        elif c == variable:
            tokens.append(c)
            i += 1
        elif c.isdigit():
            num = c
            i += 1
            while i < n and expression[i].isdigit():
                num += expression[i]
                i += 1
            if i < n and expression[i] == '/':
                i += 1
                den = ''
                while i < n and expression[i].isdigit():
                    den += expression[i]
                    i += 1
                tokens.append(f"{num}/{den}")
            else:
                tokens.append(num)
        else:
            i += 1

    return tokens


def build_polynomial_from_expr(expr: str, variable: str):
    """
    Рекурсивно парсит выражение в объект Polynomial

    expr - строка математического выражения
    variable - переменная интегрирования

    возвращает объект Polynomial
    """
    if not expr:
        return Polynomial({0: 0})

    tokens = tokenize(expr, variable)
    pos = 0

    def parse_expr():
        nonlocal pos
        left = parse_term()
        while pos < len(tokens) and tokens[pos] in '+-':
            op = tokens[pos]
            pos += 1
            right = parse_term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        return left

    def parse_term():
        nonlocal pos
        left = parse_factor()
        while pos < len(tokens) and tokens[pos] == '*':
            pos += 1
            right = parse_factor()
            left = left * right
        return left

    def parse_factor():
        nonlocal pos
        if pos >= len(tokens):
            return Polynomial({0: 0})

        if tokens[pos] == '+':
            pos += 1
            return parse_factor()

        if tokens[pos] == '-':
            pos += 1
            return Polynomial({0: -1}) * parse_factor()

        tok = tokens[pos]

        if tok == '(':
            pos += 1
            res = parse_expr()
            if pos < len(tokens) and tokens[pos] == ')':
                pos += 1
            return res

        if '/' in tok:
            parts = tok.split('/')
            val = Fraction(int(parts[0]), int(parts[1]))
            pos += 1

            if pos < len(tokens) and tokens[pos] == '*':
                pos += 1
                return parse_factor() * Polynomial({0: val})

            if pos < len(tokens) and tokens[pos] == variable:
                pos += 1
                deg = 1
                if pos < len(tokens) and tokens[pos] == '^':
                    pos += 1
                    if pos < len(tokens) and tokens[pos] == '(':
                        pos += 1
                    if pos < len(tokens) and tokens[pos].isdigit():
                        deg = int(tokens[pos])
                        pos += 1
                    if pos < len(tokens) and tokens[pos] == ')':
                        pos += 1
                return Polynomial({deg: val})

            if pos < len(tokens) and tokens[pos] == '^':
                pos += 1
                if pos < len(tokens) and tokens[pos] == '(':
                    pos += 1
                if pos < len(tokens) and tokens[pos].isdigit():
                    deg = int(tokens[pos])
                    pos += 1
                if pos < len(tokens) and tokens[pos] == ')':
                    pos += 1
                return Polynomial({deg: val})

            return Polynomial({0: val})

        if tok.isdigit():
            val = int(tok)
            pos += 1

            if pos < len(tokens) and tokens[pos] == '^':
                pos += 1
                if pos < len(tokens) and tokens[pos] == '(':
                    pos += 1
                if pos < len(tokens) and tokens[pos].isdigit():
                    deg = int(tokens[pos])
                    pos += 1
                if pos < len(tokens) and tokens[pos] == ')':
                    pos += 1
                return Polynomial({deg: val})

            if pos < len(tokens) and tokens[pos] == variable:
                pos += 1
                deg = 1
                if pos < len(tokens) and tokens[pos] == '^':
                    pos += 1
                    if pos < len(tokens) and tokens[pos] == '(':
                        pos += 1
                    if pos < len(tokens) and tokens[pos].isdigit():
                        deg = int(tokens[pos])
                        pos += 1
                    if pos < len(tokens) and tokens[pos] == ')':
                        pos += 1
                return Polynomial({deg: val})

            return Polynomial({0: val})

        if tok == variable:
            pos += 1
            deg = 1
            if pos < len(tokens) and tokens[pos] == '^':
                pos += 1
                if pos < len(tokens) and tokens[pos] == '(':
                    pos += 1
                if pos < len(tokens) and tokens[pos].isdigit():
                    deg = int(tokens[pos])
                    pos += 1
                if pos < len(tokens) and tokens[pos] == ')':
                    pos += 1
            return Polynomial({deg: 1})

        return Polynomial({0: 0})

    return parse_expr()