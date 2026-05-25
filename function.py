"""
Класс для представления элементарных функций
"""

from fraction import Fraction


class Function:
    """
    Представляет элементарную функцию: sin, cos, tg, ctg, arcsin, arctg, ln, exp, sqrt, степень
    """

    def __init__(self, name: str, argument, coefficient: Fraction = Fraction(1, 1)) -> None:
        """
        Создаёт функцию

        name - имя функции (sin, cos, tg, ctg, arcsin, arctg, ln, exp, sqrt, poly)
        argument - аргумент функции (может быть Function, Polynomial или строка)
        coefficient - коэффициент перед функцией
        """
        self.name = name
        self.argument = argument
        self.coefficient = coefficient

    def copy(self) -> 'Function':
        """Создаёт копию функции"""
        return Function(self.name, self.argument, self.coefficient)

    def __mul__(self, other: 'Function | int | Fraction') -> 'Function | ProductFunction':
        """Умножение функции на число или другую функцию"""
        if isinstance(other, (int, Fraction)):
            new_coef = self.coefficient * other
            return Function(self.name, self.argument, new_coef)
        if isinstance(other, Function):
            return ProductFunction(self, other)
        return ProductFunction(self, other)

    def __rmul__(self, other: 'Function | int | Fraction') -> 'Function | ProductFunction':
        """Умножение числа на функцию"""
        return self.__mul__(other)

    def __add__(self, other: 'Function | int | Fraction') -> 'Function | SumFunction':
        """Сложение функций"""
        if isinstance(other, (int, Fraction)) and other == 0:
            return self
        return SumFunction(self, other)

    def __sub__(self, other: 'Function | int | Fraction') -> 'SumFunction':
        """Вычитание функций"""
        return SumFunction(self, NegateFunction(other))

    def __neg__(self) -> 'Function':
        """Унарный минус"""
        return Function(self.name, self.argument, -self.coefficient)

    def __repr__(self) -> str:
        """Строковое представление"""
        if self.coefficient.numerator == 0:
            return "0"

        coef_str = ""
        if self.coefficient.numerator != 1 or self.coefficient.denominator != 1:
            if self.coefficient.numerator == -1 and self.coefficient.denominator == 1:
                coef_str = "-"
            else:
                coef_str = str(self.coefficient)

        if self.name == "poly":
            return f"{coef_str}{self.argument}"

        if self.name == "exp":
            if self.argument == "x":
                arg_str = "x"
            else:
                arg_str = f"({self.argument})"
            return f"{coef_str}e^{arg_str}"

        if self.name == "sqrt":
            return f"{coef_str}sqrt({self.argument})"

        if self.name == "ln":
            return f"{coef_str}ln|{self.argument}|"

        return f"{coef_str}{self.name}({self.argument})"


class SumFunction:
    """Сумма функций"""

    def __init__(self, left, right) -> None:
        """Создаёт объект суммы функций"""
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """Строковое представление суммы функций"""
        left_str = str(self.left)
        right_str = str(self.right)

        if right_str.startswith('-'):
            return f"{left_str} {right_str}"
        else:
            return f"{left_str} + {right_str}"


class ProductFunction:
    """Произведение функций"""

    def __init__(self, left, right) -> None:
        """Создаёт объект произведения функций"""
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """Строковое представление произведения функций"""
        left_str = str(self.left)
        right_str = str(self.right)

        if isinstance(self.left, Function) and self.left.name == "poly":
            if isinstance(self.right, Function):
                return f"{left_str}*{right_str}"
        if isinstance(self.right, Function) and self.right.name == "poly":
            if isinstance(self.left, Function):
                return f"{left_str}*{right_str}"
        return f"{left_str}{right_str}"


class NegateFunction:
    """Отрицательная функция"""

    def __init__(self, func) -> None:
        """Создаёт объект отрицательной функции"""
        self.func = func

    def __repr__(self) -> str:
        """Строковое представление отрицательной функции"""
        return f"-{self.func}"
