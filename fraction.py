from math import gcd


class Fraction:
    """
    Класс для представления рациональных дробей
    поддерживает арифметические операции и автоматическое сокращение
    """

    def __init__(self, numerator, denominator=1):
        """
        Инициализирует дробь числителем и знаменателем

        numerator - числитель дроби
        denominator - знаменатель дроби (по умолчанию 1)
        """
        self.numerator = int(numerator)
        self.denominator = int(denominator)
        if self.denominator == 0:
            raise ValueError("Знаменатель не может быть нулём")
        self.simplify()

    def simplify(self):
        """
        Сокращает дробь до несократимого вида и нормализует знак (хранится в числителе)
        """
        g = gcd(abs(self.numerator), abs(self.denominator))
        self.numerator //= g
        self.denominator //= g
        if self.denominator < 0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator

    def __add__(self, other):
        """Сложение дробей"""
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(
            self.numerator * other.denominator + other.numerator * self.denominator,
            self.denominator * other.denominator
        )

    def __sub__(self, other):
        """Вычитание дробей"""
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(
            self.numerator * other.denominator - other.numerator * self.denominator,
            self.denominator * other.denominator
        )

    def __mul__(self, other):
        """Умножение дробей"""
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(
            self.numerator * other.numerator,
            self.denominator * other.denominator
        )

    def __truediv__(self, other):
        """Деление дробей"""
        if isinstance(other, int):
            other = Fraction(other, 1)
        return Fraction(
            self.numerator * other.denominator,
            self.denominator * other.numerator
        )

    def __eq__(self, other):
        """Проверка равенства двух дробей"""
        if isinstance(other, int):
            other = Fraction(other, 1)
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __repr__(self):
        """Строковое представление дроби"""
        if self.denominator == 1:
            return str(self.numerator)
        else:
            return f"{self.numerator}/{self.denominator}"