"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение файла:
Окно справки о системе.
Предназначено для ознакомления пользователей с возможностями
программного продукта, ролями и порядком работы.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit
)
from PyQt5.QtCore import Qt


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Справка о системе")
        self.setFixedSize(700, 520)

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
            QTextEdit {
                background-color: #ffffff;
                border-radius: 6px;
                padding: 10px;
                border: 1px solid #d1d5db;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("Справка о системе")
        title.setObjectName("title")

        info = QTextEdit()
        info.setReadOnly(True)
        info.setText(
            "ОПИСАНИЕ СИСТЕМЫ\n\n"
            "Данное программное обеспечение предназначено для интеллектуального "
            "анализа финансовой устойчивости предприятия на основе методов "
            "машинного обучения.\n\n"
            "Система позволяет выполнять расчет ключевых финансовых коэффициентов, "
            "оценивать устойчивость предприятия, анализировать динамику показателей "
            "по годам и формировать аналитические отчеты.\n\n"
            "РОЛИ ПОЛЬЗОВАТЕЛЕЙ:\n\n"
            "1. Пользователь\n"
            "   – просмотр результатов оценки финансовой устойчивости;\n"
            "   – ознакомление с аналитическими выводами.\n\n"
            "2. Аналитик\n"
            "   – анализ финансовых коэффициентов;\n"
            "   – прогноз финансовой устойчивости;\n"
            "   – визуализация данных и графиков.\n\n"
            "3. Администратор\n"
            "   – управление учетными записями пользователей;\n"
            "   – обучение и переобучение модели машинного обучения;\n"
            "   – экспорт отчетов в форматы PDF и Excel.\n\n"
            "ПОРЯДОК РАБОТЫ:\n\n"
            "1. Выберите роль пользователя в главном окне системы.\n"
            "2. Воспользуйтесь доступными функциями в соответствии с ролью.\n"
            "3. Для анализа введите финансовые показатели предприятия.\n"
            "4. Результаты анализа отображаются в текстовом и графическом виде.\n\n"
            "Система разработана в рамках выпускной квалификационной работы "
            "и ориентирована на использование в учебных и аналитических целях."
        )

        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(btn_close)

        self.setLayout(layout)
