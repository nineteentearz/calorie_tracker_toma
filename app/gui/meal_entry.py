import customtkinter as ctk
from datetime import date
from tkinter import messagebox


class MealEntryView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self, text="Добавить приём пищи", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_title.pack(pady=20)

        # Форма
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)

        # Продукт
        ctk.CTkLabel(form_frame, text="Продукт:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.product_entry = ctk.CTkEntry(form_frame, width=250)
        self.product_entry.grid(row=0, column=1, padx=10, pady=10)

        # Калории
        ctk.CTkLabel(form_frame, text="Калории (ккал):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.calories_entry = ctk.CTkEntry(form_frame, width=150)
        self.calories_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Дата
        ctk.CTkLabel(form_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.date_var = ctk.StringVar(value=date.today().isoformat())
        self.date_entry = ctk.CTkEntry(form_frame, textvariable=self.date_var, width=120)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Кнопка
        self.add_btn = ctk.CTkButton(form_frame, text="Добавить", command=self.add_meal)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Статус
        self.status_label = ctk.CTkLabel(form_frame, text="", text_color="green")
        self.status_label.grid(row=4, column=0, columnspan=2)

    def add_meal(self):
        product = self.product_entry.get().strip()
        calories_str = self.calories_entry.get().strip()
        date_str = self.date_var.get().strip()

        if not product:
            messagebox.showwarning("Ошибка", "Введите название продукта")
            return
        try:
            calories = int(calories_str)
            if calories <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка", "Калории должны быть положительным целым числом")
            return
        try:
            meal_date = date.fromisoformat(date_str)
        except ValueError:
            messagebox.showwarning("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        success = self.controller.add_meal(product, calories, meal_date)
        if success:
            self.status_label.configure(text="✓ Запись добавлена!", text_color="green")
            self.product_entry.delete(0, "end")
            self.calories_entry.delete(0, "end")
            # Дату оставляем текущую или как было
            self.product_entry.focus()
        else:
            self.status_label.configure(text="Ошибка при добавлении. Проверьте соединение с БД.", text_color="red")