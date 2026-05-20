"""
Тесты для проверки всех 25 базовых типов интегрирования
"""

from integration import integrate
from formatter import format_output


def run_test(expr, var, expected):
    try:
        result = integrate(expr, var)
        output = format_output(expr, result, var)
        if output == expected:
            print(f"✅ {expr} = {output}")
            return True
        else:
            print(f"❌ {expr}")
            print(f"   Ожидалось: {expected}")
            print(f"   Получено:  {output}")
            return False
    except Exception as e:
        print(f"❌ {expr}")
        print(f"   Ошибка: {e}")
        print(f"   Ожидалось: {expected}")
        return False


def main():
    print("ТЕСТИРОВАНИЕ")
    print()

    tests = [
        ("1", "x", "∫ (1) dx = x + C"),
        ("5", "x", "∫ (5) dx = 5x + C"),
        ("x", "x", "∫ (x) dx = 1/2x^2 + C"),
        ("x^3", "x", "∫ (x^3) dx = x^4/4 + C"),
        ("1/x^2", "x", "∫ (1/x^2) dx = -1/x + C"),
        ("1/sqrt(x)", "x", "∫ (1/sqrt(x)) dx = 2*sqrt(x) + C"),
        ("sqrt(x)", "x", "∫ (sqrt(x)) dx = 2/3x^(3/2) + C"),
        ("1/x", "x", "∫ (1/x) dx = ln|x| + C"),
        ("1/(x+3)", "x", "∫ (1/(x+3)) dx = ln|x+3| + C"),
        ("1/(x-2)", "x", "∫ (1/(x-2)) dx = ln|x-2| + C"),
        ("e^x", "x", "∫ (e^x) dx = e^x + C"),
        ("2^x", "x", "∫ (2^x) dx = 2^x/ln(2) + C"),
        ("cos(x)", "x", "∫ (cos(x)) dx = sin(x) + C"),
        ("cos(2x)", "x", "∫ (cos(2x)) dx = 1/2sin(2x) + C"),
        ("sin(x)", "x", "∫ (sin(x)) dx = -cos(x) + C"),
        ("sin(2x)", "x", "∫ (sin(2x)) dx = -1/2cos(2x) + C"),
        ("1/cos(x)^2", "x", "∫ (1/cos(x)^2) dx = tg(x) + C"),
        ("1/sin(x)^2", "x", "∫ (1/sin(x)^2) dx = -ctg(x) + C"),
        ("1/sqrt(1-x^2)", "x", "∫ (1/sqrt(1-x^2)) dx = arcsin(x) + C"),
        ("1/(1+x^2)", "x", "∫ (1/(1+x^2)) dx = arctg(x) + C"),
        ("tg(x)", "x", "∫ (tg(x)) dx = -ln|cos(x)| + C"),
        ("ctg(x)", "x", "∫ (ctg(x)) dx = ln|sin(x)| + C"),
        ("e^(2x)", "x", "∫ (e^(2x)) dx = 1/2e^(2x) + C"),
        ("1/sqrt(9-x^2)", "x", "∫ (1/sqrt(9-x^2)) dx = arcsin(x/3) + C"),
        ("1/(4+x^2)", "x", "∫ (1/(4+x^2)) dx = 1/2arctg(x/2) + C"),
        ("1/(x^2-4)", "x", "∫ (1/(x^2-4)) dx = 1/4ln|(x-2)/(x+2)| + C"),
        ("1/sqrt(x^2+4)", "x", "∫ (1/sqrt(x^2+4)) dx = ln|x + sqrt(x^2+4)| + C"),
        ("1/sqrt(x^2-4)", "x", "∫ (1/sqrt(x^2-4)) dx = ln|x + sqrt(x^2-4)| + C"),
    ]

    passed = 0
    failed = 0

    for expr, var, expected in tests:
        if run_test(expr, var, expected):
            passed += 1
        else:
            failed += 1
        print()

    print(f"ИТОГО: {passed} пройдено, {failed} не пройдено")


if __name__ == "__main__":
    main()