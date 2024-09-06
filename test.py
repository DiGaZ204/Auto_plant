import requests
import time

def post_data(url, data, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("数据发送成功:", data)
                response.close()
                return
            else:
                print(f"发送数据失败。状态码: {response.status_code}")
                response.close()
        except Exception as e:
            print(f"连接失败: {e}")
        time.sleep(1)  # 重试前等待一秒
    print(f"尝试 {retries} 次后仍未能发送数据")

def send_custom_data():
    FASTAPI_URL = "https://e554-1-169-79-88.ngrok-free.app"
    sensor_API = FASTAPI_URL + "/blog/sensors/update"

    sensor_id = input("请输入传感器ID: ")
    moisture = float(input("请输入湿度值: "))
    temperature = float(input("请输入温度值: "))
    cycle = int(input("请输入周期值: "))

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