import network
import time
from machine import Pin
import usocket
import config

led = Pin(2, Pin.OUT)
button = Pin(2, Pin.IN, Pin.PULL_UP)


def toggle_led():
    led.value(not led.value())


def blink_led(count=1, blink_len=0.1):
    count *= 2  # Toggle on, toggle off
    for i in range(count):
        toggle_led()
        time.sleep(blink_len)


def connect_wifi(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        blink_led()
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            blink_led(1, 1)
    print('Network config:', sta_if.ifconfig())
    blink_led(3, 1)  # Blink 5 times with 0.1 seconds interval


def listen_for_btn_click():
    while True:
        if button.value() == 0:
            print('Button pressed')
            send_message('Button pressed')
            blink_led(1, 0.3)
            while button.value() == 0:
                pass  # Wait for the button to be released
        time.sleep(0.1)  # So it doesn't accidentally trigger multiple times


def send_message(message):
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    server_address = (config.SERVER_IP, config.SERVER_PORT)
    sock.connect(server_address)
    try:
        sock.send(message)
    finally:
        sock.close()


print('Connecting to WiFi...')
connect_wifi(config.SSID, config.PASSWORD)

listen_for_btn_click()
