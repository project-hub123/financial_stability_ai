import sys
from PyQt5.QtWidgets import QApplication

"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение файла:
Точка входа десктопного приложения.
Обеспечивает запуск окна авторизации
и главного окна системы с учетом ролей.
"""

from gui.login_window import LoginWindow
from gui.main_window import MainWindow


def start_main(username: str, role: str):
    """
    Запуск главного окна после успешной авторизации
    """
    global main_window
    main_window = MainWindow(username, role)
    main_window.show()


def main():
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.login_success.connect(start_main)
    login_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
