import requests
import os
from fpdf import FPDF
import fitz

def set_pdf(content: str,doi: str):
    
    try:
        doi = doi.replace('DOI - arXiv:','')
        
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

    except Exception as E:

        msg = f"Unicode error occurred: {str(E)}. Please check the content for unsupported characters."
        
        return msg

def get_content(link):
    
    link = link.replace("DOI - ","").replace('pdf','html')

    response = requests.get(link)

    content = response.text

    return content


if __name__ == '__main__':
    analysis = get_content("https://arxiv.org/pdf/2504.07109")
    print(analysis)  