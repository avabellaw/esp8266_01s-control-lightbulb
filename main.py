import network
import time
from machine import Pin

led = Pin(2, Pin.OUT)
button = Pin(2, Pin.IN, Pin.PULL_UP)

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
        
def listen_for_btn_click():
    while True:
        if button.value() == 0:
            blink_led(1, 0.3)
            while button.value() == 0:
                pass  # Wait for the button to be released
        time.sleep(0.1)  # So it doesn't accidentally trigger multiple times

connect_wifi(os.environ['SSID'], os.environ['PASSWORD'])


