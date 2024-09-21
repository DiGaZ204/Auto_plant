import requests
import time
import random
from datetime import datetime

def post_data(url, data, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("數據發送成功:", data)
                response.close()
                return
            else:
                print(f"發送數據失敗。狀態碼: {response.status_code}")
                response.close()
        except Exception as e:
            print(f"連接失敗: {e}")
        time.sleep(1)  # 重試前等待一秒
    print(f"嘗試 {retries} 次後仍未能發送數據")

def send_custom_data():
    FASTAPI_URL = "https://7be0-1-169-86-126.ngrok-free.app"
    sensor_API = FASTAPI_URL + "/blog/sensors/update"

    sensor_id = input("請輸入傳感器ID: ")
    moisture = float(input("請輸入濕度值: "))
    temperature = float(input("請輸入溫度值: "))
    cycle = int(input("請輸入週期值: "))
    current_time = datetime.now().strftime("%H:%M")

    sensor_data = {
        "sensor_id": str(sensor_id),
        "time": current_time,
        "temperature": temperature,
        "moisture": moisture,
        "cycle": cycle
    }

    post_data(sensor_API, sensor_data)

def send_multiple_random_data(start_id, end_id, cycle):
    FASTAPI_URL = "https://7be0-1-169-86-126.ngrok-free.app"
    sensor_API = FASTAPI_URL + "/blog/sensors/update"

    for sensor_id in range(start_id, end_id + 1):
        moisture = round(random.uniform(0, 100), 2)
        temperature = round(random.uniform(26, 27), 2)
        current_time = datetime.now().strftime("%H:%M")

        sensor_data = {
            "sensor_id": str(sensor_id),
            "time": current_time,
            "temperature": temperature,
            "moisture": moisture,
            "cycle": cycle
        }

        post_data(sensor_API, sensor_data)
        print(f"已發送數據：ID={sensor_id}, 時間={current_time}, 溫度={temperature}, 濕度={moisture}, 週期={cycle}")
        time.sleep(1)  # 每次發送後等待1秒

    print(f"已成功發送 {end_id - start_id + 1} 筆數據")

if __name__ == "__main__":
    choice = input("選擇操作模式：1. 手動輸入單筆數據  2. 自動生成多筆數據 (輸入1或2): ")
    
    if choice == "1":
        while True:
            send_custom_data()
    elif choice == "2":
        #post id=3~20, cycle=1
        send_multiple_random_data(1, 20, 1)
    else:
        print("無效的選擇，程序結束。")