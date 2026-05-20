import tkinter as tk
from tkinter import messagebox

# --- База данных вопросов ---
questions = [
    # Вопрос 1 (Сохраняем для примера)
    {
        "question": "Что означает этот знак? (Знак 'Въезд запрещен')",
        "options": [
            "А) Запрещено движение всех транспортных средств",
            "Б) Движение прямо запрещено",
            "В) Въезд запрещен",
            "Г) Остановка запрещена"
        ],
        "correct": 2
    },
    # Вопрос 2 (Сохраняем для примера)
    {
        "question": "С какой максимальной скоростью разрешено движение в населенном пункте?",
        "options": [
            "А) 40 км/ч",
            "Б) 60 км/ч",
            "В) 80 км/ч",
            "Г) 100 км/ч"
        ],
        "correct": 1
    },
    # Новые вопросы
    {
        "question": "В каких случаях Вы обязаны уступить дорогу автомобилю с включенными проблесковым маячком синего цвета и специальным звуковым сигналом?",
        "options": [
            "А) Только если он движется сзади",
            "Б) Если его водитель показывает, что намерен совершить обгон",
            "В) Если его водитель показывает, что намерен совершить поворот налево",
            "Г) В любом случае, если он приближается к Вам"
        ],
        "correct": 3
    },
    {
        "question": "Что означает прерывистая линия разметки (1.5), разделяющая транспортные потоки противоположных направлений?",
        "options": [
            "А) Обгон запрещен",
            "Б) Разрешен обгон с любой стороны",
            "В) Разрешен обгон только с прерывистой стороны",
            "Г) Разрешен обгон, если это безопасно"
        ],
        "correct": 3
    },
    {
        "question": "Разрешается ли Вам остановка в указанном месте?",
        "options": [
            "А) Разрешается только для посадки или высадки пассажиров",
            "Б) Разрешается, если это не создаст помех маршрутным транспортным средствам",
            "В) Запрещается",
            "Г) Разрешается на время не более 5 минут"
        ],
        "correct": 2 # Ответ зависит от конкретного знака на картинке, но в общем тесте часто это 'Запрещено'
    },
    {
        "question": "Кто из водителей нарушил правила стоянки?",
        "options": [
            "А) Только водитель автомобиля А",
            "Б) Только водитель автомобиля Б",
            "В) Оба водителя",
            "Г) Никто не нарушил"
        ],
        "correct": 1 # Ответ зависит от схемы расстановки машин
    },
    {
        "question": "При движении в темное время суток на неосвещенных участках дорог Вы должны использовать:",
        "options": [
            "А) Только габаритные огни",
            "Б) Ближний или дальний свет фар",
            "В) Противотуманные фары",
            "Г) Аварийную сигнализацию"
        ],
        "correct": 1
    },
    {
        "question": "Вы намерены повернуть направо. Можете ли Вы приступить к повороту?",
        "options": [
            "А) Да, уступив дорогу пешеходам и велосипедистам",
            "Б) Да, только после звукового сигнала",
            "В) Нет, так как создадите помеху встречному автомобилю",
            "Г) Да, так как у Вас главная дорога"
        ],
        "correct": 3 # Ответ зависит от приоритета на перекрестке
    },
    {
        "question": "Какое расстояние должно быть обеспечено между транспортными средствами при буксировке на жесткой сцепке?",
        "options": [
            "А) Не более 1 метра",
            "Б) От 4 до 6 метров",
            "В) Более 10 метров",
            "Г) Не регламентируется"
        ],
        "correct": 2
    },
    {
        "question": "Разрешается ли Вам продолжить движение в прямом направлении на перекрестке?",
        "options": [
            "А) Да, у Вас главная дорога",
            "Б) Да, так как Вы движетесь прямо",
            "В) Нет, Вы должны уступить дорогу трамваю",
            "Г) Нет, Вы должны уступить дорогу автомобилю справа"
        ],
        "correct": 3 # Ответ зависит от типа перекрестка и знаков
    },
    {
        "question": "Что означает требование уступить дорогу?",
        "options": [
            "А) Остановиться в любом случае",
            "Б) Не возобновлять движение, если это вынудит других участников изменить скорость или направление",
            "В) Снизить скорость и проехать перекресток без остановки",
            "Г) Подать звуковой сигнал и проехать первым"
        ],
        "correct": 1
    },

]

class PDDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Экзамен ПДД РФ")
        self.root.geometry("500x400")
        
        self.current_index = 0
        self.score = 0
        self.user_answers = [-1] * len(questions) # -1 значит, что ответ не выбран

        # --- Создание виджетов ---
        self.question_label = tk.Label(root, text="", wraplength=450, font=('Arial', 12))
        self.question_label.pack(pady=10)

        self.var = tk.IntVar()
        
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.var, value=i, font=('Arial', 10))
            rb.pack(anchor='w')
            self.radio_buttons.append(rb)

        self.status_label = tk.Label(root, text="", font=('Arial', 10))
        self.status_label.pack(pady=5)

        # Кнопки навигации и действий
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=15)

        self.prev_btn = tk.Button(btn_frame, text="Назад", command=self.prev_question)
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.submit_btn = tk.Button(btn_frame, text="Ответить", command=self.check_answer)
        self.submit_btn.grid(row=0, column=1, padx=10)

        self.next_btn = tk.Button(btn_frame, text="Далее", command=self.next_question)
        self.next_btn.grid(row=0, column=2, padx=10)

        self.show_answer_btn = tk.Button(btn_frame, text="Показать ответ", command=self.show_correct_answer)
        self.show_answer_btn.grid(row=0, column=3, padx=10)

        # Отображение первого вопроса
        self.display_question()

    def display_question(self):
        """Отображает текущий вопрос и варианты ответов."""
        q_data = questions[self.current_index]
        
        self.question_label.config(text=f"Вопрос {self.current_index + 1}: {q_data['question']}")
        
        for i in range(4):
            self.radio_buttons[i].config(text=q_data['options'][i])
        
        # Сброс выбора радиокнопок при смене вопроса
        self.var.set(-1)
        
        # Обновление статуса
        if self.user_answers[self.current_index] == questions[self.current_index]['correct']:
            self.status_label.config(text="✅ Ответ верный", fg="green")
            self.submit_btn.config(state='disabled')
            self.show_answer_btn.config(state='disabled')
            self.next_btn.config(state='normal')
            self.prev_btn.config(state='normal')
            
            # Блокируем кнопки выбора ответа
            for rb in self.radio_buttons:
                rb.config(state='disabled')
                
        elif self.user_answers[self.current_index] != -1:
            self.status_label.config(text="❌ Ответ неверный", fg="red")
            self.submit_btn.config(state='disabled')
            self.show_answer_btn.config(state='normal')
            self.next_btn.config(state='normal')
            self.prev_btn.config(state='normal')
            
            for rb in self.radio_buttons:
                rb.config(state='disabled')
                
                # Если ответ еще не был дан
                if self.user_answers[self.current_index] == -1:
                    self.status_label.config(text="")
                    self.submit_btn.config(state='normal')
                    self.show_answer_btn.config(state='disabled')
                    self.next_btn.config(state='disabled')
                    self.prev_btn.config(state='normal')
                    
                    for rb in self.radio_buttons:
                        rb.config(state='normal')

    def check_answer(self):
        """Проверяет выбранный ответ."""
        selected = self.var.get()
        
        if selected == -1:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите вариант ответа!")
            return

        self.user_answers[self.current_index] = selected

        if selected == questions[self.current_index]['correct']:
            self.score += 1

        # Обновляем интерфейс для текущего вопроса
        self.display_question()

    def next_question(self):
        """Переходит к следующему вопросу."""
        if self.current_index < len(questions) - 1:
            self.current_index += 1
            self.display_question()

    def prev_question(self):
        """Возвращается к предыдущему вопросу."""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_question()

    def show_correct_answer(self):
        """Показывает правильный ответ для текущего вопроса."""
        correct_idx = questions[self.current_index]['correct']
        
        messagebox.showinfo("Правильный ответ",
                            f"Правильный ответ: {questions[self.current_index]['options'][correct_idx]}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDDApp(root)
    root.mainloop()