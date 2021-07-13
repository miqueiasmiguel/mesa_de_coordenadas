from datetime import datetime
from time import sleep, time
from typing import Type
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from src.database.repository import PositionRepository


def move_by_point(
    x_axis: int, y_axis: int, user_id: int, client: Type[ModbusClient], trajectory=None
):
    """Função para movimentar a mesa por ponto

    :param x_axis: ponto no eixo x
    :param y_axis: ponto no eixo y
    :param trajectory: nome do arquivo de trajetória
    :param client: cliente mestre modbus
    """

    repository = PositionRepository()
    print("Estou no movimento")
    client.connect()
    sleep(1.7)

    client.write_register(512, x_axis, unit=1)
    timeout = (
        time() + 7
    )  # pretendo fazer esse timeout de acordo com a velocidade setada
    while True:
        x_response = client.read_holding_registers(512, 1, unit=1)
        print("X: {}".format(x_response.registers))
        if time() > timeout:
            print("Erro de Timeout")
            break
        if x_axis == x_response.registers[0]:
            print("Eixo X OK!")
            break

    client.write_register(528, y_axis, unit=1)
    timeout = (
        time() + 7
    )  # pretendo fazer esse timeout de acordo com a velocidade setada
    while True:
        y_response = client.read_holding_registers(528, 1, unit=1)
        print("Y: {}".format(y_response.registers))
        if time() > timeout:
            print("Erro de timeout")
            break
        if y_axis == y_response.registers[0]:
            print("Eixo Y OK!")
            break

    if trajectory:
        repository.insert_position(
            x_axis=x_response.registers[0],
            y_axis=y_response.registers[0],
            date_time=datetime.now(),
            trajectory=trajectory,
            user_id=user_id,
        )
    else:
        repository.insert_position(
            x_axis=x_response.registers[0],
            y_axis=y_response.registers[0],
            date_time=datetime.now(),
            trajectory=None,
            user_id=user_id,
        )

    client.close()
