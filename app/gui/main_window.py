import customtkinter as ctk
from .dashboard import DashboardView
from .meal_entry import MealEntryView
from .report_view import ReportView
from .profile_view import ProfileView


class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Calorie Tracker - Главная")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Настройка внешнего вида
        ctk.set_appearance_mode("dark")  # или "light", позже сделаем переключатель

        # Создаём вкладки
        self.tabview = ctk.CTkTabview(self, width=900, height=600)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        # Добавляем вкладки
        self.tabview.add("📊 Прогресс")
        self.tabview.add("🍽️ Добавить приём пищи")
        self.tabview.add("📈 Диаграмма калорий")
        self.tabview.add("👤 Профиль")

        # Инициализируем виджеты каждой вкладки
        self.dashboard = DashboardView(self.tabview.tab("📊 Прогресс"), self.controller)
        self.meal_entry = MealEntryView(self.tabview.tab("🍽️ Добавить приём пищи"), self.controller)
        self.report = ReportView(self.tabview.tab("📈 Диаграмма калорий"), self.controller)
        self.profile = ProfileView(self.tabview.tab("👤 Профиль"), self.controller)

        # Переключатель темы (в правом верхнем углу)
        self.theme_switch = ctk.CTkSwitch(
            self, text="Тёмная тема", command=self.toggle_theme,
            onvalue="dark", offvalue="light"
        )
        self.theme_switch.place(relx=0.98, rely=0.02, anchor="ne")
        self.theme_switch.select()  # по умолчанию тёмная

        # Обработчик закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_theme(self):
        if self.theme_switch.get() == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def on_closing(self):
        self.controller.close()
        self.destroy()