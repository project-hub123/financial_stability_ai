import json
import os
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)

USERS_FILE = "data/users.json"


class ChangePasswordWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("Смена пароля")
        self.setFixedSize(360, 220)

        layout = QVBoxLayout()

        self.old_pass = QLineEdit()
        self.old_pass.setEchoMode(QLineEdit.Password)
        self.old_pass.setPlaceholderText("Старый пароль")

        self.new_pass = QLineEdit()
        self.new_pass.setEchoMode(QLineEdit.Password)
        self.new_pass.setPlaceholderText("Новый пароль")

        self.btn_save = QPushButton("Сохранить пароль")
        self.btn_save.clicked.connect(self.change_password)

        layout.addWidget(QLabel(f"Пользователь: {username}"))
        layout.addWidget(self.old_pass)
        layout.addWidget(self.new_pass)
        layout.addWidget(self.btn_save)

        self.setLayout(layout)

    def change_password(self):
        if not os.path.exists(USERS_FILE):
            QMessageBox.critical(self, "Ошибка", "Файл пользователей не найден")
            return

        with open(USERS_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)

        if users[self.username]["password"] != self.old_pass.text():
            QMessageBox.warning(self, "Ошибка", "Старый пароль неверный")
            return

        users[self.username]["password"] = self.new_pass.text()

        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Готово", "Пароль успешно изменён")
        self.close()
