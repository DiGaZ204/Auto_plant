from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import shutil
from pathlib import Path

router = APIRouter(prefix="/blog", tags=["blogs"])

# 設定上傳目錄
UPLOAD_DIR = Path("uploads/")
UPLOAD_DIR.mkdir(exist_ok=True)

# 文件上傳處理
@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return {"info": f"文件 '{file.filename}' 已保存至 '{file_location}'"}

# 定義sensor模型
class SensorDataModel(BaseModel):
    sensor_id: str
    time: Optional[str] = None  # 新增時間屬性
    temperature: Optional[float] = None
    moisture: Optional[float] = None
    cycle: Optional[int] = None

sensor_data = {}

# 更新sensor
@router.post("/sensors/update")
async def update_sensor_data(data: SensorDataModel):
    # 驗證濕度
    if data.moisture is not None and not 0 <= data.moisture <= 100:
        raise HTTPException(status_code=400, detail="濕度值必須在0到100之間")
    
    # 驗證溫度
    if data.temperature is not None and not -50 <= data.temperature <= 150:
        raise HTTPException(status_code=400, detail="溫度值必須在-50到150之間")
    
    # 更新數據
    sensor_data[data.sensor_id] = {
        "time": data.time,  # 新增時間屬性
        "temperature": data.temperature,
        "moisture": data.moisture,
        "cycle": data.cycle
    }
    
    return {
        "sensor_id": data.sensor_id,
        "data": sensor_data[data.sensor_id]
    }