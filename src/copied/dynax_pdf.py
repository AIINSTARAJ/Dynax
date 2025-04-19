
import os
from fpdf import FPDF

def set_pdf(doi: str, content: str):
    if not os.path.exists("PDF"):
        os.mkdir("PDF")

    filename = f"PDF/Dynax-{doi}.pdf"

    pdf = FPDF()
    pdf.add_page()

    # Set background color (light gray)
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(0, 0, 210, 297, 'F')  # A4 size in mm

    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filename)
    print(f"PDF saved: {filename}")

# Example usage
if __name__ == "__main__":
    example_doi = "10.2025/fpdf"
    example_content = (
        "Dynax PDF Report\n"
        "Generated with FPDF.\n"
        "Simple, clean, and light background.\n"
        "No styling stress."
    )
    set_pdf(example_doi, example_content)
