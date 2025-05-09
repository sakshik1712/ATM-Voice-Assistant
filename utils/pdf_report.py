from fpdf import FPDF
import os

def generate_pdf_report(df, name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt=f"{name} - Monthly Transactions", ln=True, align="C")
    pdf.ln(10)

    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"Month: {row['Month']}, Amount: {row['Amount']}", ln=True)

    path = f"reports/{name.replace(' ', '_')}_transactions.pdf"
    pdf.output(path)
    return path
