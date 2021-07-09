from time import sleep, time
from typing import Type
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def move_by_point(x_axis: int, y_axis: int, client: Type[ModbusClient]):
    """Função para movimentar a mesa por ponto

    :param x_axis: ponto no eixo x
    :param y_axis: ponto no eixo y
    :param client: cliente mestre modbus
    """

    client.connect()
    sleep(1.7)

    client.write_register(511, x_axis, unit=1)
    timeout = (
        time() + 7
    )  # pretendo fazer esse timeout de acordo com a velocidade setada
    while True:
        x_response = client.read_holding_registers(511, 1, unit=1)
        if time() > timeout:
            print("Erro")
            break
        if x_axis == x_response[0]:
            print("Eixo X OK!")
            break

    client.write_register(527, y_axis, unit=1)
    timeout = (
        time() + 7
    )  # pretendo fazer esse timeout de acordo com a velocidade setada
    while True:
        y_response = client.read_holding_registers(527, 1, unit=1)
        if time() > timeout:
            print("Erro")
            break
        if y_axis == y_response[0]:
            print("Eixo Y OK!")
            break

    client.close()
