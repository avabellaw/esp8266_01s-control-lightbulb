import network
import time
from machine import Pin
import usocket
import config

# LED on espboard8266 01s is GPIO2
led = Pin(2, Pin.OUT)  # GPIO2
button = Pin(0, Pin.IN, Pin.PULL_UP)  # GPIO0

# 1 for interal led, 0 for external led
LED_OFF = 0

led.value(LED_OFF)  # Ensure led is off at start

socket = None


def toggle_led():
    led.value(not led.value())


def blink_led(count=1, blink_len=0.1):
    count *= 2  # Toggle on, toggle off
    # Common anode configuaration and therefore, 1 is off
    # (cathode to ground)
    led.value(LED_OFF)  # Ensure led is off before blinking
    for i in range(count):
        toggle_led()
        time.sleep(blink_len)
    led.value(LED_OFF)  # Ensure led is off after blinking


def connect_wifi(ssid, password):
    print('Connecting to WiFi...')
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            blink_led(1, 1)
        print(f'Connected to WiFi: {ssid}\n\
                Network config: {sta_if.ifconfig()}')
        blink_led(4, 0.2)  # Blink 5 times with 0.2 second interval


def button_clicked(pin):
    send_message(socket, config.BUTTON_CLICK)
    blink_led(1, 0.1)


def connect_to_server():
    socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    server_address = (config.SERVER_IP, config.SERVER_PORT)

    # Need to add feedback if not connected
    socket.connect(server_address)

    socket.setblocking(False)

    return (server_address, socket)


def send_message(socket, message):
    print('Sending message:', message)
    socket.send(message)


connect_wifi(config.SSID, config.PASSWORD)

addr, socket = connect_to_server()
print(f'Connected to server: {addr}')

# Setup event handler (interrupt) for button press
# This is more power effiecient than polling
button.irq(trigger=Pin.IRQ_FALLING, handler=button_clicked)
