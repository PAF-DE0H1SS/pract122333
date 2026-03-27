# -*- coding: utf-8 -*-

import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
import subprocess
import os


# admin \ 123
class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.db_path = r"W:\pract\day3-day5\db\prackt.db"
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("12 СТУЛЬЕВ - Авторизация")
        self.setFixedSize(350, 200)

        icon_path =r"W:\pract\day3-day5\app\icon\icon.png"
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))

        screen = QtWidgets.QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel("Магазин мебели «12 СТУЛЬЕВ»")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)

        form_layout = QtWidgets.QFormLayout()

        self.edit_login = QtWidgets.QLineEdit()
        self.edit_login.setPlaceholderText("Введите логин")
        self.edit_pass = QtWidgets.QLineEdit()
        self.edit_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.edit_pass.setPlaceholderText("Введите пароль")

        form_layout.addRow("Логин:", self.edit_login)
        form_layout.addRow("Пароль:", self.edit_pass)

        layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()

        self.btn_login = QtWidgets.QPushButton("Вход")
        self.btn_login.setMinimumHeight(30)
        self.btn_login.clicked.connect(self.check_auth)

        self.btn_cancel = QtWidgets.QPushButton("Отмена")
        self.btn_cancel.setMinimumHeight(30)
        self.btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(self.btn_login)
        button_layout.addWidget(self.btn_cancel)

        layout.addLayout(button_layout)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.edit_login.setFocus()

    def check_auth(self):
        login = self.edit_login.text().strip()
        password = self.edit_pass.text().strip()

        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль!")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, login FROM users WHERE login = ? AND password = ?",
                (login, password)
            )

            user = cursor.fetchone()
            conn.close()

            if user:
                QMessageBox.information(
                    self,
                    "Успешно",
                    f"Добро пожаловать, {user[1]}!"
                )
                self.accept()
                self.open_main_window()
            else:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Неверный логин или пароль!"
                )
                self.edit_pass.clear()
                self.edit_pass.setFocus()

        except sqlite3.Error as e:
            QMessageBox.critical(
                self,
                "Ошибка базы данных",
                f"Не удалось подключиться к базе данных:\n{str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка:\n{str(e)}"
            )

    def open_main_window(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            main_path = os.path.join(current_dir, "main.py")

            if os.path.exists(main_path):
                subprocess.Popen([sys.executable, main_path])
            else:
                QMessageBox.warning(
                    self,
                    "Предупреждение",
                    f"Файл main.py не найден по пути:\n{main_path}"
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось запустить main.py:\n{str(e)}"
            )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle('Fusion')

    dialog = LoginDialog()

    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        sys.exit(0)
    else:
        sys.exit(0)