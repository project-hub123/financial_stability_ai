"""
Модуль визуализации финансовых коэффициентов
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_coefficients(df: pd.DataFrame):
    """
    Построение графиков коэффициентов по годам
    """

    if "year" not in df.columns:
        raise ValueError("В данных отсутствует колонка 'year'")

    years = df["year"]

    plt.figure(figsize=(10, 6))

    plt.plot(years, df["current_assets"], label="Оборотные активы")
    plt.plot(years, df["equity"], label="Собственный капитал")
    plt.plot(years, df["profit"], label="Прибыль")

    plt.title("Динамика ключевых финансовых показателей")
    plt.xlabel("Год")
    plt.ylabel("Значение")
    plt.legend()
    plt.grid(True)

    plt.show()
