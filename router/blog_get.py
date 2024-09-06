from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

# 導入sensor數據
from .blog_post import sensor_data

router = APIRouter(prefix="/blog", tags=["blogs"])

# 設定上傳目錄
UPLOAD_DIR = Path("uploads/")

# 文件下載處理
@router.get("/download/{file_name}")
async def download_file(file_name: str):
    file_location = UPLOAD_DIR / file_name
    if file_location.exists():
        return FileResponse(
            path=file_location,
            media_type='application/octet-stream',
            filename=file_name
        )
    return {"error": "文件未找到"}

# 獲取所有sensor數據
@router.get("/sensors/all")
async def get_all_sensor_data():
    if not sensor_data:
        raise HTTPException(status_code=404, detail="沒有可用的sensor數據")
    
    return [
        {"sensor_id": sensor_id, **sensor_data[sensor_id]}
        for sensor_id in sensor_data
    ]

# 獲取特定sensor數據
@router.get("/sensors/{sensor_id}")
async def get_sensor_data(sensor_id: str):
    if sensor_id not in sensor_data:
        raise HTTPException(status_code=404, detail="未找到指定的sensor_ID")
    
    return {
        "sensor_id": sensor_id,
        "data": sensor_data[sensor_id]
    }