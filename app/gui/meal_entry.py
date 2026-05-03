import customtkinter as ctk
from tkcalendar import DateEntry


class MealEntryView(ctk.CTkFrame):
    """Вкладка для добавления нового приёма пищи."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self, text="Добавить приём пищи", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(10, 20))

        # Поле "Продукт"
        self.product_label = ctk.CTkLabel(self, text="Продукт:", font=ctk.CTkFont(size=14))
        self.product_label.pack(pady=(10, 0))
        self.product_entry = ctk.CTkEntry(self, width=300, placeholder_text="Например: Овсянка")
        self.product_entry.pack(pady=(0, 10))

        # Поле "Калории"
        self.calories_label = ctk.CTkLabel(self, text="Калории (ккал):", font=ctk.CTkFont(size=14))
        self.calories_label.pack(pady=(10, 0))
        self.calories_entry = ctk.CTkEntry(self, width=300, placeholder_text="300")
        self.calories_entry.pack(pady=(0, 10))

        # Выбор даты
        self.date_label = ctk.CTkLabel(self, text="Дата:", font=ctk.CTkFont(size=14))
        self.date_label.pack(pady=(10, 0))
        self.date_picker = DateEntry(self, width=18, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_picker.pack(pady=(0, 20))

        # Кнопка сохранения
        self.save_btn = ctk.CTkButton(self, text="Сохранить", command=self.save_meal, width=200)
        self.save_btn.pack(pady=10)

        # Метка для сообщений
        self.message_label = ctk.CTkLabel(self, text="", text_color="green")
        self.message_label.pack(pady=10)

    def save_meal(self):
        product = self.product_entry.get().strip()
        calories_str = self.calories_entry.get().strip()
        meal_date = self.date_picker.get_date()

        if not product:
            self.show_message("Введите название продукта", "red")
            return
        if not calories_str:
            self.show_message("Введите количество калорий", "red")
            return

        try:
            calories = int(calories_str)
            if calories <= 0:
                raise ValueError
        except ValueError:
            self.show_message("Калории должны быть положительным целым числом", "red")
            return

        success = self.controller.add_meal(product, calories, meal_date)
        if success:
            self.show_message(f"Запись '{product}' на {meal_date} добавлена!", "green")
            self.product_entry.delete(0, 'end')
            self.calories_entry.delete(0, 'end')
            # автоматически обновляем прогресс в dashboard? можно, но не обязательно.
        else:
            self.show_message("Ошибка при добавлении записи", "red")

    def show_message(self, text, color):
        self.message_label.configure(text=text, text_color=color)
        self.after(3000, lambda: self.message_label.configure(text=""))