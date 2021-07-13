from time import sleep
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


client = ModbusClient(method="rtu", port="COM5", parity="N", baudrate=9600, bytesize=8)

client.connect()
sleep(1.7)

write = client.write_register(528, 1000, unit=1)
response = client.read_holding_registers(528, 1, unit=1)
print(response.registers)
