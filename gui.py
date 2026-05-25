"""
Графический интерфейс для ввода математических выражений
Запуск: python gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from integration import integrate
from formatter import format_output


class MathExpressionBuilder:
    """
    Главный класс графического интерфейса

    root - главное окно tkinter
    variable - текущая переменная интегрирования
    expression - текущее выражение
    expression_var - строковая переменная tkinter для поля ввода
    """

    def __init__(self) -> None:
        """
        Инициализирует главное окно и все компоненты
        """
        self.root = tk.Tk()
        self.root.title("Интегратор функций")
        self.root.geometry("850x750")
        self.root.minsize(750, 650)

        self.variable = tk.StringVar(value="x")
        self.expression = ""
        self.expression_var = tk.StringVar()

        self.setup_ui()
        self.update_variable_buttons()

    def setup_ui(self) -> None:
        """
        Создаёт и размещает все элементы графического интерфейса
        """
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top_frame, text="Переменная:", font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 10))
        self.var_entry = ttk.Entry(top_frame, textvariable=self.variable, width=5, font=("Arial", 11))
        self.var_entry.pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Применить", command=self.update_variable, width=15).pack(side=tk.LEFT, padx=(10, 0))

        display_frame = ttk.LabelFrame(main_frame, text="Введите выражение", padding="10")
        display_frame.pack(fill=tk.X, pady=(0, 10))

        self.entry = ttk.Entry(display_frame, textvariable=self.expression_var, font=("Courier", 14))
        self.entry.pack(fill=tk.X, ipady=8)
        self.entry.bind('<KeyRelease>', self.on_entry_change)

        result_frame = ttk.LabelFrame(main_frame, text="Результат интегрирования", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.result_text = tk.Text(result_frame, height=4, font=("Courier", 12), wrap=tk.WORD, relief=tk.SUNKEN, borderwidth=1)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        keyboard_frame = ttk.LabelFrame(main_frame, text="Клавиатура", padding="10")
        keyboard_frame.pack(fill=tk.X)

        numbers_frame = ttk.LabelFrame(keyboard_frame, text="Цифры", padding="5")
        numbers_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        for i, num in enumerate(['7', '8', '9', '4', '5', '6', '1', '2', '3', '0']):
            btn = ttk.Button(numbers_frame, text=num, width=5, command=lambda n=num: self.add_text(n))
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)

        operators_frame = ttk.LabelFrame(keyboard_frame, text="Операторы", padding="5")
        operators_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        operators = [('+', '+'), ('-', '-'), ('*', '*'), ('/', '/'), ('^', '^'), ('(', '('), (')', ')')]
        for i, (text, cmd) in enumerate(operators):
            btn = ttk.Button(operators_frame, text=text, width=5, command=lambda c=cmd: self.add_text(c))
            btn.grid(row=i // 2, column=i % 2, padx=2, pady=2)

        functions_frame = ttk.LabelFrame(keyboard_frame, text="Функции", padding="5")
        functions_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        functions = [
            ('sin', 'sin('), ('cos', 'cos('), ('tg', 'tg('), ('ctg', 'ctg('),
            ('arcsin', 'arcsin('), ('arctg', 'arctg('), ('ln', 'ln('), ('sqrt', 'sqrt(')
        ]
        row = 0
        col = 0
        for text, cmd in functions:
            btn = ttk.Button(functions_frame, text=text, width=8, command=lambda c=cmd: self.add_text(c))
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 1:
                col = 0
                row += 1

        variables_frame = ttk.LabelFrame(keyboard_frame, text="Переменные и константы", padding="5")
        variables_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        self.var_btn = ttk.Button(variables_frame, text=self.variable.get(), width=8, command=lambda: self.add_text(self.variable.get()))
        self.var_btn.pack(pady=2)
        self.var_buttons = [self.var_btn]

        power_btn = ttk.Button(variables_frame, text="^2", width=8, command=lambda: self.add_text('^2'))
        power_btn.pack(pady=2)
        power3_btn = ttk.Button(variables_frame, text="^3", width=8, command=lambda: self.add_text('^3'))
        power3_btn.pack(pady=2)
        e_btn = ttk.Button(variables_frame, text="e", width=8, command=lambda: self.add_text('e^('))
        e_btn.pack(pady=2)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(control_frame, text="Вычислить интеграл", command=self.calculate_integral, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Очистить все", command=self.clear, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Удалить один", command=self.backspace, width=15).pack(side=tk.LEFT, padx=5)

    def on_entry_change(self, event) -> None:
        """
        Обрабатывает изменение текста в поле ввода

        event - событие изменения
        """
        self.expression = self.expression_var.get()

    def add_text(self, text: str) -> None:
        """
        Добавляет текст в поле ввода

        text - добавляемый текст
        """
        current = self.expression_var.get()
        self.expression_var.set(current + text)
        self.expression = current + text

    def clear(self) -> None:
        """
        Очищает поле ввода и результат
        """
        self.expression_var.set("")
        self.expression = ""
        self.result_text.delete(1.0, tk.END)

    def backspace(self) -> None:
        """
        Удаляет последний символ из поля ввода
        """
        current = self.expression_var.get()
        self.expression_var.set(current[:-1])
        self.expression = current[:-1]

    def update_variable(self) -> None:
        """
        Обновляет переменную интегрирования
        """
        new_var = self.variable.get()
        if not new_var or len(new_var) != 1 or not new_var.isalpha():
            messagebox.showerror("Ошибка", "Переменная должна быть одной буквой")
            self.variable.set("x")
            return
        self.update_variable_buttons()

    def update_variable_buttons(self) -> None:
        """
        Обновляет кнопки с переменной
        """
        var = self.variable.get()
        self.var_btn.config(text=var, command=lambda: self.add_text(var))

    def calculate_integral(self) -> None:
        """
        Вычисляет интеграл и выводит результат
        """
        expression = self.expression_var.get()
        if not expression:
            messagebox.showwarning("Предупреждение", "Введите выражение")
            return

        var = self.variable.get()
        try:
            result = integrate(expression, var)
            output = format_output(expression, result, var)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, output)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def run(self) -> None:
        """
        Запускает главный цикл приложения
        """
        self.root.mainloop()


if __name__ == "__main__":
    app = MathExpressionBuilder()
    app.run()
