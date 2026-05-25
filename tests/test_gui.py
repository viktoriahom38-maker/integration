"""
Тестирование графического интерфейса
"""

import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk


class TestGuiReal(unittest.TestCase):
    """реальные тесты GUI (создает настоящее окно)"""

    @classmethod
    def setUpClass(cls):
        """создаем окно один раз"""
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.root.update()

        from gui import MathExpressionBuilder
        cls.app = MathExpressionBuilder()
        cls.app.root = cls.root
        cls.app.setup_ui()
        cls.root.update()

    @classmethod
    def tearDownClass(cls):
        """закрываем окно"""
        cls.root.destroy()

    def test_main_frame_created(self):
        """проверка создания главного фрейма"""
        found = False
        for child in self.root.winfo_children():
            if isinstance(child, tk.ttk.Frame):
                found = True
                break
        self.assertTrue(found)

    def test_apply_button_exists(self):
        """проверка кнопки Применить"""
        found = False

        def search(widget):
            nonlocal found
            if isinstance(widget, tk.ttk.Button) and widget.cget('text') == "Применить":
                found = True
            for child in widget.winfo_children():
                search(child)

        search(self.root)
        self.assertTrue(found)

    def test_expression_entry_exists(self):
        """проверка поля ввода выражения"""
        found = False

        def search(widget):
            nonlocal found
            if isinstance(widget, tk.ttk.Entry):
                found = True
            for child in widget.winfo_children():
                search(child)

        search(self.root)
        self.assertTrue(found)

    def test_result_text_exists(self):
        """проверка поля результата"""
        found = False

        def search(widget):
            nonlocal found
            if isinstance(widget, tk.Text):
                found = True
            for child in widget.winfo_children():
                search(child)

        search(self.root)
        self.assertTrue(found)

    def test_add_text_method(self):
        """проверка add_text"""
        self.app.expression_var = tk.StringVar()
        self.app.expression_var.set("")
        self.app.add_text("x")
        self.assertEqual(self.app.expression_var.get(), "x")

    def test_clear_method(self):
        """проверка clear"""
        self.app.expression_var = tk.StringVar()
        self.app.expression_var.set("x^2")
        self.app.clear()
        self.assertEqual(self.app.expression_var.get(), "")


class TestGuiMethodsMocked(unittest.TestCase):
    """тесты методов GUI с моками (без реального окна)"""

    def setUp(self):
        """создаем моки для tkinter"""
        with patch('tkinter.Tk') as mock_tk:
            with patch('tkinter.StringVar') as mock_stringvar:
                mock_tk.return_value = MagicMock()
                mock_stringvar.return_value = MagicMock()

                from gui import MathExpressionBuilder
                self.app = MathExpressionBuilder()
                self.app.expression_var = MagicMock()
                self.app.result_text = MagicMock()

    def test_add_text_appends(self):
        """add_text добавляет текст"""
        self.app.expression_var.get.return_value = "sin("
        self.app.add_text("x")
        self.app.expression_var.set.assert_called_with("sin(x")

    def test_clear_clears(self):
        """clear очищает всё"""
        self.app.clear()
        self.app.expression_var.set.assert_called_with("")
        self.app.result_text.delete.assert_called_with(1.0, tk.END)

    def test_backspace_removes_last(self):
        """backspace удаляет последний символ"""
        self.app.expression_var.get.return_value = "sin(x"
        self.app.backspace()
        self.app.expression_var.set.assert_called_with("sin(")

    def test_backspace_empty(self):
        """backspace на пустой строке"""
        self.app.expression_var.get.return_value = ""
        self.app.backspace()
        self.app.expression_var.set.assert_called_with("")

    def test_on_entry_change(self):
        """on_entry_change обновляет expression"""
        self.app.expression_var.get.return_value = "x^3"
        mock_event = MagicMock()
        self.app.on_entry_change(mock_event)
        self.assertEqual(self.app.expression, "x^3")

    def test_update_variable_valid(self):
        """update_variable с валидным значением"""
        with patch('gui.messagebox'):
            self.app.variable = MagicMock()
            self.app.variable.get.return_value = "t"
            self.app.update_variable_buttons = MagicMock()
            self.app.update_variable()
            self.app.update_variable_buttons.assert_called_once()

    def test_update_variable_invalid(self):
        """update_variable с невалидным значением"""
        with patch('gui.messagebox') as mock_msg:
            self.app.variable = MagicMock()
            self.app.variable.get.return_value = "xy"
            self.app.update_variable()
            mock_msg.showerror.assert_called_once()


if __name__ == "__main__":
    unittest.main()
