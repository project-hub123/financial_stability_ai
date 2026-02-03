"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение модуля:
Данный модуль реализует применение обученной модели
машинного обучения для оценки финансовой устойчивости предприятия.

Модуль используется:
– в графическом интерфейсе пользователя;
– при анализе отдельных финансовых периодов;
– при демонстрации результатов работы системы на защите ВКР.
"""

import os
import joblib
import pandas as pd
import numpy as np

from ml.features import (
    calculate_financial_ratios,
    interpret_financial_state
)


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def load_model(model_path: str):
    """
    Загрузка обученной ML-модели с диска.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Файл модели не найден: {model_path}"
        )

    model = joblib.load(model_path)
    return model


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

    df = pd.DataFrame([input_data])
    return df


# ============================================================
# ПРОГНОЗ ФИНАНСОВОЙ УСТОЙЧИВОСТИ
# ============================================================

def predict_stability(
    input_data: dict,
    model_path: str = "models/financial_stability_model.pkl"
) -> dict:
    """
    Прогноз финансовой устойчивости предприятия
    на основе введенных финансовых показателей.
    """

    # Загрузка модели
    model = load_model(model_path)

    # Подготовка входных данных
    raw_df = prepare_input_data(input_data)

    # Формирование признаков
    features = calculate_financial_ratios(raw_df)

    # Прогноз класса
    prediction = model.predict(features)[0]

    # Вероятность классов (если поддерживается моделью)
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(features)[0]
        probability_stable = probability[1]
    else:
        probability_stable = None

    # Текстовая интерпретация коэффициентов
    interpretation = interpret_financial_state(features)

    result = {
        "prediction": int(prediction),
        "probability_stable": probability_stable,
        "features": features.round(3),
        "interpretation": interpretation.iloc[0, 0]
    }

    return result


# ============================================================
# ТЕКСТОВАЯ ИНТЕРПРЕТАЦИЯ РЕЗУЛЬТАТА
# ============================================================

def interpret_prediction(result: dict) -> str:
    """
    Формирование итогового текстового заключения
    по финансовому состоянию предприятия.
    """

    if result["prediction"] == 1:
        status = "ФИНАНСОВО УСТОЙЧИВОЕ"
    else:
        status = "ФИНАНСОВО НЕУСТОЙЧИВОЕ"

    text = (
        f"Результат оценки: предприятие {status}.\n"
    )

    if result["probability_stable"] is not None:
        text += (
            f"Вероятность устойчивого состояния: "
            f"{result['probability_stable']:.2%}\n"
        )

    text += (
        "Анализ коэффициентов:\n"
        f"{result['interpretation']}"
    )

    return text


# ============================================================
# САМОСТОЯТЕЛЬНЫЙ ЗАПУСК МОДУЛЯ
# ============================================================

if __name__ == "__main__":
    """
    Пример автономного запуска модуля прогнозирования.
    Используется для тестирования и демонстрации работы.
    """

    test_input = {
        "year": 2023,
        "current_assets": 1750000,
        "current_liabilities": 780000,
        "equity": 2100000,
        "total_assets": 3600000,
        "profit": 420000
    }

    try:
        result = predict_stability(test_input)

        print("=== РЕЗУЛЬТАТ ПРОГНОЗА ===")
        print(interpret_prediction(result))
        print("\nИспользованные признаки:")
        print(result["features"])

    except Exception as e:
        print("Ошибка при выполнении прогноза:")
        print(str(e))
