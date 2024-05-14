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
    print('Connecting to WiFi...')
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        blink_led()
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            blink_led(1, 1)
    print(f'Connected to WiFi: {ssid}\n\
            Network config: {sta_if.ifconfig()}')
    blink_led(3, 1)  # Blink 3 times with 1 second interval


def listen_for_btn_click(socket):
    while True:
        try:
            data = socket.recv(1)
        except OSError:
            pass
        else:
            socket.send(data)

        if button.value() == 0:
            send_message(socket, config.BUTTON_CLICK)
            blink_led(1, 0.3)
            while button.value() == 0:
                pass  # Wait for the button to be released
        time.sleep(0.1)  # So it doesn't accidentally trigger multiple times


def connect_to_server():
    socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    server_address = (config.SERVER_IP, config.SERVER_PORT)
    socket.connect(server_address)

    socket.setblocking(False)

    return (server_address, socket)


def send_message(socket, message):
    print('Sending message:', message)
    socket.send(message)


def listen_for_ping(socket):
    socket.settimeout(2)
    while True:
        try:
            data = socket.recv(1)
            socket.send(data)
            if not data:
                break
        except usocket.timeout:
            pass


connect_wifi(config.SSID, config.PASSWORD)

addr, socket = connect_to_server()
print(f'Connected to server: {addr}')

listen_for_btn_click(socket)
