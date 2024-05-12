import network
import time
from machine import Pin

led = Pin(2, Pin.OUT)

def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        blink_led()
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            blink_led(1, 1)
    print('Network config:', sta_if.ifconfig())
    blink_led(5, 0.1) # Blink 5 times with 0.1 seconds interval


def toggle_led():
    led.value(not led.value())
    

def blink_led(count=1, blink_len=0.1):
    count *= 2 # Toggle on, toggle off
    for i in range(count):
        toggle_led()
        time.sleep(blink_len)

connect_wifi(os.environ['SSID'], os.environ['PASSWORD'])