import network
import time
from machine import Pin

led = Pin(2, Pin.OUT)

def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            time.sleep(1)
    print('Network config:', sta_if.ifconfig())


def toggle_led():
    led.value(not led.value())
    

def blink_led(count=2):
    for i in range(blink_led):
        toggle_led()
        time.sleep(1)

connect_wifi(os.environ['SSID'], os.environ['PASSWORD'])