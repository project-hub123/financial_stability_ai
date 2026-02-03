"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Назначение модуля:
Обучение второй модели машинного обучения (Logistic Regression)
и корректное сравнение с моделью Random Forest
на ОДИНАКОВОМ наборе признаков.
"""

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from ml.features import calculate_financial_ratios


# ============================================================
# ПУТИ ПРОЕКТА
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA_PATH = os.path.join(
    PROJECT_ROOT, "data", "financial_data.csv"
)

MODEL1_PATH = os.path.join(
    PROJECT_ROOT, "models", "model1.pkl"
)

MODEL2_PATH = os.path.join(
    PROJECT_ROOT, "models", "model2.pkl"
)


# ============================================================
# ЗАГРУЗКА ДАННЫХ
# ============================================================

df = pd.read_csv(DATA_PATH)

# признаки БЕРЁМ ТЕ ЖЕ, что использовались при обучении model1
X_features = calculate_financial_ratios(df)

y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X_features,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# ============================================================
# ОБУЧЕНИЕ ВТОРОЙ МОДЕЛИ
# ============================================================

model2 = LogisticRegression(
    max_iter=2000,
    solver="lbfgs"
)

model2.fit(X_train, y_train)


# ============================================================
# ОЦЕНКА ВТОРОЙ МОДЕЛИ
# ============================================================

y_pred_2 = model2.predict(X_test)

metrics_model2 = {
    "Accuracy": accuracy_score(y_test, y_pred_2),
    "Precision": precision_score(y_test, y_pred_2),
    "Recall": recall_score(y_test, y_pred_2),
    "F1-score": f1_score(y_test, y_pred_2)
}


# ============================================================
# ЗАГРУЗКА И ОЦЕНКА ПЕРВОЙ МОДЕЛИ
# ============================================================

model1 = joblib.load(MODEL1_PATH)

y_pred_1 = model1.predict(X_test)

metrics_model1 = {
    "Accuracy": accuracy_score(y_test, y_pred_1),
    "Precision": precision_score(y_test, y_pred_1),
    "Recall": recall_score(y_test, y_pred_1),
    "F1-score": f1_score(y_test, y_pred_1)
}


# ============================================================
# СРАВНЕНИЕ МОДЕЛЕЙ
# ============================================================

comparison = pd.DataFrame.from_dict(
    {
        "Random Forest (model1)": metrics_model1,
        "Logistic Regression (model2)": metrics_model2
    },
    orient="index"
)

print("=== СРАВНЕНИЕ МОДЕЛЕЙ ===")
print(comparison.round(3))


# ============================================================
# СОХРАНЕНИЕ ВТОРОЙ МОДЕЛИ
# ============================================================

joblib.dump(model2, MODEL2_PATH)

print("\nВторая модель сохранена:")
print(MODEL2_PATH)
