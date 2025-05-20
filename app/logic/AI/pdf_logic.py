import requests
import os
import pdfkit

def set_pdf(content: str,doi: str):
    
    try:
        doi = doi.replace('DOI - arXiv:','')
        
        if not os.path.exists("PDF"):
            os.mkdir("PDF")

        filename = os.path.join(r'C:\Users\USER\OneDrive\Documents\Advanced Projects\Dynax\PDF', f'Dynax-{doi}.pdf')

        path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

        options = {'page-size': 'A4', 'encoding': 'UTF-8'}
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

        pdfkit.from_string(content, filename, configuration=config,options=options)

    except Exception as E:
        
        return 'Error'

def get_content(link:str):

    link = link.replace("DOI - ","").replace('pdf','html')

    response = requests.get(link)

    content = response.text

    return content


if __name__ == '__main__':
    analysis = get_content("https://arxiv.org/pdf/2504.07109")
    print(analysis)  