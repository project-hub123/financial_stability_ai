"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович
"""

from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

import pandas as pd

from ml.features import calculate_financial_ratios
from utils.data_loader import load_and_prepare_data


class AnalysisWindow(QWidget):
    def __init__(self, role="Аналитик"):
        super().__init__()
        self.role = role
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Анализ финансовых коэффициентов")
        self.setFixedSize(900, 500)

        layout = QVBoxLayout()

        title = QLabel("Анализ финансовых коэффициентов предприятия")
        title.setStyleSheet("font-size:16px; font-weight:bold;")

        self.table = QTableWidget()

        btn_load = QPushButton("Загрузить и рассчитать коэффициенты")
        btn_load.clicked.connect(self.load_and_analyze)

        layout.addWidget(title)
        layout.addWidget(btn_load)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_and_analyze(self):
        try:
            df = load_and_prepare_data("data/financial_data.csv")
            features = calculate_financial_ratios(df)

            self.table.setRowCount(len(features))
            self.table.setColumnCount(len(features.columns))
            self.table.setHorizontalHeaderLabels(features.columns)

            for i in range(len(features)):
                for j, col in enumerate(features.columns):
                    self.table.setItem(
                        i, j,
                        QTableWidgetItem(str(round(features.iloc[i, j], 3)))
                    )

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
