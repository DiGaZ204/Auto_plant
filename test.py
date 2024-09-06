import requests
import time

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
    FASTAPI_URL = "https://e554-1-169-79-88.ngrok-free.app"
    sensor_API = FASTAPI_URL + "/blog/sensors/update"

    sensor_id = input("請輸入傳感器ID: ")
    moisture = float(input("請輸入濕度值: "))
    temperature = float(input("請輸入溫度值: "))
    cycle = int(input("請輸入週期值: "))

    sensor_data = {
        "sensor_id": str(sensor_id),
        "moisture": moisture,
        "temperature": temperature,
        "cycle": cycle
    }

    post_data(sensor_API, sensor_data)

if __name__ == "__main__":
    while(True):
        send_custom_data()