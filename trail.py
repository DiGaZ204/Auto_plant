from machine import Pin
from time import sleep


IN1 = Pin(4, Pin.OUT)
IN2 = Pin(32, Pin.OUT)
IN3 = Pin(33, Pin.OUT)
IN4 = Pin(25, Pin.OUT)


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
        
#     sleep(2)
    
#     for i in range(steps):
#         step_motor(i % 4)
#         sleep(delay)

rotate_motor(1024)

