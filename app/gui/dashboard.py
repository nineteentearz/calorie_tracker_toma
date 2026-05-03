import customtkinter as ctk
from tkinter import messagebox
from datetime import date
from tkcalendar import DateEntry  # для удобного выбора даты, но можно без неё


class DashboardView(ctk.CTkFrame):
    """Вкладка с отображением прогресса по калориям за выбранную дату."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Переменные
        self.selected_date = date.today()

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self, text="Прогресс выполнения дневной цели", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_title.pack(pady=20)

        # Фрейм для выбора даты
        date_frame = ctk.CTkFrame(self)
        date_frame.pack(pady=10, padx=20, fill="x")

        self.label_date = ctk.CTkLabel(date_frame, text="Дата:")
        self.label_date.pack(side="left", padx=5)

        # Поле ввода даты (можно использовать DateEntry из tkcalendar, но требует pip install tkcalendar)
        # Для простоты используем стандартный CTkEntry с валидацией
        self.date_var = ctk.StringVar(value=date.today().isoformat())
        self.date_entry = ctk.CTkEntry(date_frame, textvariable=self.date_var, width=120)
        self.date_entry.pack(side="left", padx=5)

        self.load_btn = ctk.CTkButton(date_frame, text="Показать", command=self.update_progress)
        self.load_btn.pack(side="left", padx=5)

        # Метка для отображения общей суммы калорий и цели
        self.info_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16))
        self.info_label.pack(pady=10)

        # Прогресс-бар (горизонтальный)
        self.progressbar = ctk.CTkProgressBar(self, width=400, height=20)
        self.progressbar.pack(pady=10)
        self.progressbar.set(0)

        # Процент текстом
        self.percent_label = ctk.CTkLabel(self, text="0%", font=ctk.CTkFont(size=18, weight="bold"))
        self.percent_label.pack(pady=5)

        # Дополнительная информация (рекомендация)
        self.advice_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.advice_label.pack(pady=10)

        # Кнопка установки новой цели
        self.set_goal_btn = ctk.CTkButton(self, text="Изменить дневную цель", command=self.change_goal)
        self.set_goal_btn.pack(pady=10)

        # Текущая цель будет отображаться
        self.current_goal_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12))
        self.current_goal_label.pack(pady=5)

        # Обновляем при старте
        self.update_progress()

    def parse_date(self) -> date:
        """Преобразует строку из date_var в объект date."""
        try:
            return date.fromisoformat(self.date_var.get().strip())
        except ValueError:
            return date.today()

    def update_progress(self):
        """Загружает данные и обновляет виджеты."""
        target_date = self.parse_date()
        progress_data = self.controller.get_daily_progress(target_date)
        if progress_data is None:
            self.info_label.configure(text="Профиль не найден. Зайдите в профиль и установите цель.")
            self.progressbar.set(0)
            self.percent_label.configure(text="0%")
            self.advice_label.configure(text="")
            return

        total = progress_data["total_calories"]
        goal = progress_data["daily_goal"]
        percent = progress_data["percentage"]

        self.info_label.configure(text=f"Потреблено: {total} ккал  |  Цель: {goal} ккал")
        self.progressbar.set(min(percent / 100, 1.0))
        self.percent_label.configure(text=f"{percent}%")
        self.current_goal_label.configure(text=f"Текущая дневная цель: {goal} ккал")

        if percent < 50:
            advice = "До цели ещё далеко. Добавьте приём пищи."
        elif percent < 90:
            advice = f"Осталось {goal - total} ккал. Вы почти у цели!"
        elif percent <= 100:
            advice = "Отлично! Цель выполнена."
        else:
            advice = "Вы превысили цель. Возможно, стоит увеличить физическую активность."
        self.advice_label.configure(text=advice)

    def change_goal(self):
        """Диалог для установки новой дневной цели."""
        dialog = ctk.CTkInputDialog(text="Введите новую дневную норму калорий:", title="Изменение цели")
        new_goal_str = dialog.get_input()
        if new_goal_str:
            try:
                new_goal = int(new_goal_str)
                if new_goal > 0:
                    if self.controller.set_daily_goal(new_goal):
                        self.update_progress()
                    else:
                        messagebox.showerror("Ошибка", "Не удалось обновить цель.")
                else:
                    messagebox.showwarning("Ошибка", "Цель должна быть положительным числом.")
            except ValueError:
                messagebox.showwarning("Ошибка", "Введите целое число.")