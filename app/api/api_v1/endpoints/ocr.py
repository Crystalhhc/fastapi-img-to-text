from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Body, Request
from fastapi.responses import JSONResponse,FileResponse
from PIL import Image, UnidentifiedImageError
import pytesseract
import io
import base64
from typing import List
from pydantic import BaseModel

import pathlib
import uuid
from app.core.config import BASE_DIR, UPLOAD_DIR, get_settings, Settings

router = APIRouter()

class BBoxData(BaseModel):
    image: str    # Base64 encoded image data
    x: int
    y: int
    width: int
    height: int

@router.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)) -> BBoxData:
    contents = await file.read()
    
    try:
        img = Image.open(io.BytesIO(contents))
        #img = Image.open(contents)
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image file")

    # Convert the image to base64
    buffered = io.BytesIO()
    img.save(buffered, format=img.format)
    img_str = base64.b64encode(buffered.getvalue()).decode()

    # Rest of the function remains the same
    #encoded_string = base64.b64encode(contents).decode('utf-8')
    width, height = img.size
    # Declare payload as BBoxData
    payload = BBoxData(
        image=img_str,
        x=0,
        y=0,
        width=width,
        height=height
    )
    return payload


@router.post("/bbox-to-text/")
async def bbox_to_text(bbox_data: BBoxData = Body(...)):
    print(bbox_data.image)
    try:
        # Decode the base64 image
        image_data = base64.b64decode(bbox_data.image)
        #image_data = bbox_data.image 
        # convert image stringt to binary
        image = Image.open(io.BytesIO(image_data))
        # Crop the image based on bbox
        cropped_image = image.crop((bbox_data.x, bbox_data.y, 
                                    bbox_data.x + bbox_data.width, 
                                    bbox_data.y + bbox_data.height))

        # Perform OCR on the cropped image
        custome_config = r'--oem 3 --psm 6' # It is needed.
        texts = pytesseract.image_to_string(cropped_image, config=custome_config, lang='chi_tra')
        #text = pytesseract.image_to_string(cropped_image)

        # Split the text into lines and remove empty lines
        lines: List[str] = [line.strip() for line in texts.split('\n') if line.strip()]

        # Return the extracted text
        return JSONResponse(content={
            "status": "success",
            "full_text": texts,
            "lines": lines,
            "word_count": len(texts.split()),
            "char_count": len(texts),
            "bbox": {
                "x": bbox_data.x,
                "y": bbox_data.y,
                "width": bbox_data.width,
                "height": bbox_data.height
            }
        })
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid base64 image data: {str(ve)}")
    except pytesseract.TesseractNotFoundError:
        raise HTTPException(status_code=500, detail="Tesseract OCR is not installed or not found")
    except pytesseract.TesseractError as e:
        raise HTTPException(status_code=500, detail=f"Tesseract OCR error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
"""
Example of BBoxData
    {
        "image": "base64_encoded_image_data_here",
        "x": 100,
        "y": 200,
        "width": 300,
        "height": 150
    }
"""
@router.post("/img-echo/", response_class=FileResponse) # http POST
async def img_echo_view(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):
    print(f"settings.echo_view: {settings.echo_active}")
    if not settings.echo_active:
        raise HTTPException(detail="Invalid endpoint", status_code=400)
    UPLOAD_DIR.mkdir(exist_ok=True)
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)
    fname = pathlib.Path(file.filename)
    fext = fname.suffix # .jpg, .txt
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest