from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.config import BASE_DIR
from app.api.api_v1.endpoints import ocr

#templates = Jinja2Templates(directory="templates")
router = APIRouter()
router.include_router(ocr.router, prefix='/ocr', tags=['OCR'])

"""
@router.get("/", response_class=HTMLResponse) # http GET -> JSON


def home_view(request: Request):
    templates = Jinja2Templates(directory="./templates")
    return templates.TemplateResponse("home.html", {"request": request, "abc": 123})
"""