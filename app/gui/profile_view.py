import customtkinter as ctk
from tkinter import messagebox


class ProfileView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self, text="Профиль пользователя", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_title.pack(pady=20)

        # Форма
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=40, fill="both", expand=True)

        # Email (только для чтения)
        ctk.CTkLabel(form_frame, text="Email:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.email_label = ctk.CTkLabel(form_frame, text="", font=ctk.CTkFont(weight="bold"))
        self.email_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Рост
        ctk.CTkLabel(form_frame, text="Рост (см):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.height_entry = ctk.CTkEntry(form_frame, width=150)
        self.height_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Вес
        ctk.CTkLabel(form_frame, text="Вес (кг):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.weight_entry = ctk.CTkEntry(form_frame, width=150)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Возраст
        ctk.CTkLabel(form_frame, text="Возраст:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.age_entry = ctk.CTkEntry(form_frame, width=150)
        self.age_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Пол
        ctk.CTkLabel(form_frame, text="Пол:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.gender_combobox = ctk.CTkComboBox(form_frame, values=["male", "female", ""], width=150)
        self.gender_combobox.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.gender_combobox.set("")

        # Дневная цель калорий
        ctk.CTkLabel(form_frame, text="Дневная цель (ккал):").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.goal_entry = ctk.CTkEntry(form_frame, width=150)
        self.goal_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Кнопки
        btn_frame = ctk.CTkFrame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        self.save_btn = ctk.CTkButton(btn_frame, text="Сохранить изменения", command=self.save_profile)
        self.save_btn.pack(side="left", padx=10)

        self.refresh_btn = ctk.CTkButton(btn_frame, text="Обновить", command=self.load_profile, fg_color="gray")
        self.refresh_btn.pack(side="left", padx=10)

        self.logout_btn = ctk.CTkButton(btn_frame, text="Выйти", command=self.logout, fg_color="red")
        self.logout_btn.pack(side="left", padx=10)

        # Статус
        self.status_label = ctk.CTkLabel(form_frame, text="", text_color="green")
        self.status_label.grid(row=7, column=0, columnspan=2)

        # Загружаем профиль при старте
        self.load_profile()

    def load_profile(self):
        profile = self.controller.get_profile()
        if not profile:
            self.email_label.configure(text="Не авторизован")
            return
        self.email_label.configure(text=profile.get("email", ""))
        self.height_entry.delete(0, "end")
        self.height_entry.insert(0, str(profile.get("height_cm", "")))
        self.weight_entry.delete(0, "end")
        self.weight_entry.insert(0, str(profile.get("weight_kg", "")))
        self.age_entry.delete(0, "end")
        self.age_entry.insert(0, str(profile.get("age", "")))
        self.gender_combobox.set(profile.get("gender", "") or "")
        self.goal_entry.delete(0, "end")
        self.goal_entry.insert(0, str(profile.get("daily_calorie_goal", 2000)))

    def save_profile(self):
        data = {}
        # Рост
        height_str = self.height_entry.get().strip()
        if height_str:
            try:
                data["height_cm"] = float(height_str)
            except ValueError:
                messagebox.showwarning("Ошибка", "Рост должен быть числом")
                return
        # Вес
        weight_str = self.weight_entry.get().strip()
        if weight_str:
            try:
                data["weight_kg"] = float(weight_str)
            except ValueError:
                messagebox.showwarning("Ошибка", "Вес должен быть числом")
                return
        # Возраст
        age_str = self.age_entry.get().strip()
        if age_str:
            try:
                data["age"] = int(age_str)
            except ValueError:
                messagebox.showwarning("Ошибка", "Возраст должен быть целым числом")
                return
        # Пол
        gender = self.gender_combobox.get().strip()
        if gender in ("male", "female"):
            data["gender"] = gender
        # Цель
        goal_str = self.goal_entry.get().strip()
        if goal_str:
            try:
                goal = int(goal_str)
                if goal > 0:
                    data["daily_calorie_goal"] = goal
                else:
                    messagebox.showwarning("Ошибка", "Цель должна быть положительным числом")
                    return
            except ValueError:
                messagebox.showwarning("Ошибка", "Цель должна быть целым числом")
                return

        success = self.controller.update_profile(**data)
        if success:
            self.status_label.configure(text="Профиль обновлён", text_color="green")
            self.load_profile()  # перезагрузить, чтобы отобразить актуальные данные
        else:
            self.status_label.configure(text="Ошибка сохранения", text_color="red")

    def logout(self):
        self.controller.logout()
        # Закрыть текущее окно и открыть окно авторизации
        self.winfo_toplevel().destroy()
        from .auth_window import run_auth
        run_auth()