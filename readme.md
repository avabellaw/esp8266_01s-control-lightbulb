## Flashing micropython

**First erase flash**

python -m esptool --port COM8 erase_flash

**Write flash**

python -m esptool --port [eg COM8] --baud 460800 write_flash --flash_size=detect 0 [PATH TO FILE]

## Upload files using rshell

Install using pip.

rshell works well to upload the files. I had issues originally because I used the wrong size micropython. Therefore, no space was left for my files.

Use `rshell -p [PORT eg COM8]`

### Copy files

`cp ./main.py /pyboard/`

## Connecting to MicroPython shell

Using Putty, you can:
* select 'serial' connection.
* Set "Flow control" (under connection within category on the left) to none
* Set baud to 115200
* Set Serial line to port (eg COM8)

## Issues

**MicroPython doesn't include enviroment variables.**
I decided to import and use a config.py file instead.

**MicroPython also doesn't use threading.**
 I got around this by setting blocking to False on the socket. This means that socket.recv is no longer a blocking call.

`socket.setblocking(False)`

## Physical setup

### Resistors 

* R1 and R2 for 5v power supply

* 68 ohm resister for 2V (Red, yellow, green)

* White and blue is fine as it's 3.3v

* No resistor for button connected to GIO0  
