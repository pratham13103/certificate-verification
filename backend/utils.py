from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

app = FastAPI()

# Coordinates stored in the backend
COORDINATES = {
    "name": (700, 525),
    "internship_text": (400, 625),  # Below the name, left-aligned
    "start_date": (75, 925),  # Position for the date
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

        # Get text width using font.getbbox()
        text_width = font.getbbox(test_line)[2]  

        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)  # Add the last line
    return lines

def overlay_text_on_image(name, course, start_date, end_date):
    template_path = "static/cert.jpeg"
    output_dir = "modified_certs"
    output_path = os.path.join(output_dir, f"{name.replace(' ', '_')}.jpeg")

    os.makedirs(output_dir, exist_ok=True)

    try:
        image = Image.open(template_path)
    except FileNotFoundError:
        raise ValueError(f"Template image not found at {template_path}")

    draw = ImageDraw.Draw(image)

    bold_font_path = "static/AGENCYB.TTF"
    regular_font_path = "static/AGENCYR.TTF"

    try:
        bold_font_large = ImageFont.truetype(bold_font_path, 80)  
        regular_font_small = ImageFont.truetype(regular_font_path, 35)  # Regular (non-bold) font for internship text
        bold_font_small = ImageFont.truetype(bold_font_path, 40)  
        font_small = ImageFont.truetype(regular_font_path, 30)  
    except IOError:
        raise ValueError("Font file not found. Ensure both AGENCYB.TTF and AGENCYR.TTF exist in static folder.")

    name_text = f"{name}"

    internship_text = (
        f"has completed an Internship at EduDiagno PVT. LTD. from "
        f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}. "
        "We found him sincere, hardworking, dedicated, and result-oriented. "
        "He worked well as part of the team during his tenure. "
        "We take this opportunity to thank him and wish him the best for the future."
    )

    wrapped_text = wrap_text(internship_text, regular_font_small, 800)  # Adjust width as needed for left alignment

    date_text = f"{end_date.strftime('%Y-%m-%d')}"  

    draw.text(COORDINATES["name"], name_text, fill="red", font=bold_font_large)

    # Draw the internship text with left alignment
    y_offset = COORDINATES["internship_text"][1]
    for line in wrapped_text:
        draw.text((COORDINATES["internship_text"][0], y_offset), line, fill="black", font=regular_font_small)
        y_offset += 40  # Adjust line spacing

    draw.text(COORDINATES["start_date"], date_text, fill="black", font=bold_font_small)

    image.save(output_path)
    return output_path
