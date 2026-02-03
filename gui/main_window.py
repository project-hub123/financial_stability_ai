"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение файла:
Главное окно десктопного приложения.
Обеспечивает разграничение прав доступа,
навигацию по функциям системы и доступ
к справочной информации.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt

# Окна системы
from gui.predict_window import PredictWindow
from gui.analysis_window import AnalysisWindow
from gui.admin_window import AdminWindow
from gui.help_window import HelpWindow


class MainWindow(QWidget):
    def __init__(self, role: str):
        super().__init__()

        # Роль пользователя задаётся при авторизации
        self.current_role = role

        self.init_ui()
        self.update_access_rights()

    # ---------------------------------------------------------
    # ИНТЕРФЕЙС
    # ---------------------------------------------------------

    def init_ui(self):
        self.setWindowTitle(
            "Интеллектуальный анализ финансовой устойчивости"
        )
        self.setFixedSize(760, 500)

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
        """)

        main_layout = QVBoxLayout()

        # -----------------------------------------------------
        # Заголовок
        # -----------------------------------------------------

        title = QLabel("ООО «НТЦ АРМ-Регистр»")
        title.setObjectName("title")

        subtitle = QLabel(
            "Интеллектуальная система анализа финансовой устойчивости"
        )
        subtitle.setObjectName("subtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFixedHeight(1)
        line.setObjectName("line")
        main_layout.addWidget(line)

        # -----------------------------------------------------
        # Информация о пользователе
        # -----------------------------------------------------

        user_layout = QHBoxLayout()

        role_label = QLabel("Роль пользователя:")
        self.role_value = QLabel(self.current_role)
        self.role_value.setObjectName("role")

        user_layout.addWidget(role_label)
        user_layout.addWidget(self.role_value)
        user_layout.addStretch()

        main_layout.addLayout(user_layout)

        # -----------------------------------------------------
        # КНОПКИ ДЕЙСТВИЙ
        # -----------------------------------------------------

        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(12)

        self.btn_predict = QPushButton("Оценка финансовой устойчивости")
        self.btn_analysis = QPushButton("Анализ коэффициентов")
        self.btn_train = QPushButton("Обучение модели")
        self.btn_admin = QPushButton("Панель администратора")
        self.btn_help = QPushButton("Справка о системе")
        self.btn_exit = QPushButton("Выход")
        self.btn_exit.setObjectName("danger")

        self.btn_predict.clicked.connect(self.on_predict)
        self.btn_analysis.clicked.connect(self.on_analysis)
        self.btn_train.clicked.connect(self.on_train)
        self.btn_admin.clicked.connect(self.on_admin)
        self.btn_help.clicked.connect(self.on_help)
        self.btn_exit.clicked.connect(self.close)

        buttons_layout.addWidget(self.btn_predict)
        buttons_layout.addWidget(self.btn_analysis)
        buttons_layout.addWidget(self.btn_train)
        buttons_layout.addWidget(self.btn_admin)
        buttons_layout.addWidget(self.btn_help)
        buttons_layout.addWidget(self.btn_exit)

        main_layout.addSpacing(20)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    # ---------------------------------------------------------
    # ЛОГИКА РОЛЕЙ
    # ---------------------------------------------------------

    def update_access_rights(self):
        """Разграничение доступа в зависимости от роли."""

        if self.current_role == "Пользователь":
            self.btn_analysis.setEnabled(False)
            self.btn_train.setEnabled(False)
            self.btn_admin.setEnabled(False)

        elif self.current_role == "Аналитик":
            self.btn_analysis.setEnabled(True)
            self.btn_train.setEnabled(False)
            self.btn_admin.setEnabled(False)

        elif self.current_role == "Администратор":
            self.btn_analysis.setEnabled(True)
            self.btn_train.setEnabled(True)
            self.btn_admin.setEnabled(True)

    # ---------------------------------------------------------
    # ОБРАБОТЧИКИ КНОПОК
    # ---------------------------------------------------------

    def on_predict(self):
        self.predict_window = PredictWindow()
        self.predict_window.show()

    def on_analysis(self):
        if self.current_role == "Пользователь":
            QMessageBox.warning(
                self,
                "Доступ запрещён",
                "Анализ коэффициентов доступен "
                "только аналитику и администратору."
            )
            return

        self.analysis_window = AnalysisWindow(self.current_role)
        self.analysis_window.show()

    def on_train(self):
        if self.current_role != "Администратор":
            QMessageBox.warning(
                self,
                "Доступ запрещён",
                "Обучение модели доступно "
                "только администратору."
            )
            return

        QMessageBox.information(
            self,
            "Обучение модели",
            "Запуск обучения осуществляется "
            "из панели администратора."
        )

    def on_admin(self):
        if self.current_role != "Администратор":
            QMessageBox.warning(
                self,
                "Доступ запрещён",
                "Панель администратора доступна "
                "только администратору."
            )
            return

        self.admin_window = AdminWindow()
        self.admin_window.show()

    def on_help(self):
        self.help_window = HelpWindow()
        self.help_window.show()
