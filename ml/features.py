"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Тема ВКР:
«Интеллектуальный анализ финансовой устойчивости предприятия
и проблемы ее повышения
(на примере ООО „Научно-технический центр "АРМ-Регистр"»)»

Назначение модуля:
Данный модуль реализует полный набор функций для расчета
ключевых финансово-экономических показателей предприятия,
используемых при анализе финансовой устойчивости и обучении
моделей машинного обучения.

Модуль используется на этапах:
– предварительной обработки данных;
– формирования признакового пространства;
– обучения и применения ML-моделей;
– аналитической интерпретации результатов.
"""

import pandas as pd
import numpy as np


# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================

def _safe_divide(numerator, denominator):
    """
    Безопасное деление с защитой от деления на ноль.
    Возвращает 0, если знаменатель равен 0.
    """
    return np.where(denominator == 0, 0, numerator / denominator)


def _replace_infinite(df: pd.DataFrame) -> pd.DataFrame:
    """
    Замена бесконечных значений и NaN на 0
    для корректной работы ML-алгоритмов.
    """
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)
    return df


# ============================================================
# ОСНОВНЫЕ ФИНАНСОВЫЕ КОЭФФИЦИЕНТЫ
# ============================================================

def calculate_liquidity_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Расчет показателей ликвидности.
    """

    result = pd.DataFrame()

    # Коэффициент текущей ликвидности
    result["current_ratio"] = _safe_divide(
        df["current_assets"],
        df["current_liabilities"]
    )

    # Коэффициент быстрой ликвидности (упрощенный вариант)
    result["quick_ratio"] = _safe_divide(
        df["current_assets"] * 0.8,
        df["current_liabilities"]
    )

    # Коэффициент абсолютной ликвидности (условно)
    result["absolute_liquidity"] = _safe_divide(
        df["current_assets"] * 0.2,
        df["current_liabilities"]
    )

    return result


def calculate_financial_stability_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Расчет показателей финансовой устойчивости.
    """

    result = pd.DataFrame()

    # Коэффициент автономии
    result["equity_ratio"] = _safe_divide(
        df["equity"],
        df["total_assets"]
    )

    # Коэффициент финансовой зависимости
    result["financial_dependency"] = 1 - result["equity_ratio"]

    # Коэффициент маневренности капитала (упрощенный)
    result["maneuverability"] = _safe_divide(
        df["equity"] - (df["total_assets"] - df["current_assets"]),
        df["equity"]
    )

    return result


def calculate_profitability_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Расчет показателей рентабельности.
    """

    result = pd.DataFrame()

    # Рентабельность активов (ROA)
    result["return_on_assets"] = _safe_divide(
        df["profit"],
        df["total_assets"]
    )

    # Рентабельность собственного капитала (ROE)
    result["return_on_equity"] = _safe_divide(
        df["profit"],
        df["equity"]
    )

    # Маржинальность (условная)
    result["profit_margin"] = _safe_divide(
        df["profit"],
        df["current_assets"]
    )

    return result


# ============================================================
# АНАЛИЗ ДИНАМИКИ ПО ГОДАМ
# ============================================================

def calculate_growth_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Расчет темпов роста основных показателей по годам.
    Используется для анализа динамики развития предприятия.
    """

    result = pd.DataFrame()

    if "year" not in df.columns:
        return result

    df_sorted = df.sort_values("year")

    result["assets_growth"] = df_sorted["total_assets"].pct_change().fillna(0)
    result["equity_growth"] = df_sorted["equity"].pct_change().fillna(0)
    result["profit_growth"] = df_sorted["profit"].pct_change().fillna(0)

    return result


# ============================================================
# ИНТЕГРАЛЬНЫЕ ПОКАЗАТЕЛИ
# ============================================================

def calculate_integral_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Расчет интегрального показателя финансовой устойчивости.
    Используется как дополнительный аналитический признак.
    """

    result = pd.DataFrame()

    liquidity = _safe_divide(
        df["current_assets"],
        df["current_liabilities"]
    )

    autonomy = _safe_divide(
        df["equity"],
        df["total_assets"]
    )

    profitability = _safe_divide(
        df["profit"],
        df["total_assets"]
    )

    # Интегральный показатель (взвешенная сумма)
    result["integral_stability_score"] = (
        0.4 * liquidity +
        0.4 * autonomy +
        0.2 * profitability
    )

    return result


# ============================================================
# ФОРМИРОВАНИЕ ПОЛНОГО НАБОРА ПРИЗНАКОВ
# ============================================================

def calculate_financial_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """
    Формирование полного признакового пространства
    для моделей машинного обучения.
    """

    features = pd.DataFrame()

    liquidity = calculate_liquidity_ratios(df)
    stability = calculate_financial_stability_ratios(df)
    profitability = calculate_profitability_ratios(df)
    growth = calculate_growth_rates(df)
    integral = calculate_integral_score(df)

    features = pd.concat(
        [liquidity, stability, profitability, growth, integral],
        axis=1
    )

    features = _replace_infinite(features)

    return features


# ============================================================
# ИНТЕРПРЕТАЦИЯ ФИНАНСОВОГО СОСТОЯНИЯ
# ============================================================

def interpret_financial_state(features: pd.DataFrame) -> pd.DataFrame:
    """
    Формирование текстовой интерпретации финансового состояния
    предприятия на основе рассчитанных коэффициентов.
    """

    interpretation = []

    for _, row in features.iterrows():
        conclusions = []

        if row.get("current_ratio", 0) >= 2:
            conclusions.append("высокая ликвидность")
        elif row.get("current_ratio", 0) >= 1:
            conclusions.append("приемлемая ликвидность")
        else:
            conclusions.append("низкая ликвидность")

        if row.get("equity_ratio", 0) >= 0.5:
            conclusions.append("высокая финансовая автономия")
        else:
            conclusions.append("зависимость от заемных средств")

        if row.get("return_on_assets", 0) > 0:
            conclusions.append("прибыльная деятельность")
        else:
            conclusions.append("убыточная деятельность")

        interpretation.append("; ".join(conclusions))

    return pd.DataFrame({"analysis": interpretation})


# ============================================================
# ТЕСТОВЫЙ ЗАПУСК МОДУЛЯ
# ============================================================

if __name__ == "__main__":
    # Пример тестового запуска для проверки корректности расчетов

    test_data = pd.DataFrame({
        "year": [2021, 2022, 2023],
        "current_assets": [1000000, 1200000, 1400000],
        "current_liabilities": [900000, 950000, 980000],
        "equity": [1500000, 1700000, 2000000],
        "total_assets": [3000000, 3200000, 3500000],
        "profit": [100000, 200000, 300000]
    })

    features = calculate_financial_ratios(test_data)
    interpretation = interpret_financial_state(features)

    print(features)
    print(interpretation)
