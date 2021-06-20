import serial

serial_port = serial.Serial()

serial_port.baudrate = 9600
serial_port.port = "COM5"

serial_port.bytesize = 8
serial_port.parity = "N"
serial_port.stopbits = 1
serial_port.timeout = 1
