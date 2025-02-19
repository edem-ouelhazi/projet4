import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi


def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  
    except json.JSONDecodeError:
        return []  


def save_questions(questions):
    try:
        with open("questions.json", "w", encoding="utf-8") as file:
            json.dump(questions, file, indent=4)  
    except Exception as e:
        print(f"Error saving questions: {e}")

class QuestionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("question.ui", self)  

        self.add.clicked.connect(self.add_question)  
        self.remove.clicked.connect(self.remove_question)  

        
        self.questions = load_questions()

        
        self.populate_list()

    def populate_list(self):
        self.list1.clear()
        for question in self.questions:
            item = QListWidgetItem(question["question"])
            self.list1.addItem(item)

    def add_question(self):
        question_text = self.qinput.text()
        choice1 = self.choice1.text()
        choice2 = self.choice2.text()
        choice3 = self.choice3.text()
        choice4 = self.choice4.text()
        right_answer = int(self.rightanswer.currentText())

        if question_text and choice1 and choice2 and choice3 and choice4:
            new_question = {
                "question": question_text,
                "options": [choice1, choice2, choice3, choice4],
                "answer": right_answer
            }
            self.questions.append(new_question)  
            self.save_questions(self.questions) 
            self.populate_list()  

            QMessageBox.information(self, "Success", "Question added successfully!")
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def remove_question(self):
        selected_item = self.list1.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Warning", "Please select a question to remove!")
            return

        selected_text = selected_item.text()

        
        self.questions = [q for q in self.questions if q["question"] != selected_text]

        
        self.populate_list()
        self.save_questions(self.questions)

        QMessageBox.information(self, "Success", "Question removed successfully!")

    def save_questions(self, questions):
        try:
            with open("questions.json", "w", encoding="utf-8") as file:
                json.dump(questions, file, indent=4)  
        except Exception as e:
            print(f"Error saving questions: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionApp()
    window.show()
    sys.exit(app.exec_())
