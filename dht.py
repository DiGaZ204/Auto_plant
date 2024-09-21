from machine import Pin, ADC
import time
import xtools, utime
import urequests
import dht
import machine
from time import sleep

# Constants
MOISTURE_THRESHOLD = 30
RELAY_ON_TIME = 4
RELAY_CHECK_INTERVAL = 600
MOTOR_ROTATION_INTERVAL = 10
MOTOR_ROTATION_STEPS = 300

xtools.connect_wifi_led()
# WRITE_API_KEY = "8GF45PHQ1K0H7GLJ"

# Pin setup
IN1 = Pin(4, Pin.OUT)
IN2 = Pin(32, Pin.OUT)
IN3 = Pin(33, Pin.OUT)
IN4 = Pin(25, Pin.OUT)
RELAY_PIN = 14
analogPin = 34
temp = dht.DHT11(Pin(2))

# Initialize ADC
adc = ADC(Pin(analogPin))
adc.atten(ADC.ATTN_11DB)

# Relay setup
relay = Pin(RELAY_PIN, Pin.OUT)
relay.value(0)

def step_motor(step):
    pins = [IN1, IN2, IN3, IN4]
    for i, pin in enumerate(pins):
        pin.value(i == step)

def rotate_motor(steps, delay=0.01):
    for i in range(steps):
        step_motor(3 - i % 4)
        sleep(delay)
    for i in range(steps):
        step_motor(i % 4)
        sleep(delay)

def read_soil_moisture():
    try:
        moisture_value = adc.read()
        moisture_percent = (moisture_value / 4095.0) * 100
        return round(moisture_percent, 1)
    except Exception as e:
        print("Error reading soil moisture:", e)
        return None

def measure_temperature():
    try:
        temp.measure()
        return round(temp.temperature(), 1)
    except Exception as e:
        print("Error reading temperature:", e)
        return None

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

def send_data(temperature, moisture, sensor_id, cycle):
    current_time = utime.localtime()
    formatted_time = f"{current_time[3]:02d}:{current_time[4]:02d}"
    sensor_data = {
        "sensor_id": str(sensor_id),
        "time": formatted_time,
        "temperature": temperature,
        "moisture": moisture,
        "cycle": cycle
    }
    sensor_API = FASTAPI_URL + "/blog/sensors/update"
    post_data(sensor_API, sensor_data)

sensor_1 = 0
flag_rotate_motor = 0
relay_on = False
relay_start_time = 0
next_check_time = 0
cycle = 0

FASTAPI_URL = "https://bdb3-140-121-16-77.ngrok-free.app"

while True:
    # Motor rotation
    flag_rotate_motor = (flag_rotate_motor + 1) % MOTOR_ROTATION_INTERVAL
    if flag_rotate_motor == 0:
        rotate_motor(MOTOR_ROTATION_STEPS)

    # Get data
    temperature = measure_temperature()
    moisture = read_soil_moisture()

    if temperature is not None and moisture is not None:
        print("Temperature:", temperature, "C, Soil Moisture:", moisture, "%")

        # Relay control
        current_time = time.time()
        if moisture < MOISTURE_THRESHOLD and not relay_on and current_time >= next_check_time:
            print("Relay On!")
            relay_on = True
            relay.value(1)
            relay_start_time = current_time
        if relay_on and current_time - relay_start_time >= RELAY_ON_TIME:
            relay.value(0)
            relay_on = False
            next_check_time = current_time + RELAY_CHECK_INTERVAL

        # Data processing
        sensor_1 = sensor_1 % 60 + 1
        if sensor_1 == 1:
            cycle = cycle % 3 + 1

        # Send data
        send_data(temperature, moisture, sensor_1, cycle)

    print()
    time.sleep(1)

    # Line Notify (commented out)
    # url = "http://api.thingspeak.com/update?"
    # url += "api_key=" + WRITE_API_KEY
    # url += "&field1=" + str(moisture)
    # xtools.webhook_get(url)