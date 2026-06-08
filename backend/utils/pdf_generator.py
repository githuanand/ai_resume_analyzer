from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(
    filename,
    analysis_text
):

    pdf_file = f"reports/{filename}.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = [
        Paragraph(
            "AI Resume Analysis Report",
            styles["Title"]
        ),
        Paragraph(
            analysis_text.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    ]

    doc.build(content)

    return pdf_file