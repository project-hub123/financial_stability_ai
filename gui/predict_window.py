"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение файла:
Главное окно десктопного приложения.
Обеспечивает выбор пользователя, доступ ко всем функциям системы
и навигацию по интеллектуальному анализу финансовой устойчивости.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.current_role = "Аналитик"
        self.init_ui()

    # ---------------------------------------------------------
    # ИНТЕРФЕЙС
    # ---------------------------------------------------------

    def init_ui(self):
        self.setWindowTitle(
            "Интеллектуальный анализ финансовой устойчивости"
        )
        self.setFixedSize(720, 420)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: Segoe UI;
                font-size: 13px;
            }
            QLabel#title {
                font-size: 18px;
                font-weight: bold;
                color: #1f2937;
            }
            QLabel#subtitle {
                font-size: 13px;
                color: #374151;
            }
            QLabel#role {
                font-weight: bold;
                color: #2563eb;
            }
            QFrame#line {
                background-color: #d1d5db;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 6px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
            QPushButton#danger {
                background-color: #6b7280;
            }
            QPushButton#danger:hover {
                background-color: #4b5563;
            }
            QComboBox {
                padding: 6px;
                border-radius: 5px;
            }
        """)

        main_layout = QVBoxLayout()

        # -----------------------------------------------------
        # Заголовок
        # -----------------------------------------------------

        title = QLabel(
            "ООО «НТЦ АРМ-Регистр»"
        )
        title.setObjectName("title")

        subtitle = QLabel(
            "Интеллектуальная система анализа финансовой устойчивости"
        )
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Линия
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(1)
        line.setObjectName("line")
        main_layout.addWidget(line)

        # -----------------------------------------------------
        # Панель пользователя
        # -----------------------------------------------------

        user_layout = QHBoxLayout()

        role_label = QLabel("Текущий пользователь:")
        self.role_value = QLabel(self.current_role)
        self.role_value.setObjectName("role")

        self.role_selector = QComboBox()
        self.role_selector.addItems([
            "Аналитик",
            "Администратор"
        ])
        self.role_selector.currentTextChanged.connect(
            self.change_role
        )

        user_layout.addWidget(role_label)
        user_layout.addWidget(self.role_value)
        user_layout.addStretch()
        user_layout.addWidget(QLabel("Сменить роль:"))
        user_layout.addWidget(self.role_selector)

        main_layout.addLayout(user_layout)

        # -----------------------------------------------------
        # Кнопки действий
        # -----------------------------------------------------

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(12)

        self.btn_train = QPushButton("Обучение модели")
        self.btn_predict = QPushButton("Оценка устойчивости")
        self.btn_analysis = QPushButton("Анализ коэффициентов")
        self.btn_reports = QPushButton("Отчёты и результаты")
        self.btn_exit = QPushButton("Выход")
        self.btn_exit.setObjectName("danger")

        self.btn_train.clicked.connect(self.on_train)
        self.btn_predict.clicked.connect(self.on_predict)
        self.btn_analysis.clicked.connect(self.on_analysis)
        self.btn_reports.clicked.connect(self.on_reports)
        self.btn_exit.clicked.connect(self.close)

        buttons_layout.addWidget(self.btn_train)
        buttons_layout.addWidget(self.btn_predict)
        buttons_layout.addWidget(self.btn_analysis)
        buttons_layout.addWidget(self.btn_reports)
        buttons_layout.addWidget(self.btn_exit)

        main_layout.addSpacing(20)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.update_access_rights()

    # ---------------------------------------------------------
    # ЛОГИКА РОЛЕЙ
    # ---------------------------------------------------------

    def change_role(self, role: str):
        self.current_role = role
        self.role_value.setText(role)
        self.update_access_rights()

    def update_access_rights(self):
        """
        Управление доступом к функциям системы
        в зависимости от роли пользователя.
        """

        if self.current_role == "Аналитик":
            self.btn_train.setEnabled(False)
        else:
            self.btn_train.setEnabled(True)

    # ---------------------------------------------------------
    # ОБРАБОТЧИКИ КНОПОК
    # ---------------------------------------------------------

    def on_train(self):
        QMessageBox.information(
            self,
            "Обучение модели",
            "Запуск процедуры обучения модели\n"
            "доступен только администратору."
        )

    def on_predict(self):
        QMessageBox.information(
            self,
            "Оценка устойчивости",
            "Переход к модулю оценки финансовой устойчивости."
        )

    def on_analysis(self):
        QMessageBox.information(
            self,
            "Анализ коэффициентов",
            "Отображение финансовых коэффициентов\n"
            "и аналитических показателей."
        )

    def on_reports(self):
        QMessageBox.information(
            self,
            "Отчёты",
            "Формирование отчётов и просмотр\n"
            "результатов интеллектуального анализа."
        )
