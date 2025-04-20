import requests
import os
import pdfkit

def set_pdf(content: str,doi: str):
    
    try:
        doi = doi.replace('DOI - arXiv:','')
        
        if not os.path.exists("PDF"):
            os.mkdir("PDF")

        filename = os.path.join('PDF', 'Dynax-{doi}.pdf')

        pdfkit.from_string(content,filename)

    except Exception as E:
        
        return 'Error'

def get_content(link):
    
    link = link.replace("DOI - ","").replace('pdf','html')

    response = requests.get(link)

    content = response.text

    return content


if __name__ == '__main__':
    analysis = get_content("https://arxiv.org/pdf/2504.07109")
    print(analysis)  