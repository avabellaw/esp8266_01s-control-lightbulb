## Using ampy to upload files

ampy --port [eg. COM8] put main.py

have to use ampy with python 3.1.0 as the dependency distutils is depreceated in 3.1.2

[Upload using ampy](https://pythonforundergradengineers.com/upload-py-files-to-esp8266-running-micropython.html)

import esp
esp.osdebug(None)
then close putty

**List dir** ampy --port COM8 --baud 115200 ls 

## Flashing micropython

**First erase flash**

python -m esptool --port COM8 erase_flash

**Write flash**

python -m esptool --port [eg COM8] --baud 460800 write_flash --flash_size=detect 0 [PATH TO FILE]

## rshell

I ended up using rshell to upload the files. More on this.

## Issues

MicroPython doesn't include enviroment variables.
I decided to import and use a config.py file instead.


