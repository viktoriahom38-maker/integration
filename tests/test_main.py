"""
Тестирование консольного интерфейса
Запуск: python -m unittest tests.test_main_console
"""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO


class TestMainConsole(unittest.TestCase):
    """тестирование консольного интерфейса"""

    def test_start_valid_variable_then_keyboard_interrupt(self):
        """запуск с валидной переменной и прерывание"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", KeyboardInterrupt()]
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                from main import start
                try:
                    start()
                except KeyboardInterrupt:
                    pass
                output = mock_stdout.getvalue()
                self.assertIn("Переменная: 'x'", output)

    def test_start_empty_variable(self):
        """пустая переменная"""
        with patch('builtins.input') as mock_input:
            mock_input.return_value = ""
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                from main import start
                start()
                output = mock_stdout.getvalue()
                self.assertIn("Ошибка: Переменная должна быть одной буквой", output)

    def test_start_too_long_variable(self):
        """слишком длинная переменная (2 буквы)"""
        with patch('builtins.input') as mock_input:
            mock_input.return_value = "xy"
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                from main import start
                start()
                output = mock_stdout.getvalue()
                self.assertIn("Ошибка: Переменная должна быть одной буквой", output)

    def test_start_three_letter_variable(self):
        """переменная из трех букв"""
        with patch('builtins.input') as mock_input:
            mock_input.return_value = "xyz"
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                from main import start
                start()
                output = mock_stdout.getvalue()
                self.assertIn("Ошибка: Переменная должна быть одной буквой", output)

    def test_start_numeric_variable(self):
        """числовая переменная"""
        with patch('builtins.input') as mock_input:
            mock_input.return_value = "123"
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                from main import start
                start()
                output = mock_stdout.getvalue()
                self.assertIn("Ошибка: Переменная должна быть одной буквой", output)

    def test_start_digit_letter_variable(self):
        """смешанная переменная (цифра и буква)"""
        with patch('builtins.input') as mock_input:
            mock_input.return_value = "x1"
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                from main import start
                start()
                output = mock_stdout.getvalue()
                self.assertIn("Ошибка: Переменная должна быть одной буквой", output)

    def test_successful_integration_one_expression(self):
        """успешное интегрирование одного выражения"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", "x^2", KeyboardInterrupt()]
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('main.integrate') as mock_integrate:
                    with patch('main.format_output') as mock_format:
                        mock_integrate.return_value = "x^3/3"
                        mock_format.return_value = "∫ (x^2) dx = x^3/3 + C"

                        from main import start
                        try:
                            start()
                        except KeyboardInterrupt:
                            pass

                        mock_integrate.assert_called_with("x^2", "x")
                        mock_format.assert_called_once()

    def test_multiple_integrations(self):
        """несколько выражений подряд"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", "x^2", "sin(x)", KeyboardInterrupt()]
            with patch('main.integrate') as mock_integrate:
                with patch('main.format_output') as mock_format:
                    mock_integrate.side_effect = ["x^3/3", "-cos(x)"]
                    mock_format.side_effect = [
                        "∫ (x^2) dx = x^3/3 + C",
                        "∫ (sin(x)) dx = -cos(x) + C"
                    ]

                    from main import start
                    try:
                        start()
                    except KeyboardInterrupt:
                        pass

                    self.assertEqual(mock_integrate.call_count, 2)
                    self.assertEqual(mock_format.call_count, 2)

    def test_integration_with_polynomial(self):
        """интегрирование многочлена"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", "x^3+2*x", KeyboardInterrupt()]
            with patch('main.integrate') as mock_integrate:
                with patch('main.format_output') as mock_format:
                    mock_integrate.return_value = "x^4/4+x^2"
                    mock_format.return_value = "∫ (x^3+2x) dx = x^4/4+x^2 + C"

                    from main import start
                    try:
                        start()
                    except KeyboardInterrupt:
                        pass

                    mock_integrate.assert_called_with("x^3+2*x", "x")

    def test_integration_with_fraction(self):
        """интегрирование дроби"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", "1/x", KeyboardInterrupt()]
            with patch('main.integrate') as mock_integrate:
                with patch('main.format_output') as mock_format:
                    mock_integrate.return_value = "ln|x|"
                    mock_format.return_value = "∫ (1/x) dx = ln|x| + C"

                    from main import start
                    try:
                        start()
                    except KeyboardInterrupt:
                        pass

                    mock_integrate.assert_called_with("1/x", "x")

    def test_integration_with_trigonometric(self):
        """интегрирование тригонометрической функции"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", "cos(x)", KeyboardInterrupt()]
            with patch('main.integrate') as mock_integrate:
                with patch('main.format_output') as mock_format:
                    mock_integrate.return_value = "sin(x)"
                    mock_format.return_value = "∫ (cos(x)) dx = sin(x) + C"

                    from main import start
                    try:
                        start()
                    except KeyboardInterrupt:
                        pass

                    mock_integrate.assert_called_with("cos(x)", "x")

    def test_integration_with_exponential(self):
        """интегрирование экспоненты"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", "e^x", KeyboardInterrupt()]
            with patch('main.integrate') as mock_integrate:
                with patch('main.format_output') as mock_format:
                    mock_integrate.return_value = "e^x"
                    mock_format.return_value = "∫ (e^x) dx = e^x + C"

                    from main import start
                    try:
                        start()
                    except KeyboardInterrupt:
                        pass

                    mock_integrate.assert_called_with("e^x", "x")

    def test_empty_expression_skip(self):
        """пустое выражение (должно пропускаться и запрашивать снова)"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", "", "x^2", KeyboardInterrupt()]
            with patch('main.integrate') as mock_integrate:
                with patch('main.format_output') as mock_format:
                    mock_integrate.return_value = "x^3/3"
                    mock_format.return_value = "∫ (x^2) dx = x^3/3 + C"

                    from main import start
                    try:
                        start()
                    except KeyboardInterrupt:
                        pass

                    mock_integrate.assert_called_once_with("x^2", "x")

    def test_error_handling_integration(self):
        """обработка ошибки при интегрировании"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["x", "invalid", KeyboardInterrupt()]
            with patch('main.integrate') as mock_integrate:
                with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                    mock_integrate.side_effect = Exception("Недопустимое выражение")

                    from main import start
                    try:
                        start()
                    except KeyboardInterrupt:
                        pass

                    output = mock_stdout.getvalue()
                    self.assertIn("Ошибка: Недопустимое выражение", output)

    def test_different_variable_name(self):
        """интегрирование с переменной 't'"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["t", "t^2", KeyboardInterrupt()]
            with patch('main.integrate') as mock_integrate:
                with patch('main.format_output') as mock_format:
                    mock_integrate.return_value = "t^3/3"
                    mock_format.return_value = "∫ (t^2) dt = t^3/3 + C"

                    from main import start
                    try:
                        start()
                    except KeyboardInterrupt:
                        pass

                    mock_integrate.assert_called_with("t^2", "t")


if __name__ == "__main__":
    unittest.main()
