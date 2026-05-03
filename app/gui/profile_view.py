import customtkinter as ctk


class ProfileView(ctk.CTkFrame):
    """Вкладка профиля: просмотр и редактирование данных пользователя."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_widgets()
        self.load_profile()

    def create_widgets(self):
        # Заголовок
        self.title_label = ctk.CTkLabel(
            self, text="Профиль пользователя", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(10, 20))

        # Email (только для чтения)
        self.email_label = ctk.CTkLabel(self, text="Email:", font=ctk.CTkFont(size=14))
        self.email_label.pack(pady=(10, 0))
        self.email_value = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.email_value.pack()

        # Рост
        self.height_label = ctk.CTkLabel(self, text="Рост (см):", font=ctk.CTkFont(size=14))
        self.height_label.pack(pady=(10, 0))
        self.height_entry = ctk.CTkEntry(self, width=200)
        self.height_entry.pack()

        # Вес
        self.weight_label = ctk.CTkLabel(self, text="Вес (кг):", font=ctk.CTkFont(size=14))
        self.weight_label.pack(pady=(10, 0))
        self.weight_entry = ctk.CTkEntry(self, width=200)
        self.weight_entry.pack()

        # Возраст
        self.age_label = ctk.CTkLabel(self, text="Возраст:", font=ctk.CTkFont(size=14))
        self.age_label.pack(pady=(10, 0))
        self.age_entry = ctk.CTkEntry(self, width=200)
        self.age_entry.pack()

        # Пол
        self.gender_label = ctk.CTkLabel(self, text="Пол:", font=ctk.CTkFont(size=14))
        self.gender_label.pack(pady=(10, 0))
        self.gender_menu = ctk.CTkOptionMenu(self, values=["male", "female", "other"], width=200)
        self.gender_menu.pack()

        # Дневная цель калорий
        self.goal_label = ctk.CTkLabel(self, text="Дневная цель калорий:", font=ctk.CTkFont(size=14))
        self.goal_label.pack(pady=(10, 0))
        self.goal_entry = ctk.CTkEntry(self, width=200)
        self.goal_entry.pack()

        # Кнопка сохранения
        self.save_btn = ctk.CTkButton(self, text="Сохранить изменения", command=self.save_profile)
        self.save_btn.pack(pady=20)

        # Сообщение
        self.message_label = ctk.CTkLabel(self, text="", text_color="green")
        self.message_label.pack()

    def load_profile(self):
        """Загружает данные профиля из controller и заполняет поля."""
        profile = self.controller.get_profile()
        if profile:
            self.email_value.configure(text=profile.get("email", ""))
            self.height_entry.delete(0, 'end')
            self.height_entry.insert(0, str(profile.get("height_cm") or ""))
            self.weight_entry.delete(0, 'end')
            self.weight_entry.insert(0, str(profile.get("weight_kg") or ""))
            self.age_entry.delete(0, 'end')
            self.age_entry.insert(0, str(profile.get("age") or ""))
            self.gender_menu.set(profile.get("gender") or "male")
            self.goal_entry.delete(0, 'end')
            self.goal_entry.insert(0, str(profile.get("daily_calorie_goal", 2000)))

    def save_profile(self):
        updates = {}
        try:
            height = self.height_entry.get().strip()
            if height:
                updates["height_cm"] = float(height)

            weight = self.weight_entry.get().strip()
            if weight:
                updates["weight_kg"] = float(weight)

            age = self.age_entry.get().strip()
            if age:
                updates["age"] = int(age)

            gender = self.gender_menu.get()
            if gender:
                updates["gender"] = gender

            goal = self.goal_entry.get().strip()
            if goal:
                goal_int = int(goal)
                if goal_int <= 0:
                    raise ValueError("Цель должна быть > 0")
                updates["daily_calorie_goal"] = goal_int

            if not updates:
                self.show_message("Нет изменений для сохранения", "orange")
                return

            success = self.controller.update_profile(**updates)
            if success:
                self.show_message("Профиль обновлён", "green")
                # Если изменили цель, обновим dashboard? можно, но пусть пользователь переключит вкладку.
            else:
                self.show_message("Ошибка при обновлении профиля", "red")
        except ValueError as e:
            self.show_message(f"Ошибка ввода: {e}", "red")

    def show_message(self, text, color):
        self.message_label.configure(text=text, text_color=color)
        self.after(3000, lambda: self.message_label.configure(text=""))