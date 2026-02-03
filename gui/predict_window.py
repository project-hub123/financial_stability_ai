"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Назначение:
Окно оценки финансовой устойчивости
с выбором модели машинного обучения.
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QTextEdit, QMessageBox
)

from ml.predict import predict_stability, interpret_prediction


class PredictWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Оценка финансовой устойчивости")
        self.setFixedSize(420, 560)

        layout = QVBoxLayout()

        self.model_selector = QComboBox()
        self.model_selector.addItems([
            "Random Forest",
            "Logistic Regression"
        ])

        layout.addWidget(QLabel("Выбор модели:"))
        layout.addWidget(self.model_selector)

        self.inputs = {}

        fields = [
            ("year", "Год"),
            ("current_assets", "Оборотные активы"),
            ("current_liabilities", "Краткосрочные обязательства"),
            ("equity", "Собственный капитал"),
            ("total_assets", "Всего активов"),
            ("profit", "Прибыль")
        ]

        for key, label in fields:
            layout.addWidget(QLabel(label))
            edit = QLineEdit()
            layout.addWidget(edit)
            self.inputs[key] = edit

        self.btn_predict = QPushButton("Оценить устойчивость")
        self.btn_predict.clicked.connect(self.run_prediction)

        self.output = QTextEdit()
        self.output.setReadOnly(True)

        layout.addWidget(self.btn_predict)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def run_prediction(self):
        try:
            data = {k: float(v.text()) for k, v in self.inputs.items()}
            data["year"] = int(data["year"])

            model_name = self.model_selector.currentText()

            result = predict_stability(data, model_name)

            self.output.setText(
                interpret_prediction(result)
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                str(e)
            )
