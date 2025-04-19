from fpdf import FPDF
from bs4 import BeautifulSoup

# Function to sanitize Unicode text for FPDF (latin-1 only)
def sanitize_text(text):
    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "…": "...",
        "•": "*",
        "é": "e",
        "✓": "v",  # or leave out if needed
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# Function to create PDF from HTML content
def create_pdf_from_html(content, filename="output.pdf"):
    soup = BeautifulSoup(content, "html.parser")
    pdf = FPDF()
    pdf.add_page()

    def add_text_block(text, font="Times", style="", size=12, color=(0, 0, 0), spacing=5):
        text = sanitize_text(text.strip())
        pdf.set_text_color(*color)
        pdf.set_font(font, style, size)
        pdf.multi_cell(50, spacing, text)

    for tag in soup.find_all():
        if tag.name == "h1":
            add_text_block(tag.get_text(), style="B", size=16, color=(33, 33, 33), spacing=8)
        elif tag.name == "h2":
            add_text_block(tag.get_text(), style="B", size=14, color=(81, 45, 168), spacing=8)
        elif tag.name == "p":
            add_text_block(tag.get_text(), style="", size=12, spacing=6)
        elif tag.name == "strong":
            add_text_block(tag.get_text(), style="B", size=12)
        elif tag.name == "em":
            add_text_block(tag.get_text(), style="I", size=12)

    pdf.output(filename)

# Example usage
html_content = """
<h1>Welcome to My PDF</h1>
<h2>Introduction</h2>
<p>This is an example paragraph with curly quotes: “Hello World!” and smart apostrophes like this: It’s working!</p>
<p>Em dashes — and symbols like ✓ will be sanitized.</p>
"""

create_pdf_from_html(html_content, "clean_output.pdf")

