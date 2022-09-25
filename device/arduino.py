from device import Device
import serial

PORT = '/dev/ttyACM0'

arduino = serial.Serial(port=PORT, baudrate=115200, timeout=.1)
dev = Device('garage')

@dev.register
def open():
    arduino.write(b'\x01')

@dev.register
def close():
    arduino.write(b'\x00')

dev.run()
