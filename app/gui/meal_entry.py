import customtkinter as ctk
from tkcalendar import DateEntry
from uuid import UUID

class MealEntryView(ctk.CTkFrame):
    """Вкладка для добавления нового приёма пищи с выбором из базы продуктов."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self, text="Добавить приём пищи", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(10, 20))

        # Выбор продукта из списка
        self.product_label = ctk.CTkLabel(self, text="Выберите продукт (или введите новый):", font=ctk.CTkFont(size=14))
        self.product_label.pack(pady=(10, 0))

        self.product_var = ctk.StringVar()
        self.product_menu = ctk.CTkOptionMenu(self, variable=self.product_var, values=[], command=self.on_product_select)
        self.product_menu.pack(pady=(5, 10))

        # Кнопка "Новый продукт"
        self.new_product_btn = ctk.CTkButton(self, text="+ Новый продукт", command=self.new_product_dialog, fg_color="#2ecc71")
        self.new_product_btn.pack(pady=5)

        # Название продукта (если вручную)
        self.custom_name_label = ctk.CTkLabel(self, text="Или введите название вручную:")
        self.custom_name_label.pack(pady=(10, 0))
        self.product_entry = ctk.CTkEntry(self, width=300, placeholder_text="Например: Овсянка")
        self.product_entry.pack(pady=(0, 10))

        # Калории
        self.calories_label = ctk.CTkLabel(self, text="Калории (ккал):", font=ctk.CTkFont(size=14))
        self.calories_label.pack(pady=(10, 0))
        self.calories_entry = ctk.CTkEntry(self, width=300, placeholder_text="300")
        self.calories_entry.pack(pady=(0, 10))

        # Дата
        self.date_label = ctk.CTkLabel(self, text="Дата:", font=ctk.CTkFont(size=14))
        self.date_label.pack(pady=(10, 0))
        self.date_picker = DateEntry(self, width=18, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_picker.pack(pady=(0, 20))

        # Кнопка сохранения
        self.save_btn = ctk.CTkButton(self, text="Сохранить", command=self.save_meal, width=200, fg_color="#2ecc71")
        self.save_btn.pack(pady=10)

        # Метка для сообщений
        self.message_label = ctk.CTkLabel(self, text="", text_color="green")
        self.message_label.pack(pady=10)

        # Загружаем список продуктов
        self.refresh_product_list()

    def refresh_product_list(self):
        """Обновляет выпадающий список продуктов из базы данных."""
        products = self.controller.get_all_products()
        product_names = [p.name for p in products]
        self.product_menu.configure(values=product_names)
        if product_names:
            self.product_var.set(product_names[0])
            self.on_product_select(product_names[0])
        else:
            self.product_var.set("")
            self.product_entry.delete(0, 'end')
            self.calories_entry.delete(0, 'end')

    def on_product_select(self, selected_name):
        """При выборе продукта подставляет его название и калории."""
        products = self.controller.get_all_products()
        for p in products:
            if p.name == selected_name:
                self.product_entry.delete(0, 'end')
                self.product_entry.insert(0, p.name)
                self.calories_entry.delete(0, 'end')
                self.calories_entry.insert(0, str(p.calories_per_unit))
                break

    def new_product_dialog(self):
        """Диалог для быстрого добавления нового продукта."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Новый продукт")
        dialog.geometry("300x200")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Название:").pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Калорий (на порцию/100г):").pack(pady=5)
        cal_entry = ctk.CTkEntry(dialog, width=250)
        cal_entry.pack(pady=5)

        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=5)

        def save():
            name = name_entry.get().strip()
            try:
                cal = int(cal_entry.get().strip())
            except:
                cal = 0
            if name and cal > 0:
                try:
                    self.controller.create_product(name, cal)
                    dialog.destroy()
                    self.refresh_product_list()
                    self.show_message(f"Продукт '{name}' добавлен!", "green")
                except Exception as e:
                    error_label.configure(text=str(e))
            else:
                error_label.configure(text="Заполните корректно поля")

        ctk.CTkButton(dialog, text="Сохранить", command=save).pack(pady=10)

    def save_meal(self):
        product_name = self.product_entry.get().strip()
        calories_str = self.calories_entry.get().strip()
        meal_date = self.date_picker.get_date()

        if not product_name:
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

        success = self.controller.add_meal(product_name, calories, meal_date)
        if success:
            self.show_message(f"Запись '{product_name}' на {meal_date} добавлена!", "green")
            # Не очищаем поля, чтобы можно было добавить ещё одно блюдо подряд
        else:
            self.show_message("Ошибка при добавлении записи", "red")

    def show_message(self, text, color):
        self.message_label.configure(text=text, text_color=color)
        self.after(3000, lambda: self.message_label.configure(text=""))