import customtkinter as ctk
from datetime import date, timedelta
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ReportView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Переменные
        self.start_date = date.today() - timedelta(days=7)
        self.end_date = date.today()

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self, text="Диаграмма калорий за период", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_title.pack(pady=10)

        # Фрейм для выбора периода
        filter_frame = ctk.CTkFrame(self)
        filter_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(filter_frame, text="С даты:").grid(row=0, column=0, padx=5, pady=5)
        self.start_var = ctk.StringVar(value=self.start_date.isoformat())
        self.start_entry = ctk.CTkEntry(filter_frame, textvariable=self.start_var, width=100)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(filter_frame, text="По дату:").grid(row=0, column=2, padx=5, pady=5)
        self.end_var = ctk.StringVar(value=self.end_date.isoformat())
        self.end_entry = ctk.CTkEntry(filter_frame, textvariable=self.end_var, width=100)
        self.end_entry.grid(row=0, column=3, padx=5, pady=5)

        self.update_btn = ctk.CTkButton(filter_frame, text="Обновить график", command=self.update_chart)
        self.update_btn.grid(row=0, column=4, padx=10, pady=5)

        # Фрейм для графика
        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.figure = plt.Figure(figsize=(8, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Загружаем начальные данные
        self.update_chart()

    def update_chart(self):
        try:
            start = date.fromisoformat(self.start_var.get().strip())
            end = date.fromisoformat(self.end_var.get().strip())
            if start > end:
                messagebox.showwarning("Ошибка", "Начальная дата не может быть позже конечной.")
                return
        except ValueError:
            messagebox.showwarning("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        data = self.controller.get_calories_for_range(start, end)
        if not data:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Нет данных за выбранный период", ha="center", va="center")
            self.canvas.draw()
            return

        dates = [item["date"] for item in data]
        calories = [item["total_calories"] for item in data]

        self.ax.clear()
        self.ax.bar(dates, calories, color='skyblue', edgecolor='navy')
        self.ax.set_xlabel("Дата")
        self.ax.set_ylabel("Калории (ккал)")
        self.ax.set_title("Потребление калорий по дням")
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha="right")
        self.figure.tight_layout()
        self.canvas.draw()