from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from layout_builder import build_comic_layout
from exporters import export_comic_to_pdf


app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )


@app.get("/comic")
def comic_preview(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "request": request,
            "comic": []
        }
    )


@app.post("/generate")
def generate_comic(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    story_panels = [
        {
            "panel": 1,
            "title": "Test Panel",
            "scene_description": story_prompt,
            "narration": f"{character_name} enters the {setting}.",
            "dialogue": f"{character_name}: This is a {tone} story!"
        }
    ]

    image_paths = [""]

    comic = build_comic_layout(
        story_panels,
        image_paths
    )

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "request": request,
            "comic": comic
        }
    )


@app.get("/export")
def export_pdf():
    output_path = "static/exports/comic.pdf"

    story_panels = [
        {
            "panel": 1,
            "title": "Test Panel",
            "scene_description": "A girl discovers a mysterious robot in her college.",
            "narration": "Maya enters the college and discovers something unusual.",
            "dialogue": "Maya: What is this robot doing here?"
        }
    ]

    image_paths = [""]

    comic_layout = build_comic_layout(
        story_panels,
        image_paths
    )

    export_comic_to_pdf(
        comic_layout,
        output_path
    )

    return {
        "message": "PDF exported successfully!"
    }
