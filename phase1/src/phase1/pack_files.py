from __future__ import annotations

from io import BytesIO


def _latin(text: str) -> str:
    return (
        (text or "")
        .replace("—", "-")
        .replace("–", "-")
        .replace("·", "-")
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def markdown_to_docx(text: str) -> bytes:
    from docx import Document

    doc = Document()
    for line in text.splitlines():
        doc.add_paragraph(line)
    buf = BytesIO()
    doc.save(buf)
    return buf.getvalue()


def markdown_to_pdf(text: str) -> bytes:
    from fpdf import FPDF

    pdf = FPDF(format="A4", unit="mm")
    pdf.set_margins(18, 16, 18)
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()
    lines = (text or "").splitlines()
    if lines:
        pdf.set_font("Helvetica", "B", 16)
        pdf.multi_cell(0, 8, _latin(lines[0]))
        pdf.ln(1)
        body = lines[1:]
    else:
        body = []
    for raw in body:
        line = raw.rstrip()
        if not line:
            pdf.ln(2)
            continue
        pdf.set_x(pdf.l_margin)
        if line.isupper() and len(line) < 48 and not line.startswith("-"):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 7, _latin(line))
            continue
        pdf.set_font("Helvetica", "", 10)
        body = ("- " + line[2:]) if line.startswith("- ") else line
        try:
            pdf.multi_cell(0, 5, _latin(body))
        except Exception:
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(0, 5, _latin(body[:90]))
    out = pdf.output()
    return bytes(out) if not isinstance(out, (bytes, bytearray)) else bytes(out)
