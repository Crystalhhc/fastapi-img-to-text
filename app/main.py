import pathlib
import os
import io
import uuid

from fastapi import(
        FastAPI, 
        Request,
        Depends,
        File,
        UploadFile,
        )  
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

class Settings(BaseSettings):
    debug: bool = False
    echo_active: bool = False
    class config:
        

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / 'uploaded'

print(BASE_DIR / 'templates')
app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get('/', response_class=HTMLResponse)
async def home_view(request: Request):
    return templates.TemplateResponse({"request": request, "abc": 123}, "home.html", )

@app.post('/')
async def home_detail_view():
    return {"hello": "world"}

@app.post('/img-echo/', response_class=FileResponse)
async def img_echo_view(file: UploadFile = File(...)):
    bytes_str = io.BytesIO(await file.read())
    fname = pathlib.Path(file.filename)
    fext = fname.suffix
    
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    with open(str(dest), 'wb') as out:
        out.write(bytes_str.read())
        
    return dest

