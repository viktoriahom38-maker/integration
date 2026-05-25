import re


def validate(expression: str, variable: str) -> None:
    """
    Выполняет комплексную проверку корректности входного выражения

    expression - предобработанное выражение
    variable - переменная интегрирования
    """
    check_symbols(expression, variable)
    check_brackets(expression)
    check_division_sign(expression)
    check_operators(expression)
    check_no_decimals(expression)
    check_no_negative_powers(expression, variable)


def check_symbols(text: str, variable: str) -> None:
    """Проверяет наличие только разрешенных символов"""
    func_names = ['sin', 'cos', 'tg', 'ctg', 'arcsin', 'arctg', 'ln', 'sqrt']
    allowed_chars = set('0123456789+-*/^()' + variable)
    for ch in text:
        if not ch.isalpha():
            if ch not in allowed_chars:
                raise ValueError(f"Недопустимый символ: '{ch}'")
    words = re.findall(r'[a-zA-Z]+', text)
    for word in words:
        if word == variable:
            continue
        if word == 'e':
            continue
        if word not in func_names:
            raise ValueError(f"Недопустимое имя функции: '{word}'")


def check_brackets(text: str) -> None:
    """Проверяет баланс открывающих и закрывающих скобок"""
    balance = 0
    for ch in text:
        if ch == '(':
            balance += 1
        elif ch == ')':
            balance -= 1
    if balance != 0:
        raise ValueError("Проверьте баланс открывающих и закрывающих скобок")


def check_division_sign(text: str) -> None:
    """Запрещает более одного знака деления"""
    if text.count('/') > 1:
        raise ValueError("Более одного знака деления")


def check_operators(text: str) -> None:
    """Проверяет корректность расположения арифметических операторов"""
    if text and text[0] in '/^*':
        raise ValueError("Выражение не может начинаться с / или ^")
    if text and text[-1] in '+-/^*':
        raise ValueError("Выражение не может заканчиваться оператором")
    for i in range(len(text) - 1):
        if text[i] in '+-/^*' and text[i + 1] in '+-/^*':
            raise ValueError(f"Два оператора подряд: '{text[i]}{text[i + 1]}'")


def check_no_decimals(text: str) -> None:
    """Запрещает использование десятичных дробей"""
    if re.search(r'\d+[.,]\d+', text):
        raise ValueError("Десятичные дроби не поддерживаются")


def check_no_negative_powers(text: str, variable: str) -> None:
    """Запрещает отрицательные степени, но пропускает e^(2x)"""
    if re.search(r'e\^\(', text):
        return

    pattern = r'[a-zA-Z0-9]\^\(([^)]+)\)'
    match = re.search(pattern, text)
    if match:
        inside = match.group(1)
        if not inside.isdigit():
            raise ValueError(f"Степень должна быть положительным целым числом, получено: '{inside}'")
    if re.search(r'[a-zA-Z0-9]\^-\d+', text):
        raise ValueError("Отрицательные степени не поддерживаются")