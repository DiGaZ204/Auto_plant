from fastapi import APIRouter, Query, Path, Body, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import status, Response
from enum import Enum
router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
)
UPLOAD_DIR = Path("uploads/")
@router.get("/download/{file_name}")
async def download_file(file_name: str):
    file_location = UPLOAD_DIR / file_name
    if file_location.exists():
        return FileResponse(path=file_location, media_type='application/octet-stream', filename=file_name)
    return {"error": "File not found"}
