"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение модуля:
Применение обученной модели машинного обучения
для оценки финансовой устойчивости предприятия.

Модуль используется:
– в графическом интерфейсе пользователя;
– при анализе отдельных финансовых периодов;
– при демонстрации результатов работы системы на защите ВКР.
"""

import os
import joblib
import pandas as pd

from ml.features import (
    calculate_financial_ratios,
    interpret_financial_state
)

# ============================================================
# ОПРЕДЕЛЕНИЕ КОРНЯ ПРОЕКТА
# ============================================================

# ml/predict.py → поднимаемся на уровень проекта
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT, "models", "model1.pkl"
)

# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def load_model(model_path: str):
    """Загрузка обученной ML-модели."""
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Файл модели не найден: {model_path}"
        )
    return joblib.load(model_path)


def prepare_input_data(input_data: dict) -> pd.DataFrame:
    """
    Преобразование входных данных пользователя
    в DataFrame для дальнейшего анализа.
    """
    required_fields = [
        "year",
        "current_assets",
        "current_liabilities",
        "equity",
        "total_assets",
        "profit"
    ]

    for field in required_fields:
        if field not in input_data:
            raise ValueError(
                f"Отсутствует обязательное поле: {field}"
            )

    return pd.DataFrame([input_data])


# ============================================================
# ПРОГНОЗ ФИНАНСОВОЙ УСТОЙЧИВОСТИ
# ============================================================

def predict_stability(input_data: dict) -> dict:
    """
    Прогноз финансовой устойчивости предприятия
    на основе введенных финансовых показателей.
    """

    # загрузка модели
    model = load_model(MODEL_PATH)

    # подготовка данных
    raw_df = prepare_input_data(input_data)

    # расчет признаков
    features = calculate_financial_ratios(raw_df)

    # прогноз класса
    prediction = int(model.predict(features)[0])

    # вероятность устойчивости
    probability_stable = None
    if hasattr(model, "predict_proba"):
        probability_stable = float(
            model.predict_proba(features)[0][1]
        )

    # текстовая интерпретация коэффициентов
    interpretation = interpret_financial_state(features)

    return {
        "prediction": prediction,
        "probability_stable": probability_stable,
        "features": features.round(3),
        "interpretation": interpretation.iloc[0, 0]
    }


# ============================================================
# ТЕКСТОВОЕ ЗАКЛЮЧЕНИЕ
# ============================================================

def interpret_prediction(result: dict) -> str:
    """
    Формирование итогового текстового заключения
    по финансовой устойчивости предприятия.
    """

    status = (
        "ФИНАНСОВО УСТОЙЧИВОЕ"
        if result["prediction"] == 1
        else "ФИНАНСОВО НЕУСТОЙЧИВОЕ"
    )

    text = f"Результат оценки: предприятие {status}.\n"

    if result["probability_stable"] is not None:
        text += (
            f"Вероятность устойчивого состояния: "
            f"{result['probability_stable']:.2%}\n"
        )

    text += (
        "Анализ финансовых коэффициентов:\n"
        f"{result['interpretation']}"
    )

    return text


# ============================================================
# АВТОНОМНЫЙ ЗАПУСК (ТЕСТ)
# ============================================================

if __name__ == "__main__":
    test_input = {
        "year": 2023,
        "current_assets": 1_750_000,
        "current_liabilities": 780_000,
        "equity": 2_100_000,
        "total_assets": 3_600_000,
        "profit": 420_000
    }

    result = predict_stability(test_input)

    print("=== РЕЗУЛЬТАТ ПРОГНОЗА ===")
    print(interpret_prediction(result))
    print("\nИспользованные признаки:")
    print(result["features"])
