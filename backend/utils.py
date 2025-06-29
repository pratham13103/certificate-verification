from fastapi import FastAPI
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

app = FastAPI()

# Coordinates stored in the backend
COORDINATES = {
    "internship_text": (200, 625),
    "generated_on": (160, 925),
    "cert_number": (1460, 1090),
    "name_y": 525  # Only Y-coordinate for name, X will be computed dynamically
}

@app.get("/text-coordinates")
def get_text_coordinates():
    return COORDINATES

# Function to wrap text within a given width
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        text_width = font.getbbox(test_line)[2]
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

def overlay_text_on_image(cert_number, name, course, start_date, end_date):
    template_path = "static/cert.jpeg"
    output_dir = "modified_certs"
    output_path = os.path.join(output_dir, f"{name.replace(' ', '_')}.jpeg")
    os.makedirs(output_dir, exist_ok=True)

    try:
        image = Image.open(template_path)
    except FileNotFoundError:
        raise ValueError(f"Template image not found at {template_path}")

    draw = ImageDraw.Draw(image)

    # Font paths
    times_font_path = "static/times.ttf"
    times_bold_font_path = "static/timesbd.ttf"  # Times New Roman Bold

    try:
        times_regular = ImageFont.truetype(times_font_path, 35)
        times_bold_large = ImageFont.truetype(times_bold_font_path, 80)
        times_bold_small = ImageFont.truetype(times_bold_font_path, 40)
        times_small = ImageFont.truetype(times_font_path, 30)
    except IOError:
        raise ValueError("Times New Roman font files not found. Please add 'times.ttf' and 'timesbd.ttf' to the static folder.")

    # Draw name centered between fixed range
    name_text = f"{name}"
    name_width = times_bold_large.getbbox(name_text)[2]
    center_start = 433
    center_end = 1290
    name_x = center_start + ((center_end - center_start - name_width) // 2)

    internship_text = (
        f"has completed an Internship at EduDiagno PVT. LTD. from "
        f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}. "
        "We found him sincere, hardworking, dedicated, and result-oriented. "
        "He worked well as part of the team during his tenure. "
        "We take this opportunity to thank him and wish him the best for the future."
    )
    wrapped_text = wrap_text(internship_text, times_regular, 1350)
    current_date_text = datetime.now().strftime('%Y-%m-%d')

    # Draw elements
    draw.text((name_x, COORDINATES["name_y"]), name_text, fill="black", font=times_bold_large)

    y_offset = COORDINATES["internship_text"][1]
    for line in wrapped_text:
        draw.text((COORDINATES["internship_text"][0], y_offset), line, fill="black", font=times_regular)
        y_offset += 40

    draw.text(COORDINATES["generated_on"], current_date_text, fill="black", font=times_bold_small)
    draw.text(COORDINATES["cert_number"], cert_number, fill="black", font=times_small)

    image.save(output_path)
    return output_path
