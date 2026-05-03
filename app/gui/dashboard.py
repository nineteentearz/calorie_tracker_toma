import customtkinter as ctk
from datetime import date
from tkcalendar import DateEntry
from tkinter import ttk


class DashboardView(ctk.CTkFrame):
    """Вкладка "Прогресс" с отображением процента выполнения дневной цели."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self, text="Дневной прогресс по калориям", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(10, 20))

        # Фрейм для выбора даты
        date_frame = ctk.CTkFrame(self)
        date_frame.pack(pady=10)

        self.date_label = ctk.CTkLabel(date_frame, text="Дата:")
        self.date_label.pack(side="left", padx=10)

        self.date_picker = DateEntry(date_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_picker.pack(side="left", padx=10)

        self.load_btn = ctk.CTkButton(date_frame, text="Показать", command=self.update_progress)
        self.load_btn.pack(side="left", padx=10)

        # Прогресс-бар
        self.progress_bar = ctk.CTkProgressBar(self, width=400, height=20)
        self.progress_bar.pack(pady=30)
        self.progress_bar.set(0)

        # Текстовая информация
        self.info_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=16), justify="center"
        )
        self.info_label.pack(pady=10)

        # Дополнительная информация о цели
        self.goal_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.goal_label.pack(pady=5)

        # При первом показе загружаем сегодняшнюю дату
        self.update_progress()

    def update_progress(self):
        """Обновляет прогресс на основе выбранной даты."""
        selected_date = self.date_picker.get_date()
        progress_data = self.controller.get_daily_progress(selected_date)

        if progress_data:
            total = progress_data["total_calories"]
            goal = progress_data["daily_goal"]
            percent = progress_data["percentage"]
            self.progress_bar.set(percent / 100.0)
            self.info_label.configure(
                text=f"Потреблено калорий: {total} из {goal}\n"
                     f"Выполнено: {percent}%"
            )
            self.goal_label.configure(text=f"Дневная цель: {goal} ккал")
        else:
            self.progress_bar.set(0)
            self.info_label.configure(text="Нет данных о профиле или цели")
            self.goal_label.configure(text="Установите цель во вкладке 'Профиль'")