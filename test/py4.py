from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
import sys
from tv import MyApp  
import res_rc


LoginForm, _ = uic.loadUiType("ui4.ui")

class LoginApp(QtWidgets.QMainWindow, LoginForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
        self.login_button.clicked.connect(self.check_login)  

        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        
        correct_username = "a"
        correct_password = "a"

        if username == correct_username and password == correct_password:
            QMessageBox.information(self, "Login Successful", "You have logged in successfully!")
            self.open_tv()  
        else:
            QMessageBox.warning(self, "Login Failed", "Error: Check username or password!")

    def open_tv(self):
        self.tv = MyApp() 
        self.tv.show()  
        self.close()  

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginApp()
    login_window.show()
    sys.exit(app.exec_())
