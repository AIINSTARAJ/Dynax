
import os
from fpdf import FPDF

def set_pdf(content: str,doi: str):
    
    if not os.path.exists("PDF"):
        os.mkdir("PDF")

    filename = f"PDF/Dynax-{doi}.pdf"

    pdf = FPDF()
    pdf.add_page()

    pdf.set_fill_color(240, 240, 240)
    pdf.rect(0, 0, 210, 297, 'F')

    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filename)
