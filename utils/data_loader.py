"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение модуля:
Данный модуль предназначен для загрузки, первичной проверки
и предварительной обработки финансовых данных предприятия.

Модуль используется:
– при обучении моделей машинного обучения;
– при анализе финансовых показателей;
– при подготовке данных для интеллектуального анализа;
– при формировании отчетов и визуализации.
"""

import os
import pandas as pd
import numpy as np


# ============================================================
# КОНСТАНТЫ И НАСТРОЙКИ
# ============================================================

REQUIRED_COLUMNS = [
    "year",
    "current_assets",
    "current_liabilities",
    "equity",
    "total_assets",
    "profit",
    "label"
]


# ============================================================
# ЗАГРУЗКА ДАННЫХ
# ============================================================

def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Загрузка CSV-файла с финансовыми данными предприятия.

    :param file_path: путь к CSV-файлу
    :return: DataFrame с данными
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Файл данных не найден: {file_path}"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("CSV-файл не содержит данных")

    return df


# ============================================================
# ПРОВЕРКА СТРУКТУРЫ ДАННЫХ
# ============================================================

def validate_columns(df: pd.DataFrame) -> None:
    """
    Проверка наличия обязательных колонок в датасете.
    """

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(
            f"В датасете отсутствуют обязательные колонки: {missing}"
        )


def validate_data_types(df: pd.DataFrame) -> None:
    """
    Проверка корректности типов данных.
    """

    numeric_columns = [
        "year",
        "current_assets",
        "current_liabilities",
        "equity",
        "total_assets",
        "profit",
        "label"
    ]

    for col in numeric_columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise TypeError(
                f"Колонка '{col}' должна быть числовой"
            )


# ============================================================
# ПРЕДВАРИТЕЛЬНАЯ ОБРАБОТКА
# ============================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Очистка данных:
    – удаление дубликатов;
    – замена NaN значений;
    – сортировка по годам.
    """

    # Удаление дубликатов
    df = df.drop_duplicates()

    # Замена NaN значений на 0
    df = df.fillna(0)

    # Сортировка по году
    if "year" in df.columns:
        df = df.sort_values("year")

    return df


def normalize_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Нормализация числовых признаков (min-max),
    используется при необходимости.
    """

    df_norm = df.copy()

    numeric_cols = [
        "current_assets",
        "current_liabilities",
        "equity",
        "total_assets",
        "profit"
    ]

    for col in numeric_cols:
        min_val = df_norm[col].min()
        max_val = df_norm[col].max()

        if max_val != min_val:
            df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
        else:
            df_norm[col] = 0

    return df_norm


# ============================================================
# ИНФОРМАЦИОННЫЕ ФУНКЦИИ
# ============================================================

def get_dataset_info(df: pd.DataFrame) -> dict:
    """
    Получение общей информации о датасете
    для отображения в GUI или отчете.
    """

    info = {
        "rows": len(df),
        "columns": list(df.columns),
        "years": sorted(df["year"].unique().tolist())
        if "year" in df.columns else [],
        "labels_distribution": df["label"].value_counts().to_dict()
        if "label" in df.columns else {}
    }

    return info


def print_dataset_summary(df: pd.DataFrame) -> None:
    """
    Вывод краткой сводки по датасету в консоль.
    Удобно для демонстрации и логирования.
    """

    print("=== СВОДКА ПО ДАТАСЕТУ ===")
    print(f"Количество строк: {len(df)}")
    print(f"Колонки: {list(df.columns)}")

    if "year" in df.columns:
        print(
            f"Период данных: {df['year'].min()} – {df['year'].max()}"
        )

    if "label" in df.columns:
        print("Распределение классов:")
        print(df["label"].value_counts())

    print("==========================")


# ============================================================
# КОМПЛЕКСНАЯ ЗАГРУЗКА
# ============================================================

def load_and_prepare_data(file_path: str) -> pd.DataFrame:
    """
    Полный цикл загрузки и подготовки данных:
    – загрузка CSV;
    – проверка структуры;
    – проверка типов;
    – очистка данных.
    """

    df = load_csv_data(file_path)
    validate_columns(df)
    validate_data_types(df)
    df = clean_data(df)

    return df


# ============================================================
# ТЕСТОВЫЙ ЗАПУСК
# ============================================================

if __name__ == "__main__":
    """
    Тестовый запуск модуля загрузки данных.
    Используется для проверки корректности работы.
    """

    try:
        data = load_and_prepare_data(
            "data/financial_data.csv"
        )
        print_dataset_summary(data)

    except Exception as e:
        print("Ошибка при загрузке данных:")
        print(str(e))
