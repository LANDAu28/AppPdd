import customtkinter as ctk
from tkinter import ttk
import requests
import json
import os
from datetime import datetime

class CurrencyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Currency Converter Pro")
        self.geometry("600x700")
        
        # Данные
        self.api_key = "ВАШ_КЛЮЧ_ЗДЕСЬ"
        self.history_file = "history.json"
        
        # --- UI: Поля ввода ---
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Сумма", width=200)
        self.amount_entry.pack(pady=10)

        self.cur_from = ctk.CTkComboBox(self, values=["USD", "EUR", "RUB", "GBP", "CNY"])
        self.cur_from.set("USD")
        self.cur_from.pack(pady=5)

        self.cur_to = ctk.CTkComboBox(self, values=["USD", "EUR", "RUB", "GBP", "CNY"])
        self.cur_to.set("RUB")
        self.cur_to.pack(pady=5)

        self.btn = ctk.CTkButton(self, text="Конвертировать", command=self.convert)
        self.btn.pack(pady=20)

        self.res_label = ctk.CTkLabel(self, text="---", font=("Arial", 20, "bold"))
        self.res_label.pack(pady=10)

        # --- UI: Таблица истории ---
        columns = ("date", "from", "to", "result")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=8)
        self.tree.heading("date", text="Дата")
        self.tree.heading("from", text="Из")
        self.tree.heading("to", text="В")
        self.tree.heading("result", text="Итог")
        self.tree.pack(pady=20, padx=20, fill="x")
        
        self.load_history()

    def convert(self):
        amount = self.amount_entry.get()
        
        # Шаг 4: Валидация
        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            self.res_label.configure(text="Введите число > 0", text_color="red")
            return

        from_c, to_c = self.cur_from.get(), self.cur_to.get()
        url = f"https://exchangerate-api.com{self.api_key}/pair/{from_c}/{to_c}/{amount}"

        try:
            data = requests.get(url).json()
            if data["result"] == "success":
                res = round(data["conversion_result"], 2)
                self.res_label.configure(text=f"{res} {to_c}", text_color="green")
                self.save_history(amount, from_c, to_c, res)
        except:
            self.res_label.configure(text="Ошибка связи", text_color="red")

    def save_history(self, amt, f, t, res):
        item = {
            "date": datetime.now().strftime("%d.%m %H:%M"),
            "from": f"{amt} {f}",
            "to": t,
            "result": res
        }
        
        # Загрузка и сохранение JSON
        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                history = json.load(file)
        
        history.append(item)
        with open(self.history_file, "w") as file:
            json.dump(history, file, indent=4)
        
        self.tree.insert("", "0", values=(item["date"], item["from"], item["to"], item["result"]))

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as file:
                for item in json.load(file):
                    self.tree.insert("", "end", values=(item["date"], item["from"], item["to"], item["result"]))

if __name__ == "__main__":
    app = CurrencyApp()
    app.mainloop()
