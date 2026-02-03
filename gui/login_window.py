"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Назначение файла:
Окно авторизации пользователей системы.
Обеспечивает вход в приложение с учетом ролей доступа.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt5.QtCore import pyqtSignal


class LoginWindow(QWidget):
    # сигнал успешного входа (username, role)
    login_success = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Авторизация")
        self.setFixedSize(360, 280)

        layout = QVBoxLayout()

        title = QLabel("Вход в систему")
        title.setStyleSheet("font-size:16px; font-weight:bold;")
        layout.addWidget(title)

        # ---- Логин ----
        layout.addWidget(QLabel("Логин:"))
        self.login_input = QLineEdit()
        layout.addWidget(self.login_input)

        # ---- Пароль ----
        layout.addWidget(QLabel("Пароль:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # ---- Роль ----
        layout.addWidget(QLabel("Роль пользователя:"))
        self.role_selector = QComboBox()
        self.role_selector.addItems([
            "Пользователь",
            "Аналитик",
            "Администратор"
        ])
        layout.addWidget(self.role_selector)

        # ---- Кнопки ----
        btn_layout = QHBoxLayout()

        self.btn_login = QPushButton("Войти")
        self.btn_exit = QPushButton("Выход")

        self.btn_login.clicked.connect(self.login)
        self.btn_exit.clicked.connect(self.close)

        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_exit)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def login(self):
        """
        Проверка данных пользователя.
        """

        username = self.login_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_selector.currentText()

        if not username or not password:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите логин и пароль."
            )
            return

        # ---- ПРОВЕРКА РОЛИ ----
        if role == "Администратор" and username != "admin":
            QMessageBox.warning(
                self,
                "Ошибка",
                "Для роли администратора используйте логин: admin"
            )
            return

        # ---- УСПЕШНЫЙ ВХОД ----
        self.login_success.emit(username, role)
        self.close()
