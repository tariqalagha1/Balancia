import io

from fastapi.responses import HTMLResponse, StreamingResponse
from openpyxl import Workbook
from weasyprint import HTML


def generate_pdf(html_content: str, filename: str):
    """Generate PDF from HTML content with Arabic support"""
    pdf = HTML(string=html_content).write_pdf()
    return StreamingResponse(
        io.BytesIO(pdf),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


def generate_excel(data: list, headers: list, filename: str):
    """Generate Excel file from data"""
    wb = Workbook()
    ws = wb.active
    ws.append(headers)

    for row in data:
        ws.append(row)

    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)

    return StreamingResponse(
        excel_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


def generate_print_html(template: str, context: dict):
    """Generate print-optimized HTML view"""
    # In practice, we would use Jinja2 to render templates
    # For now, return raw HTML string
    return HTMLResponse(content=template % context, media_type="text/html")
