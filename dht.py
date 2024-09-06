from machine import Pin, ADC
import time
import xtools, utime
import urequests
import dht
import machine
from time import sleep

xtools.connect_wifi_led()
WRITE_API_KEY = "8GF45PHQ1K0H7GLJ"

#trail's pin
IN1 = Pin(4, Pin.OUT)
IN2 = Pin(32, Pin.OUT)
IN3 = Pin(33, Pin.OUT)
IN4 = Pin(25, Pin.OUT)
#esp32's pin
RELAY_PIN = 14
analogPin = 34
temp = dht.DHT11(machine.Pin(2))
#Init ADC
adc = ADC(Pin(analogPin))
adc.atten(ADC.ATTN_11DB)
#relay's pin
relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(0)

def step_motor(step):
    if step == 0:
        IN1.on()
        IN2.off()
        IN3.off()
        IN4.off()
    elif step == 1:
        IN1.off()
        IN2.on()
        IN3.off()
        IN4.off()
    elif step == 2:
        IN1.off()
        IN2.off()
        IN3.on()
        IN4.off()
    elif step == 3:
        IN1.off()
        IN2.off()
        IN3.off()
        IN4.on()


def rotate_motor(steps, delay=0.01):
    
    for i in range(steps):
        step_motor(3 - i % 4)
        sleep(delay)
    
    for i in range(steps):
        step_motor(i % 4)
        sleep(delay)

def read_soil_moisture():
    moisture_value = adc.read()
    moisture_percent = (moisture_value / 4095.0) * 100
    return float(moisture_percent)

def post_data(url, data, retries=10):
    for attempt in range(retries):
        try:
            response = urequests.post(url, json=data)
            if response.status_code == 200:
                print(data)
                response.close()
                return
            else:
                print(f"Failed to post data. Status code: {response.status_code}")
                response.close()
        except OSError as e:
            print(f"Failed to connect: {e}")
        time.sleep(1)  # wait a bit before retrying
    
    print(f"Failed to post data after {retries} attempts")
    
sensor_1 = 0
flag_rotate_motor = 0
relay_on = False
relay_start_time = 0
next_check_time = 0
cycle = 0
while True:
    #trail_run
    flag_rotate_motor = flag_rotate_motor % 10
    if not flag_rotate_motor:
        rotate_motor(300)#100 = 1sec, limit = 7600
    flag_rotate_motor += 1
    #get_data
    temp.measure()
    temperature = round(float(temp.temperature()), 1)
    moisture = round(float(read_soil_moisture()), 1)
    print("temperature:", temperature, "C, ", "soil_moi:", moisture, "%")
    #relay
    current_time = utime.time()
    if moisture < 30 and not relay_on and current_time >= next_check_time:
        print("relay On!!!")
        relay_on = True
        relay.value(1)
        relay_start_time = current_time
    if relay_on and current_time - relay_start_time >= 4:
        relay.value(0)
        relay_on = False
        next_check_time = current_time + 600
    #json_trans
    sensor_1 = sensor_1 % 60 + 1
    if sensor_1 == 1:
        cycle = cycle % 3 + 1
    sensor_data = {
        "sensor_id": str(sensor_1),
        "moisture": moisture,
        "temperature": temperature,
        "cycle": cycle
    }
    #ngrok
    FASTAPI_URL = "https://bdb3-140-121-16-77.ngrok-free.app"
    #API
    sensor_API = FASTAPI_URL + "/blog/sensors/update"
    post_data(sensor_API, sensor_data)
    print("\n")
    #line notify
#     url = "http://api.thingspeak.com/update?"
#     url += "api_key=" + WRITE_API_KEY
#     url += "&field1=" + str(moisture)
#     xtools.webhook_get(url)