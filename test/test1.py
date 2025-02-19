import sys
import time
import threading
import random
import json
from PyQt5 import QtWidgets, uic
from last import LastApp  

Form, Window = uic.loadUiType("takwin.ui")


def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  
    except json.JSONDecodeError:
        return []  


questions = load_questions()

class QuizApp(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.score = 0
        self.right_count = 0  
        self.wrong_count = 0  
        self.current_question = 0
        self.start_time = time.time()  
        self.timer = 30
        self.timer_thread = None

        self.option_1.clicked.connect(lambda: self.check_answer(1))
        self.option_2.clicked.connect(lambda: self.check_answer(2))
        self.option_3.clicked.connect(lambda: self.check_answer(3))
        self.option_4.clicked.connect(lambda: self.check_answer(4))

        self.ask_question()

    def start_timer(self):
        self.timer = 30
        self.time_label.setText(f" {self.timer}s")

        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.stop_event = threading.Event()
            self.timer_thread = threading.Thread(target=self.countdown_timer)
            self.timer_thread.start()

    def countdown_timer(self):
        while self.timer > 0:
            if self.stop_event.is_set():
                break
            time.sleep(1)
            self.timer -= 1
            self.time_label.setText(f" {self.timer}s")

        if self.timer == 0:
            self.time_label.setText("Time's up!")
            self.move_to_next_question()

    def ask_question(self):
        if self.current_question < len(questions):
            q = questions[self.current_question]

            options = q["options"].copy()
            correct_answer = options[q["answer"] - 1]
            random.shuffle(options)
            q["answer"] = options.index(correct_answer) + 1

            self.question_label.setText(q["question"])
            self.option_1.setText(options[0])
            self.option_2.setText(options[1])
            self.option_3.setText(options[2])
            self.option_4.setText(options[3])

            self.start_timer()
        else:
            self.end_quiz()

    def move_to_next_question(self):
        self.current_question += 1

        if self.timer_thread and self.timer_thread.is_alive():
            self.stop_event.set()
            self.timer_thread = None

        self.ask_question()

    def check_answer(self, selected_option):
        if self.current_question < len(questions):
            correct_answer = questions[self.current_question]["answer"]

            if self.timer_thread and self.timer_thread.is_alive():
                self.stop_event.set()
                self.timer_thread.join()

            if selected_option == correct_answer:
                self.score += 1
                self.right_count += 1 
            else:
                self.wrong_count += 1  

            self.move_to_next_question()

    def end_quiz(self):
        total_time_taken = int(time.time() - self.start_time)  

        self.results_window = LastApp(self.score, total_time_taken, self.right_count, self.wrong_count)
        self.results_window.show()
        self.close()  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QuizApp()
    window.show()
    sys.exit(app.exec_())
