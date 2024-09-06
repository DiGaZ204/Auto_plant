from fastapi import APIRouter, Query, Path, Body, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi import File, UploadFile
import shutil
from pathlib import Path

router = APIRouter(
    prefix="/blog",
    tags=["blogs"],
)

UPLOAD_DIR = Path("uploads/")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = UPLOAD_DIR / file.filename
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

class SensorDataModel(BaseModel):
    sensor_id: str
    moisture: Optional[float] = None
    temperature: Optional[float] = None
    cycle: Optional[int] = None

sensor_data = {}

@router.get("/sensors/all")
async def get_all_sensor_data():
    if not sensor_data:
        raise HTTPException(status_code=404, detail="No sensor data available.")
    
    return [{"sensor_id": sensor_id, **sensor_data[sensor_id]} for sensor_id in sensor_data]

@router.post("/sensors/update")
async def update_sensor_data(data: SensorDataModel):
    if data.moisture is not None and (data.moisture < 0 or data.moisture > 100):
        raise HTTPException(status_code=400, detail="Moisture value must be between 0 and 100.")
    
    if data.temperature is not None and (data.temperature < -50 or data.temperature > 150):
        raise HTTPException(status_code=400, detail="Temperature value must be between -50 and 150.")
    
    sensor_data[data.sensor_id] = {
        "moisture": data.moisture,
        "temperature": data.temperature,
        "cycle": data.cycle
    }
    return {"sensor_id": data.sensor_id, "data": sensor_data[data.sensor_id]}

@router.get("/sensors/{sensor_id}")
async def get_sensor_data(sensor_id: str):
    if sensor_id not in sensor_data:
        raise HTTPException(status_code=404, detail="Sensor ID not found.")
    
    return {"sensor_id": sensor_id, "data": sensor_data[sensor_id]}