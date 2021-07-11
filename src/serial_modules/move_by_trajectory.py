from typing import Type
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from src.serial_modules import move_by_point


def move_by_trajectory(path: str, client: Type[ModbusClient], user_reg: int):
    """Mover por trajetória

    :param path: caminho do arquivo da trajetória
    :param client: cliente mestre modbus
    :param user_reg: matrícula do usuário
    """

    with open(path, "r") as file:

        for linha in file:
            pontos = linha.split()
            x_axis = pontos[0]
            y_axis = pontos[1]
            move_by_point(
                x_axis=x_axis,
                y_axis=y_axis,
                user_reg=user_reg,
                trajectory=path,
                client=client,
            )

        file.close()
