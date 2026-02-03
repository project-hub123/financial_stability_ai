"""
ФИО автора: Кирченков Александр Николаевич
Руководитель ВКР: Коротков Дмитрий Павлович

Назначение:
Генерация расширенного датасета (500 записей)
с шумом и пограничными финансовыми состояниями
для обучения моделей ВКР.
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)

ROWS = 500
YEARS = np.random.randint(2012, 2026, size=ROWS)

data = []

for year in YEARS:
    # базовые активы
    total_assets = np.random.normal(3_000_000, 900_000)
    total_assets = max(total_assets, 800_000)

    equity_ratio = np.random.uniform(0.25, 0.75)
    equity = total_assets * equity_ratio

    current_assets = total_assets * np.random.uniform(0.35, 0.65)
    current_liabilities = current_assets * np.random.uniform(0.6, 1.3)

    # прибыль с шумом
    profit = np.random.normal(
        loc=total_assets * 0.05,
        scale=total_assets * 0.08
    )

    # логика метки + шум
    score = (
        0.4 * (current_assets / (current_liabilities + 1)) +
        0.4 * (equity / total_assets) +
        0.2 * (profit / total_assets)
    )

    score += np.random.normal(0, 0.15)  # ШУМ

    label = 1 if score > 0.9 else 0

    data.append([
        year,
        int(current_assets),
        int(current_liabilities),
        int(equity),
        int(total_assets),
        int(profit),
        label
    ])

df = pd.DataFrame(
    data,
    columns=[
        "year",
        "current_assets",
        "current_liabilities",
        "equity",
        "total_assets",
        "profit",
        "label"
    ]
)

# путь сохранения
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "financial_data.csv")

os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
df.to_csv(DATA_PATH, index=False)

print("Датасет создан:")
print(DATA_PATH)
print(df["label"].value_counts())
