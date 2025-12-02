from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
import os
import re
from django.utils.html import strip_tags

# Styles
styles = getSampleStyleSheet()
title_style = styles["Title"]
header_style = styles["Heading2"]
normal_style = styles["BodyText"]

def clean_html_for_pdf(html_content):
    """Remove unsupported HTML for ReportLab Paragraph."""
    if not html_content:
        return "Not provided."
    html_content = re.sub(r'\s*title="[^"]*"', '', html_content) 
    return strip_tags(html_content).replace('&nbsp;', ' ')

def parse_history_sections(html_content):
    """Parse the car_history_report HTML content into sections."""
    sections = {
        "Accident History": "Not provided.",
        "Service History": "Not provided.",
        "Ownership History": "Not provided.",
        "Mileage Verification": "Not provided.",
        "Mechanical Notes / Issues": "Not provided.",
        "Recommendations": "Not provided.",
    }

    if not html_content:
        return sections

    text = clean_html_for_pdf(html_content)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    current_section = None
    for line in lines:
        match = re.match(r'\[(.+?)\]', line)
        if match:
            current_section = match.group(1)
            if current_section not in sections:
                sections[current_section] = ""
        elif current_section:
            if sections[current_section] != "Not provided.":
                sections[current_section] += " " + line
            else:
                sections[current_section] = line

    return sections

def add_watermark(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 50)
    canvas.setFillColorRGB(0.9, 0.9, 0.9)
    canvas.translate(300, 400)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, "AUTO MARKET")
    canvas.restoreState()
def generate_car_report(car):
    buffer = BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    elements = []

    # Logo
    logo_path = os.path.join(settings.BASE_DIR, "static/img/logos/logo.png")
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=120, height=50)
        logo.hAlign = "RIGHT"
        elements.append(logo)

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Car History Report — {car.car_title}", title_style))
    elements.append(Spacer(1, 12))

    # Car Main Data
    car_table_data = [
        ["Field", "Value"],
        ["Title", car.car_title],
        ["Model", car.model],
        ["City", car.city],
        ["Year", car.year],
        ["Color", car.color],
        ["Price", f"{car.price:,} €"],
        ["Mileage History", f"{car.kilometers:,} km"],
        ["Transmission", car.transmission],
        ["Fuel Type", car.fuel_type],
        ["Engine", car.engine],
        ["Body Style", car.body_style],
        ["Owners", car.no_of_owners],
        ["VIN", car.vin_no],
    ]

    table = Table(car_table_data, colWidths=[6*cm, 9*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#333333")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#f7f7f7")),
        ("BOX", (0,0), (-1,-1), 1, colors.black),
        ("GRID", (0,0), (-1,-1), 0.3, colors.gray),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # History Sections
    sections = parse_history_sections(car.car_history_report)
    for title in ["Accident History", "Service History", "Ownership History",
                  "Mileage Verification", "Mechanical Notes / Issues", "Recommendations"]:
        elements.append(Paragraph(title, header_style))
        elements.append(Paragraph(sections.get(title, "Not provided."), normal_style))
        elements.append(Spacer(1, 12))


    # Photos
    elements.append(Paragraph("Photos", header_style))
    img_fields = [car.car_photo, car.car_photo_1, car.car_photo_2, car.car_photo_3, car.car_photo_4]
    for img in img_fields:
        if img:
            try:
                pic = Image(img.path, width=12*cm, height=7*cm)
                elements.append(pic)
                elements.append(Spacer(1, 12))
            except:
                continue

    # Build PDF
    pdf.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)

    buffer.seek(0)

    # Create filename from car title (remove problematic characters)
    safe_title = re.sub(r'[^\w\s-]', '', car.car_title).strip().replace(' ', '_')
    filename = f"{safe_title}_Report.pdf"

    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response