import customtkinter as ctk
from uuid import UUID

class ProductsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.title_label = ctk.CTkLabel(self, text="База продуктов", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(10, 10))

        # Кнопка добавить
        self.add_btn = ctk.CTkButton(self, text="+ Добавить продукт", command=self.add_product_dialog)
        self.add_btn.pack(pady=5)

        # Таблица (scrollable frame)
        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(fill="both", expand=True, pady=10)

        self.refresh_table()

    def refresh_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        products = self.controller.get_all_products()
        if not products:
            label = ctk.CTkLabel(self.table_frame, text="Нет продуктов. Добавьте первый!")
            label.pack(pady=20)
            return

        # Заголовки
        header = ctk.CTkFrame(self.table_frame)
        header.pack(fill="x", pady=2)
        ctk.CTkLabel(header, text="Название", width=250).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Калорий", width=100).pack(side="left", padx=5)
        ctk.CTkLabel(header, text="Действия", width=150).pack(side="left", padx=5)

        for prod in products:
            row = ctk.CTkFrame(self.table_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=prod.name, width=250).pack(side="left", padx=5)
            ctk.CTkLabel(row, text=str(prod.calories_per_unit), width=100).pack(side="left", padx=5)
            btn_frame = ctk.CTkFrame(row)
            btn_frame.pack(side="left", padx=5)
            edit_btn = ctk.CTkButton(btn_frame, text="✏️", width=40, command=lambda p=prod: self.edit_product_dialog(p))
            edit_btn.pack(side="left", padx=2)
            del_btn = ctk.CTkButton(btn_frame, text="🗑️", width=40, fg_color="red", command=lambda p=prod: self.delete_product(p))
            del_btn.pack(side="left", padx=2)

    def add_product_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Новый продукт")
        dialog.geometry("300x200")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Название").pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Калорий (на порцию/100г)").pack(pady=5)
        cal_entry = ctk.CTkEntry(dialog, width=250)
        cal_entry.pack(pady=5)

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
                    self.refresh_table()
                except Exception as e:
                    error_label.configure(text=str(e))
            else:
                error_label.configure(text="Заполните корректно поля")

        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=5)
        ctk.CTkButton(dialog, text="Сохранить", command=save).pack(pady=10)

    def edit_product_dialog(self, product):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Редактировать продукт")
        dialog.geometry("300x200")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Название").pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, width=250)
        name_entry.insert(0, product.name)
        name_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Калорий").pack(pady=5)
        cal_entry = ctk.CTkEntry(dialog, width=250)
        cal_entry.insert(0, str(product.calories_per_unit))
        cal_entry.pack(pady=5)

        def update():
            name = name_entry.get().strip()
            try:
                cal = int(cal_entry.get().strip())
            except:
                cal = 0
            if name and cal > 0:
                try:
                    self.controller.update_product(product.id, name, cal)
                    dialog.destroy()
                    self.refresh_table()
                except Exception as e:
                    error_label.configure(text=str(e))
            else:
                error_label.configure(text="Некорректные данные")

        error_label = ctk.CTkLabel(dialog, text="", text_color="red")
        error_label.pack(pady=5)
        ctk.CTkButton(dialog, text="Сохранить", command=update).pack(pady=10)

    def delete_product(self, product):
        confirm = ctk.CTkToplevel(self)
        confirm.title("Подтверждение")
        confirm.geometry("300x120")
        confirm.grab_set()
        ctk.CTkLabel(confirm, text=f"Удалить продукт '{product.name}'?").pack(pady=10)
        def do_delete():
            self.controller.delete_product(product.id)
            confirm.destroy()
            self.refresh_table()
        ctk.CTkButton(confirm, text="Удалить", fg_color="red", command=do_delete).pack(side="left", padx=20, pady=10)
        ctk.CTkButton(confirm, text="Отмена", command=confirm.destroy).pack(side="right", padx=20, pady=10)