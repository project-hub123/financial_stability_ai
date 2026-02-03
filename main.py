import sys
import os

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение файла:
Данный файл является точкой входа десктопного интеллектуального сервиса.
Обеспечивает запуск графического интерфейса пользователя и доступ
к функциям обучения и анализа моделей машинного обучения.
"""


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Интеллектуальный анализ финансовой устойчивости предприятия"
        )
        self.setFixedSize(550, 320)

        layout = QVBoxLayout()

        title = QLabel(
            "ООО «НТЦ АРМ-Регистр»\n"
            "Интеллектуальный анализ финансовой устойчивости предприятия\n"
            "на основе методов машинного обучения"
        )
        title.setStyleSheet(
            "font-size:15px; font-weight:bold; margin-bottom:15px;"
        )

        btn_train = QPushButton("Обучить модель")
        btn_predict = QPushButton("Оценить финансовую устойчивость")
        btn_exit = QPushButton("Выход")

        btn_train.clicked.connect(self.train_model)
        btn_predict.clicked.connect(self.predict_info)
        btn_exit.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(btn_train)
        layout.addWidget(btn_predict)
        layout.addWidget(btn_exit)

        self.setLayout(layout)

    def train_model(self):
        """
        Проверка наличия датасета и информирование пользователя
        о процессе обучения модели.
        Основная логика обучения реализуется в модуле ml/train.py.
        """

        if not os.path.exists("data/financial_data.csv"):
            QMessageBox.critical(
                self,
                "Ошибка",
                "Файл данных financial_data.csv не найден.\n"
                "Проверьте наличие датасета в папке data."
            )
            return

        QMessageBox.information(
            self,
            "Обучение модели",
            "Данные для обучения обнаружены.\n"
            "Обучение модели выполняется в модуле ml/train.py.\n"
            "После обучения модель сохраняется в папку models."
        )

    def predict_info(self):
        QMessageBox.information(
            self,
            "Оценка устойчивости",
            "Для оценки финансовой устойчивости предприятия\n"
            "используются обученные модели машинного обучения.\n"
            "Анализ выполняется на основе финансовых показателей."
        )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
