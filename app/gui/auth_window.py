import customtkinter as ctk
from .controllers import AppController
from .main_window import MainWindow

# Устанавливаем тему и цветовую схему
ctk.set_appearance_mode("dark")   # можно "light"
ctk.set_default_color_theme("green")  # зелёная гамма

class AuthWindow(ctk.CTk):
    """Окно аутентификации (логин и регистрация)."""

    def __init__(self, controller: AppController):
        super().__init__()
        self.controller = controller
        self.title("Calorie Tracker - Вход")
        self.geometry("450x550")
        self.resizable(False, False)

        # Переменные для полей
        self.email_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.confirm_var = ctk.StringVar()

        # Фрейм для формы
        self.frame = ctk.CTkFrame(self, corner_radius=10)
        self.frame.pack(pady=40, padx=40, fill="both", expand=True)

        # Заголовок
        self.label_title = ctk.CTkLabel(
            self.frame, text="Calorie Tracker", font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_title.pack(pady=(20, 10))

        # Поле email
        self.email_entry = ctk.CTkEntry(
            self.frame, placeholder_text="Email", textvariable=self.email_var, width=300
        )
        self.email_entry.pack(pady=10)
        self.email_hint = ctk.CTkLabel(
            self.frame, text="Введите ваш email", font=ctk.CTkFont(size=11), text_color="gray"
        )
        self.email_hint.pack(pady=(0, 5))

        # Поле пароль
        self.password_entry = ctk.CTkEntry(
            self.frame, placeholder_text="Пароль", textvariable=self.password_var,
            show="*", width=300
        )
        self.password_entry.pack(pady=10)
        self.pass_hint = ctk.CTkLabel(
            self.frame, text="Пароль должен содержать не менее 6 символов",
            font=ctk.CTkFont(size=11), text_color="gray"
        )
        self.pass_hint.pack(pady=(0, 5))

        # Поле подтверждения пароля (только для регистрации)
        self.confirm_entry = ctk.CTkEntry(
            self.frame, placeholder_text="Подтвердите пароль", textvariable=self.confirm_var,
            show="*", width=300
        )
        self.confirm_hint = ctk.CTkLabel(
            self.frame, text="Повторите пароль", font=ctk.CTkFont(size=11), text_color="gray"
        )

        # Кнопки
        self.login_btn = ctk.CTkButton(
            self.frame, text="Войти", command=self.login_action, width=300, fg_color="#2ecc71"
        )
        self.login_btn.pack(pady=10)

        self.register_btn = ctk.CTkButton(
            self.frame, text="Регистрация", command=self.register_action,
            fg_color="transparent", border_width=2, width=300
        )
        self.register_btn.pack(pady=5)

        # Метка для сообщений
        self.message_label = ctk.CTkLabel(self.frame, text="", text_color="red")
        self.message_label.pack(pady=10)

        # Режим "регистрация" (показывать доп поле)
        self.is_register_mode = False

    def toggle_register_mode(self, enable: bool):
        self.is_register_mode = enable
        if enable:
            self.confirm_entry.pack(pady=5)
            self.confirm_hint.pack(pady=(0, 5))
            self.login_btn.configure(text="Зарегистрироваться")
            self.register_btn.configure(text="Назад ко входу")
            self.label_title.configure(text="Регистрация")
        else:
            self.confirm_entry.pack_forget()
            self.confirm_hint.pack_forget()
            self.login_btn.configure(text="Войти")
            self.register_btn.configure(text="Регистрация")
            self.label_title.configure(text="Calorie Tracker - Вход")
        self.message_label.configure(text="")

    def login_action(self):
        if self.is_register_mode:
            # Регистрация
            email = self.email_var.get().strip()
            password = self.password_var.get()
            confirm = self.confirm_var.get()
            if not email or not password:
                self.message_label.configure(text="Заполните все поля")
                return
            if len(password) < 6:
                self.message_label.configure(text="Пароль должен быть не менее 6 символов")
                return
            if password != confirm:
                self.message_label.configure(text="Пароли не совпадают")
                return
            success = self.controller.register(email, password)
            if success:
                self.message_label.configure(text="Регистрация успешна! Теперь войдите.", text_color="green")
                self.toggle_register_mode(False)
                self.email_var.set(email)
                self.password_var.set("")
            else:
                self.message_label.configure(text="Пользователь с таким email уже существует")
        else:
            # Логин
            email = self.email_var.get().strip()
            password = self.password_var.get()
            if not email or not password:
                self.message_label.configure(text="Введите email и пароль")
                return
            success = self.controller.login(email, password)
            if success:
                self.destroy()
                main_app = MainWindow(self.controller)
                main_app.mainloop()
            else:
                self.message_label.configure(text="Неверный email или пароль")

    def register_action(self):
        if self.is_register_mode:
            self.toggle_register_mode(False)
        else:
            self.toggle_register_mode(True)

def run_auth():
    controller = AppController()
    if controller.is_authenticated():
        main_app = MainWindow(controller)
        main_app.mainloop()
    else:
        auth_win = AuthWindow(controller)
        auth_win.mainloop()
    controller.close()