"""
Модуль для определения элементарных функций
"""

import re


def is_elementary_function(expression: str, variable: str) -> bool:
    """
    Проверяет, можно ли интегрировать выражение как элементарную функцию

    expression - строковое выражение для проверки
    variable - переменная интегрирования

    True если выражение распознаётся, False в противном случае
    """
    if re.search(r'e\^\(', expression):
        return True

    if re.search(rf'e\^{re.escape(variable)}', expression):
        return True

    func_names = ['sin', 'cos', 'tg', 'ctg', 'arcsin', 'arctg', 'ln', 'sqrt']

    for func in func_names:
        if re.search(rf'{func}\s*\(', expression):
            return True

    if re.search(r'\d+\^x', expression):
        return True

    if re.search(rf'1/{re.escape(variable)}(\^\d+)?', expression):
        return True

    if re.search(rf'{re.escape(variable)}\^-?\d+', expression):
        return True

    return False