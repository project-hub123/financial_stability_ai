"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение модуля:
Данный модуль реализует процесс обучения модели машинного обучения
для оценки финансовой устойчивости предприятия.

В рамках модуля выполняются следующие этапы:
– загрузка и анализ исходных данных;
– формирование признакового пространства;
– разделение данных на обучающую и тестовую выборки;
– обучение ML-модели;
– оценка качества модели;
– сохранение обученной модели на диск.
"""

import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from ml.features import calculate_financial_ratios


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def load_dataset(path: str) -> pd.DataFrame:
    """
    Загрузка датасета финансовых показателей предприятия.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл данных не найден: {path}")

    df = pd.read_csv(path)
    return df


def split_features_target(df: pd.DataFrame):
    """
    Разделение датасета на признаки и целевую переменную.
    """
    if "label" not in df.columns:
        raise ValueError("В датасете отсутствует целевая переменная label")

    X_raw = df.drop(columns=["label"])
    y = df["label"]

    return X_raw, y


# ============================================================
# ОБУЧЕНИЕ МОДЕЛИ
# ============================================================

def train_random_forest(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.25,
    random_state: int = 42
):
    """
    Обучение модели Random Forest для классификации
    финансовой устойчивости предприятия.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=6,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=random_state
    )

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred)
    }

    return model, metrics


# ============================================================
# ОСНОВНАЯ ФУНКЦИЯ ОБУЧЕНИЯ
# ============================================================

def train_model(
    data_path: str = "data/financial_data.csv",
    model_path: str = "models/financial_stability_model.pkl"
):
    """
    Полный цикл обучения модели машинного обучения.
    """

    print("=== ЗАПУСК ОБУЧЕНИЯ МОДЕЛИ ===")

    # Загрузка данных
    df = load_dataset(data_path)
    print(f"Загружено строк: {len(df)}")
    print(f"Колонки: {list(df.columns)}")

    # Разделение признаков и целевой переменной
    X_raw, y = split_features_target(df)

    # Формирование признаков
    print("Расчет финансовых коэффициентов...")
    X_features = calculate_financial_ratios(X_raw)

    print(f"Сформировано признаков: {X_features.shape[1]}")

    # Обучение модели
    print("Обучение модели Random Forest...")
    model, metrics = train_random_forest(X_features, y)

    # Вывод метрик
    print("\n=== РЕЗУЛЬТАТЫ ОБУЧЕНИЯ ===")
    print(f"Accuracy  : {metrics['accuracy']:.3f}")
    print(f"Precision : {metrics['precision']:.3f}")
    print(f"Recall    : {metrics['recall']:.3f}")
    print(f"F1-score  : {metrics['f1_score']:.3f}")

    print("\nМатрица ошибок:")
    print(metrics["confusion_matrix"])

    # Сохранение модели
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    print(f"\nМодель сохранена: {model_path}")
    print("=== ОБУЧЕНИЕ ЗАВЕРШЕНО ===")

    return metrics


# ============================================================
# ЗАПУСК МОДУЛЯ КАК САМОСТОЯТЕЛЬНОЙ ПРОГРАММЫ
# ============================================================

if __name__ == "__main__":
    """
    Самостоятельный запуск обучения модели.
    Используется для тестирования и демонстрации работы модуля.
    """

    try:
        train_model()
    except Exception as e:
        print("Ошибка при обучении модели:")
        print(str(e))
