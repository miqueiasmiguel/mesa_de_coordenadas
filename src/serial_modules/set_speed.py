from time import sleep
from typing import Type
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def set_speed(x_speed, y_speed, client: Type[ModbusClient]):
    """Define a velocidade dos motores de ambos os eixos

    :param x_speed: velocidade no eixo x
    :param y_speed: velocidade no eixo y
    :param client: cliente mestre modbus
    """

    client.connect()
    sleep(1.7)

    client.write_register(543, x_speed, unit=1)
    client.write_register(559, y_speed, unit=1)
