"""
Окно администратора системы
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QLineEdit, QComboBox, QMessageBox, QListWidget
)

from utils.user_manager import add_user, remove_user, load_users
from ml.train import train_model


class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Панель администратора")
        self.setFixedSize(500, 500)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Управление пользователями"))

        self.user_list = QListWidget()
        layout.addWidget(self.user_list)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Имя пользователя")

        self.role_box = QComboBox()
        self.role_box.addItems(["Пользователь", "Аналитик", "Администратор"])

        btn_add = QPushButton("Добавить пользователя")
        btn_remove = QPushButton("Удалить пользователя")
        btn_train = QPushButton("Обучить модель")

        btn_add.clicked.connect(self.add_user)
        btn_remove.clicked.connect(self.remove_user)
        btn_train.clicked.connect(self.train)

        layout.addWidget(self.username_input)
        layout.addWidget(self.role_box)
        layout.addWidget(btn_add)
        layout.addWidget(btn_remove)
        layout.addWidget(QLabel("Обучение модели"))
        layout.addWidget(btn_train)

        self.setLayout(layout)
        self.refresh_users()

    def refresh_users(self):
        self.user_list.clear()
        users = load_users()
        for u, r in users.items():
            self.user_list.addItem(f"{u} ({r})")

    def add_user(self):
        try:
            add_user(
                self.username_input.text(),
                self.role_box.currentText()
            )
            self.refresh_users()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def remove_user(self):
        try:
            username = self.username_input.text()
            remove_user(username)
            self.refresh_users()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", str(e))

    def train(self):
        try:
            train_model()
            QMessageBox.information(
                self,
                "Обучение",
                "Модель успешно обучена"
            )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
