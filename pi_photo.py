import cv2
import time
import os

# 設定參數
save_path = "/home/pi/API_code/uploads/"
interval = 2  # 每隔2秒拍一張照
duration = 8  # 總共拍照持續8秒
resolution = (1280, 720)  # 設定解析度為1280x720（HD）

# 確保保存路徑存在
os.makedirs(save_path, exist_ok=True)

# 初始化攝影機
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

j = 0
try:
    while True:
        start_time = time.time()
        for _ in range(duration // interval):
            ret, frame = cap.read()
            if ret:
                filename = f"{save_path}image_{j % 4}.jpg"
                cv2.imwrite(filename, frame)
                print(f"拍攝並儲存了 {filename}")
                j += 1
                time.sleep(interval)
            else:
                print("攝影機拍照失敗")
        
        # 等待到下一個小時開始
        time.sleep(3600 - (time.time() - start_time))
except KeyboardInterrupt:
    print("程序被用戶中斷")
finally:
    cap.release()
    print("攝影機資源已釋放")