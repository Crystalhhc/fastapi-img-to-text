from fastapi import(
    APIRouter,
    Header,
    HTTPException,
    Depends,
    Request,
    File,
    UploadFile
    )
from  .config import Settings, get_settings
def validate_file(file: UploadFile, settings:Settings = Depends(get_settings)):
    if file.content_type not in settings.allowed_file_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    if file.size > settings.max_file_size:
        raise HTTPException(status_code=400, detail="File too large")