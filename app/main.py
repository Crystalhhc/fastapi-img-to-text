import pathlib
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent
print(BASE_DIR / 'templates')
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get('/', response_class=HTMLResponse)
async def home_view(request: Request):
    return templates.TemplateResponse({"request": request, "abc": 123}, "home.html", )

@app.post('/')
async def home_detail_view():
    return {"hello": "world"}


