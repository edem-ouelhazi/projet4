import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from test1 import QuizApp  
import res1  
from PyQt5.QtCore import QProcess  

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("tv.ui", self) 
        
        
        self.btn.clicked.connect(self.open_quiz)  
        self.formateur.clicked.connect(self.show_password_inputs)  
        self.moon.clicked.connect(self.check_password) 
        
        
        self.line.setVisible(False)
        self.moon.setVisible(False)

        self.correct_password = "admin"  

    def open_quiz(self):
        self.quiz = QuizApp()  
        self.quiz.show()  
        self.close()  

    def show_password_inputs(self):
        
        self.line.setVisible(True)
        self.moon.setVisible(True)

    def check_password(self):
        entered_password = self.line.text()  
        if entered_password == self.correct_password:
            
            self.open_admin_panel()
        else:
            
            QMessageBox.warning(self, "Invalid Password", "Incorrect password!")

    def open_admin_panel(self):
        
        process = QProcess(self)
        process.start("python", ["question.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()  
