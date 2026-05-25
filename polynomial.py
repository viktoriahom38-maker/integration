from typing import Dict
from fraction import Fraction


class Polynomial:
    """
    Класс для представления многочлена от одной переменной
    Многочлен хранится как словарь {степень: коэффициент}
    """

    def __init__(self, terms: Dict[int, int | Fraction] = None) -> None:
        """
        Инициализирует многочлен списком членов

        terms - словарь вида {степень: коэффициент}
        Коэффициенты могут быть int или Fraction
        """
        self.terms: Dict[int, Fraction] = {}
        if terms:
            for deg, coef in terms.items():
                if isinstance(coef, Fraction):
                    f = coef
                else:
                    f = Fraction(coef, 1)
                if f.numerator != 0:
                    self.terms[int(deg)] = f

    def add_term(self, degree: int, coefficient: int | Fraction) -> None:
        """
        Добавляет член к многочлену
        Если член с такой степенью уже есть, коэффициенты суммируются

        degree - степень переменной
        coefficient - коэффициент при переменной
        """
        if not isinstance(degree, int):
            raise TypeError(f"Степень должна быть int, получено {type(degree)}")

        if isinstance(coefficient, Fraction):
            f = coefficient
        else:
            f = Fraction(coefficient, 1)

        if f.numerator == 0:
            return

        if degree in self.terms:
            self.terms[degree] = self.terms[degree] + f
        else:
            self.terms[degree] = f

        if self.terms[degree].numerator == 0:
            del self.terms[degree]

    def degree(self) -> int:
        """
        Возвращает старшую степень многочлена

        (возвращает -1 для нулевого многочлена)
        """
        if self.terms:
            return max(self.terms.keys())
        else:
            return -1

    def coefficient(self, degree: int) -> Fraction:
        """
        Возвращает коэффициент при заданной степени

        degree - запрашиваемая степень

        Fraction - коэффициент (возвращает 0, если член отсутствует)
        """
        if int(degree) in self.terms:
            return self.terms[int(degree)]
        else:
            return Fraction(0, 1)

    def is_zero(self) -> bool:
        """
        Проверяет, является ли многочлен нулевым

        True, если многочлен равен 0
        """
        return len(self.terms) == 0

    def divide_with_remainder(self, divisor: 'Polynomial') -> tuple:
        """
        Выполняет деление многочлена с остатком

        divisor - делитель

        tuple - кортеж (частное, остаток), где оба элемента — объекты Polynomial
        """
        if divisor.is_zero():
            raise ValueError("Деление на нулевой многочлен")

        dividend = Polynomial(self.terms.copy())
        quotient = Polynomial()

        while dividend.degree() >= divisor.degree() and not dividend.is_zero():
            deg_diff = dividend.degree() - divisor.degree()
            ratio = dividend.coefficient(dividend.degree()) / divisor.coefficient(divisor.degree())
            quotient.add_term(deg_diff, ratio)
            temp = Polynomial({deg_diff: ratio})
            dividend = dividend - (divisor * temp)

        return quotient, dividend

    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        """Умножение двух многочленов"""
        result = Polynomial()
        for deg1, coef1 in self.terms.items():
            for deg2, coef2 in other.terms.items():
                result.add_term(deg1 + deg2, coef1 * coef2)
        return result

    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        """Сложение двух многочленов"""
        result = Polynomial(self.terms.copy())
        for deg, coef in other.terms.items():
            result.add_term(deg, coef)
        return result

    def __sub__(self, other: 'Polynomial') -> 'Polynomial':
        """Вычитание двух многочленов"""
        result = Polynomial(self.terms.copy())
        for deg, coef in other.terms.items():
            result.add_term(deg, Fraction(-coef.numerator, coef.denominator))
        return result