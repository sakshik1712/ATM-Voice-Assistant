# email_utils.py

import smtplib
from email.message import EmailMessage
from fpdf import FPDF
import os
from email_utils import generate_pdf_report, send_email_with_pdf


def generate_pdf_report(username, df, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=f"{username}'s ATM Transaction Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)

    pdf.ln(10)
    for index, row in df.iterrows():
        line = f"{row['Date']} - {row['Type']} - ₹{row['Amount']} - Balance: ₹{row['Balance']}"
        pdf.cell(200, 10, txt=line, ln=True, align='L')

    pdf.output(filename)
    return filename

def send_email_with_pdf(receiver_email, subject, body, pdf_filename):
    sender_email = "your-email@gmail.com"
    sender_password = "your-app-password"  # Use App Password if using Gmail with 2FA

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(body)

    with open(pdf_filename, "rb") as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_filename)
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
