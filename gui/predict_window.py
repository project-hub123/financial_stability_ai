"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение файла:
Окно оценки финансовой устойчивости предприятия.
Обеспечивает ввод финансовых показателей, запуск прогноза
и отображение результатов интеллектуального анализа.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt

from ml.predict import predict_stability, interpret_prediction


class PredictWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    # ---------------------------------------------------------
    # ИНТЕРФЕЙС
    # ---------------------------------------------------------

    def init_ui(self):
        self.setWindowTitle("Оценка финансовой устойчивости")
        self.setFixedSize(720, 520)

        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: Segoe UI;
                font-size: 13px;
            }
            QLabel#title {
                font-size: 17px;
                font-weight: bold;
                color: #1f2937;
            }
            QLabel#subtitle {
                font-size: 13px;
                color: #374151;
            }
            QLabel.field {
                color: #374151;
                font-weight: bold;
            }
            QLineEdit {
                padding: 8px;
                border-radius: 5px;
                border: 1px solid #d1d5db;
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
            QLabel#result {
                font-size: 14px;
                padding: 10px;
                background-color: #e5e7eb;
                border-radius: 6px;
            }
            QFrame#line {
                background-color: #d1d5db;
            }
        """)

        main_layout = QVBoxLayout()

        # -----------------------------------------------------
        # Заголовок
        # -----------------------------------------------------

        title = QLabel("Оценка финансовой устойчивости предприятия")
        title.setObjectName("title")

        subtitle = QLabel(
            "Введите основные финансовые показатели для анализа"
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
        # Поля ввода
        # -----------------------------------------------------

        self.inputs = {}

        fields = [
            ("Год", "year"),
            ("Оборотные активы", "current_assets"),
            ("Краткосрочные обязательства", "current_liabilities"),
            ("Собственный капитал", "equity"),
            ("Валюта баланса", "total_assets"),
            ("Чистая прибыль", "profit"),
        ]

        for label_text, key in fields:
            row = QVBoxLayout()

            label = QLabel(label_text)
            label.setProperty("class", "field")
            label.setObjectName("field")

            edit = QLineEdit()
            edit.setPlaceholderText("Введите значение")

            self.inputs[key] = edit

            row.addWidget(label)
            row.addWidget(edit)
            main_layout.addLayout(row)

        # -----------------------------------------------------
        # Кнопка запуска
        # -----------------------------------------------------

        btn_predict = QPushButton("Выполнить анализ")
        btn_predict.clicked.connect(self.run_prediction)

        main_layout.addSpacing(10)
        main_layout.addWidget(btn_predict)

        # -----------------------------------------------------
        # Результат
        # -----------------------------------------------------

        self.result_label = QLabel("Результат анализа будет отображён здесь")
        self.result_label.setObjectName("result")
        self.result_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.result_label.setWordWrap(True)

        main_layout.addSpacing(15)
        main_layout.addWidget(self.result_label)

        self.setLayout(main_layout)

    # ---------------------------------------------------------
    # ЛОГИКА ПРОГНОЗА
    # ---------------------------------------------------------

    def run_prediction(self):
        try:
            input_data = {}

            for key, widget in self.inputs.items():
                value = widget.text().strip()
                if not value:
                    raise ValueError("Все поля должны быть заполнены")

                if key == "year":
                    input_data[key] = int(value)
                else:
                    input_data[key] = float(value)

            result = predict_stability(input_data)
            text = interpret_prediction(result)

            self.result_label.setText(text)

        except ValueError as e:
            QMessageBox.warning(
                self,
                "Ошибка ввода",
                str(e)
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка при выполнении анализа:\n{str(e)}"
            )
