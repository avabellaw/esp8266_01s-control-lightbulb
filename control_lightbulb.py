import os
import env # noqa
import tinytuya


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
        self.is_on = data['dps']['20']

    def toggle(self):
        self.light.turn_off() if self.is_on else self.light.turn_on()
        self.is_on = not self.is_on


light = LightBulb()
