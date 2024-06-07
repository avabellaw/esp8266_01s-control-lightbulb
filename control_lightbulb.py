import os
import env  # noqa
import tinytuya
from enum import Enum


class BrightnessLevel(Enum):
    LOW = (10, 330)
    MEDIUM = (340, 660)
    HIGH = (670, 1000)


LOW_BRIGHTNESS_LEVEL = BrightnessLevel.LOW.value[0]
MED_BRIGHTNESS_LEVEL = (BrightnessLevel.MEDIUM.value[0] + BrightnessLevel.MEDIUM.value[1]) / 2
HIGH_BRIGHTNESS_LEVEL = BrightnessLevel.HIGH.value[1]


class LightBulb:
    def __init__(self):
        self.light = tinytuya.BulbDevice(
            dev_id=os.environ['DEVICE_ID'],

            # Can set to 'Auto' to auto-discover IP address
            address=os.environ['DEVICE_IP_ADDRESS'],

            # Get from TinyTuya scan
            # Or on tuya IOT: Cloud explorer -> Device management
            #                 -> Query Device details
            # Then submit the device ID and read the response
            local_key=os.environ['LOCAL_KEY'],
            version=3.3)

        data = self.light.status()
        print(data)
        dps = data['dps']
        self.is_on = dps['20']
        self.brightness = dps['22']
        self.brightness_level = self.get_brightness_level()
        print(self.brightness)

    def get_status(self):
        dps = self.light.status()['dps']
        return {"is_on": dps['20'],
                "brightness": dps['22']}

    def get_brightness_level(self):
        print(f"brighness: {self.brightness}")
        print(f"Brightness high 1: {BrightnessLevel.HIGH.value[0]}\
            Brightness high 2: {BrightnessLevel.HIGH.value[1]}\
            in range: {self.brightness in range(BrightnessLevel.HIGH.value[0], BrightnessLevel.HIGH.value[1] + 1)}\
            ")
        if self.brightness in range(BrightnessLevel.LOW.value[0],
                                    BrightnessLevel.LOW.value[1]):
            return BrightnessLevel.LOW
        elif self.brightness in range(BrightnessLevel.MEDIUM.value[0],
                                      BrightnessLevel.MEDIUM.value[1]):
            return BrightnessLevel.MEDIUM
        elif self.brightness in range(BrightnessLevel.HIGH.value[0],
                                      BrightnessLevel.HIGH.value[1] + 1):
            return BrightnessLevel.HIGH

    def toggle(self):
        self.light.turn_off() if self.is_on else self.light.turn_on()
        self.is_on = not self.is_on

    def get_next_brightness_level(self):
        current_level = self.get_brightness_level()

        if current_level == BrightnessLevel.LOW:
            return MED_BRIGHTNESS_LEVEL
        elif current_level == BrightnessLevel.MEDIUM:
            return HIGH_BRIGHTNESS_LEVEL
        elif current_level == BrightnessLevel.HIGH:
            return LOW_BRIGHTNESS_LEVEL

    def toggle_brightness(self):
        status = self.get_status()
        self.brightness = status["brightness"]
        print(f"Current brightness: {self.brightness}")
        self.brightness = int(self.get_next_brightness_level())
        print(f"Setting brightness to {self.brightness}")

        self.light.set_brightness(self.brightness)


def get_lightbulb_instance():
    try:
        light = LightBulb()
        return light
    except Exception as e:
        print(f"Issue with lightbulb: {e}")
        return None
