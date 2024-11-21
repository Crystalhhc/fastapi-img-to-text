from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.api_v1.api import router as api_router
from app.core.config import BASE_DIR, UPLOAD_DIR, get_settings, Settings

app = FastAPI(
    title="Tesseract OCR API",
    description="API for performing OCR using Tesseract",
    version="1.0.0",
)

app.include_router(api_router, prefix="")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse) # http GET -> JSON
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request, "abc": 123})
   
