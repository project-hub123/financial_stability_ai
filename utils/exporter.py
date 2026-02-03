"""
Экспорт отчётов в PDF и Excel
"""

import pandas as pd
from fpdf import FPDF


def export_to_excel(df: pd.DataFrame, path="reports/report.xlsx"):
    df.to_excel(path, index=False)


def export_to_pdf(text: str, path="reports/report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf.output(path)
