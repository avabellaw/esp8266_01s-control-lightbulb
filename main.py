import network
import time
from machine import Pin, reset
import usocket
import config
from log import log

button_down = False

# LED on espboard8266 01s is GPIO2
led = Pin(2, Pin.OUT)  # GPIO2
button = Pin(0, Pin.IN, Pin.PULL_UP)  # GPIO0

# 1 for interal led, 0 for external led
LED_OFF = 1

led.value(LED_OFF)  # Ensure led is off at start

socket = None

button_held_down_start = 0

short_press_ms = 320


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
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            blink_led(1, 1)
        blink_led(2, 0.4)


def button_clicked(time_held_down):
    if config.DEBUG:
        print(f"Button held down for {time_held_down}ms")
    blink_led(1, 0.1)

    if time_held_down <= short_press_ms:
        send_message(socket, config.BUTTON_SHORT_CLICK)
    else:
        send_message(socket, config.BUTTON_LONG_CLICK)


def button_event_handler(pin):
    global button_down
    global button_held_down_start

    if not pin.value():  # Button down
        if not button_down:
            button_down = True
            button_held_down_start = time.ticks_ms()
    else:  # Button released
        if button_down:
            button_held_down_finish = time.ticks_ms()

            time_held_down = button_held_down_finish - button_held_down_start
            button_down = False

            button_clicked(time_held_down)


def connect_to_server():
    socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    server_address = (config.SERVER_IP, config.SERVER_PORT)

    # Need to add feedback if not connected
    try:
        socket.connect(server_address)
    except OSError as e:
        blink_led(8, 0.1)
        error_restart(socket, e, "Error connecting to server")
    else:
        blink_led(1, 0.8)

    return (server_address, socket)


def send_message(socket, message):
    try:
        socket.send(message)
    except OSError as e:
        title = "Error sending message"
        error_restart(socket, e, title)


def error_restart(socket, e, title="Error"):
    blink_led(2, 0.1)
    blink_led(1, 0.5)
    blink_led(2, 0.1)
    socket.close()
    log(e, config.DEBUG, title)
    time.sleep(5)
    reset()


connect_wifi(config.SSID, config.PASSWORD)

addr, socket = connect_to_server()

# Setup event handler (interrupt) for button press
# This is more power effiecient than polling
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
           handler=button_event_handler)

while True:
    send_message(socket, b'0')
    time.sleep(5)
