import cv2
import time

# 設定參數
save_path = "/home/pi/API_code/uploads/"
interval = 2  # 每隔5秒拍一張照
duration = 8  # 總共拍照持續（25秒）
resolution = (1280, 720)  # 設定解析度為1280x720（HD）

# 初始化攝影機
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

# 計算需要拍照的次數
num_photos = duration // interval
j = 0
# 開始拍照
# 
while(True):
    for i in range(num_photos):
        ret, frame = cap.read()
        if ret:
    #         timestamp = time.strftime("%Y%m%d_%H%M%S")
    #         filename = f"{save_path}image_{timestamp}.jpg"
            filename = f"{save_path}image_{j % 4}.jpg"
            j += 1
            cv2.imwrite(filename, frame)
            print(f"拍攝並儲存了 {filename}")
        else:
            print("攝影機拍照失敗")
    # 釋放攝影機資源
#     cap.release()
    time.sleep(3600)

