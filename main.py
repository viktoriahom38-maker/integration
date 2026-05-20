from integration import integrate
from formatter import format_output

def start():
    """Запускает интерактивный цикл программы интегрирования"""
    try:
        variable = input("Введите букву переменной (например, x): ").strip()
        if not variable or len(variable) != 1 or not variable.isalpha():
            print("Ошибка: Переменная должна быть одной буквой латинского алфавита.")
            return

        print(f"\nПеременная: '{variable}'. Вводите выражения для интегрирования.\n")

        while True:
            try:
                expression = input("Введите функцию: ").strip()
                if not expression:
                    continue

                result = integrate(expression, variable)
                print(format_output(expression, result, variable))

            except Exception as e:
                print(f"Ошибка: {e}")

    except KeyboardInterrupt:
        print("\nПрограмма завершена.")

if __name__ == "__main__":
    start()