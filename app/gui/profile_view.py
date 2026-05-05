import customtkinter as ctk

class ProfileView(ctk.CTkFrame):
    """Вкладка профиля: просмотр и редактирование с автоматическим расчётом дневной нормы калорий."""

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

        # --- Параметры для расчёта BMR/TDEE ---
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
        self.gender_menu = ctk.CTkOptionMenu(self, values=["male", "female"], width=200)
        self.gender_menu.pack()

        # Уровень активности
        self.activity_label = ctk.CTkLabel(self, text="Уровень активности:", font=ctk.CTkFont(size=14))
        self.activity_label.pack(pady=(10, 0))
        self.activity_menu = ctk.CTkOptionMenu(
            self,
            values=[
                "Сидячий (1.2)",
                "Лёгкий (1.375)",
                "Средний (1.55)",
                "Высокий (1.725)"
            ],
            width=200
        )
        self.activity_menu.pack()

        # Цель
        self.goal_type_label = ctk.CTkLabel(self, text="Цель:", font=ctk.CTkFont(size=14))
        self.goal_type_label.pack(pady=(10, 0))
        self.goal_menu = ctk.CTkOptionMenu(
            self,
            values=["Похудение", "Поддержание", "Набор массы"],
            width=200
        )
        self.goal_menu.pack()

        # Кнопка "Рассчитать и установить цель"
        self.calc_btn = ctk.CTkButton(self, text="Рассчитать дневную норму", command=self.calculate_goal, fg_color="#2ecc71")
        self.calc_btn.pack(pady=15)

        # Дневная цель калорий (можно и вручную)
        self.goal_label = ctk.CTkLabel(self, text="Дневная цель калорий (ккал):", font=ctk.CTkFont(size=14))
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
            # Загружаем активность и цель из сохранённых? Пока не сохраняем, оставим по умолчанию.

    def calculate_goal(self):
        """Рассчитывает дневную норму калорий на основе введённых параметров и цели."""
        try:
            height = float(self.height_entry.get())
            weight = float(self.weight_entry.get())
            age = int(self.age_entry.get())
        except ValueError:
            self.show_message("Заполните рост, вес и возраст корректными числами", "red")
            return

        gender = self.gender_menu.get()
        # BMR по формуле Миффлина-Сан-Жеора
        if gender == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Коэффициент активности
        activity_map = {
            "Сидячий (1.2)": 1.2,
            "Лёгкий (1.375)": 1.375,
            "Средний (1.55)": 1.55,
            "Высокий (1.725)": 1.725
        }
        activity = activity_map.get(self.activity_menu.get(), 1.2)
        tdee = bmr * activity

        # Корректировка по цели
        goal = self.goal_menu.get()
        if goal == "Похудение":
            suggested = tdee * 0.85  # дефицит 15%
        elif goal == "Набор массы":
            suggested = tdee * 1.10  # профицит 10%
        else:
            suggested = tdee

        suggested = round(suggested, 0)
        self.goal_entry.delete(0, 'end')
        self.goal_entry.insert(0, str(int(suggested)))
        self.show_message(f"Рекомендуемая дневная норма: {int(suggested)} ккал", "green")

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
                # Обновляем dashboard, если нужно, можно вызвать метод обновления прогресса
            else:
                self.show_message("Ошибка при обновлении профиля", "red")
        except ValueError as e:
            self.show_message(f"Ошибка ввода: {e}", "red")

    def show_message(self, text, color):
        self.message_label.configure(text=text, text_color=color)
        self.after(3000, lambda: self.message_label.configure(text=""))