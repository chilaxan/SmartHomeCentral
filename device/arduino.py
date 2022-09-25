from device import Device
import serial

PORT = '/dev/ttyACM0'

arduino = serial.Serial(port=PORT, baudrate=115200, timeout=.1)
dev = Device('latch')

@dev.register
def lock():
    arduino.write(b'\x01')

@dev.register
def unlock():
    arduino.write(b'\x00')

dev.run()
