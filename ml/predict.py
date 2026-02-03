"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Назначение модуля:
Применение обученных моделей машинного обучения
для оценки финансовой устойчивости предприятия
с возможностью выбора модели.
"""

import os
import joblib
import pandas as pd

from ml.features import (
    calculate_financial_ratios,
    interpret_financial_state
)


# ============================================================
# ПУТИ К МОДЕЛЯМ
# ============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODELS = {
    "Random Forest": os.path.join(PROJECT_ROOT, "models", "model1.pkl"),
    "Logistic Regression": os.path.join(PROJECT_ROOT, "models", "model2.pkl"),
}


# ============================================================
# ПРОГНОЗ
# ============================================================

def predict_stability(input_data: dict, model_name: str) -> dict:
    """
    Прогноз финансовой устойчивости с выбором модели.
    """

    if model_name not in MODELS:
        raise ValueError("Неизвестная модель")

    model_path = MODELS[model_name]

    model = joblib.load(model_path)

    df = pd.DataFrame([input_data])

    features = calculate_financial_ratios(df)

    # выравнивание признаков под модель
    if hasattr(model, "feature_names_in_"):
        features = features[model.feature_names_in_]

    prediction = int(model.predict(features)[0])

    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(features)[0][1])

    interpretation = interpret_financial_state(features)

    return {
        "model": model_name,
        "prediction": prediction,
        "probability": probability,
        "features": features.round(3),
        "interpretation": interpretation.iloc[0, 0]
    }


def interpret_prediction(result: dict) -> str:
    status = (
        "ФИНАНСОВО УСТОЙЧИВОЕ"
        if result["prediction"] == 1
        else "ФИНАНСОВО НЕУСТОЙЧИВОЕ"
    )

    text = (
        f"Используемая модель: {result['model']}\n"
        f"Результат оценки: предприятие {status}.\n"
    )

    if result["probability"] is not None:
        text += (
            f"Вероятность устойчивого состояния: "
            f"{result['probability']:.2%}\n"
        )

    text += (
        "\nАнализ коэффициентов:\n"
        f"{result['interpretation']}"
    )

    return text


# ============================================================
# ТЕСТОВЫЙ ЗАПУСК
# ============================================================

if __name__ == "__main__":
    test_data = {
        "year": 2025,
        "current_assets": 1400000,
        "current_liabilities": 900000,
        "equity": 1800000,
        "total_assets": 3200000,
        "profit": 150000
    }

    for model in MODELS:
        print("=" * 50)
        result = predict_stability(test_data, model)
        print(interpret_prediction(result))
