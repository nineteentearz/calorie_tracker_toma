import customtkinter as ctk
from tkcalendar import DateEntry
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date, timedelta


class ReportView(ctk.CTkFrame):
    """Вкладка с графиком калорий за выбранный период."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Заголовок
        self.title_label = ctk.CTkLabel(
            self, text="Диаграмма калорий", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(10, 10))

        # Фрейм для выбора периода
        period_frame = ctk.CTkFrame(self)
        period_frame.pack(pady=10)

        self.start_label = ctk.CTkLabel(period_frame, text="С:")
        self.start_label.grid(row=0, column=0, padx=5)
        self.start_date = DateEntry(period_frame, width=10, date_pattern='yyyy-mm-dd')
        self.start_date.grid(row=0, column=1, padx=5)

        self.end_label = ctk.CTkLabel(period_frame, text="По:")
        self.end_label.grid(row=0, column=2, padx=5)
        self.end_date = DateEntry(period_frame, width=10, date_pattern='yyyy-mm-dd')
        self.end_date.grid(row=0, column=3, padx=5)

        self.show_btn = ctk.CTkButton(period_frame, text="Построить", command=self.plot_calories)
        self.show_btn.grid(row=0, column=4, padx=10)

        # Метка для отображения ошибок
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        # Фрейм для графика
        self.figure_frame = ctk.CTkFrame(self)
        self.figure_frame.pack(fill="both", expand=True, pady=20)

        # По умолчанию покажем график за последние 7 дней
        self.end_date.set_date(date.today())
        self.start_date.set_date(date.today() - timedelta(days=6))
        self.plot_calories()

    def plot_calories(self):
        start = self.start_date.get_date()
        end = self.end_date.get_date()
        if start > end:
            self.error_label.configure(text="Ошибка: начальная дата позже конечной")
            return

        data = self.controller.get_calories_for_range(start, end)
        if not data:
            self.error_label.configure(text="Нет данных за выбранный период")
            return

        # Очищаем старый график
        for widget in self.figure_frame.winfo_children():
            widget.destroy()

        # Создаём новый график
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        dates = [d["date"] for d in data]
        calories = [d["total_calories"] for d in data]

        ax.bar(dates, calories, color='skyblue', edgecolor='navy')
        ax.set_xlabel("Дата")
        ax.set_ylabel("Калории (ккал)")
        ax.set_title("Потребление калорий по дням")
        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        self.error_label.configure(text="")