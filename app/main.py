from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.api.api_v1.api import router as api_router

app = FastAPI(
    title="Tesseract OCR API",
    description="API for performing OCR using Tesseract",
    version="1.0.0",
)

app.include_router(api_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
