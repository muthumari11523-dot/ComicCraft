from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.gemini_flash import generate_outline
from app.image_generator import generate_image
from app.exporters import save_pdf

router = APIRouter()

templates = Jinja2Templates(directory="templates")

# Store the latest generated comic
latest_comic = {
    "images": [],
    "panels": [],
    "character_name": ""
}


@router.post("/generate", response_class=HTMLResponse)
def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    # Generate story using Gemini
    comic_story = generate_outline(
        story_prompt,
        character_name,
        setting,
        tone,
        art_style
    )

    # Split story into 5 panels
    panels = []

    for i in range(1, 6):
        start_text = f"Panel {i}"
        start = comic_story.find(start_text)

        if i < 5:
            end_text = f"Panel {i + 1}"
            end = comic_story.find(end_text)
        else:
            end = len(comic_story)

        if start != -1:
            panel_text = comic_story[start:end].strip()
            panels.append(panel_text)

    if len(panels) == 0:
        panels = [comic_story]

    # Generate images
    image_files = []

    for i, panel in enumerate(panels, start=1):
        filename = f"panel_{i}.png"

        image_path = generate_image(
            panel,
            filename
        )

        image_files.append(image_path)

    # Save latest comic information
    latest_comic["images"] = image_files
    latest_comic["panels"] = panels
    latest_comic["character_name"] = character_name

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "request": request,
            "panels": panels,
            "images": image_files,
            "character_name": character_name
        }
    )


@router.get("/download-pdf")
def download_pdf():
    images = latest_comic["images"]
    panels = latest_comic["panels"]
    character_name = latest_comic["character_name"]

    pdf_path = save_pdf(
        images,
        panels,
        character_name
    )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="ComicCraft_Comic.pdf"
    )