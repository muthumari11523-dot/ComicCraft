from fpdf import FPDF
import os


def save_pdf(images, panels, character_name):
    os.makedirs("exports", exist_ok=True)

    pdf_path = "exports/comiccraft_comic.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title page
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 15, "COMICCRAFT", ln=True, align="C")

    pdf.set_font("Helvetica", "", 16)
    pdf.cell(0, 12, "AI Comic Story Creator", ln=True, align="C")

    pdf.ln(10)

    pdf.set_font("Helvetica", "", 14)
    pdf.cell(
        0,
        10,
        f"Character: {character_name}",
        ln=True,
        align="C"
    )

    # Add every comic panel
    for i, image_path in enumerate(images):

        pdf.add_page()

        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(
            0,
            12,
            f"Panel {i + 1}",
            ln=True,
            align="C"
        )

        pdf.ln(5)

        # Convert web path to real file path
        real_image_path = image_path.lstrip("/")

        if os.path.exists(real_image_path):
            pdf.image(
                real_image_path,
                x=15,
                y=35,
                w=180
            )

        pdf.ln(115)

        pdf.set_font("Helvetica", "", 11)

        text = panels[i]

        # Make text compatible with PDF font
        text = text.encode(
            "latin-1",
            "replace"
        ).decode("latin-1")

        pdf.multi_cell(
            0,
            7,
            text
        )

    pdf.output(pdf_path)

    return pdf_path