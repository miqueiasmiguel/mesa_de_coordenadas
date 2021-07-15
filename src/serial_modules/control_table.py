from time import time, sleep
from pymodbus.client.sync import ModbusSerialClient


class ControlTable:
    """Classe que gerencia o trontrole da mesa"""

    def __init__(self):
        self.act_x = 0
        self.act_y = 0

    def move_by_point(
        self,
        def_x: int,
        def_y: int,
        x_speed: int,
        y_speed: int,
        client: ModbusSerialClient,
    ):
        """Controla a mesa a partir da definição de ponto

        :param def_x: ponto x definido pelo usuário
        :param def_y: ponto y definido pelo usuário
        :param x_speed: velocidade no eixo x
        :param y_speed: velocidade no eixo y
        :param client: cliente modbus rtu
        :return: dicionário com os parâmetros a serem salvos
        """

        client.connect()
        sleep(1.7)

        # define a velocidade no do eixo x no registrador 0x220
        # e do eixo y no registrador 0x230
        client.write_register(576, x_speed, unit=1)
        client.write_register(592, y_speed, unit=1)

        # escreve no registrador 0x200
        client.write_register(512, def_x, unit=1)

        # deve ser configurado de acordo com a velocidade
        timeout = time() + 7
        while True:
            # lê a o registrador 0x240 que mostra a posição atual do eixo x
            x_response = client.read_holding_registers(576, 1, unit=1)
            self.act_x = x_response.registers[0]
            print("X: {}".format(self.act_x))
            if time() > timeout:
                print("Erro de Timeout")
                break
            if def_x == self.act_x:
                print("Eixo X OK!")
                break

        # escreve no registrador 0x210
        client.write_register(528, def_y, unit=1)

        # deve ser configurado de acordo com a velocidade
        timeout = time() + 7
        while True:
            # lê a o registrador 0x250 que mostra a posição atual do eixo x
            y_response = client.read_holding_registers(592, 1, unit=1)
            self.act_y = y_response.registers[0]
            print("Y: {}".format(self.act_y))
            if time() > timeout:
                print("Erro de timeout")
                break
            if def_y == self.act_y:
                print("Eixo Y OK!")
                break

        return {
            "act_x": self.act_x,
            "act_y": self.act_y,
            "x_speed": x_speed,
            "y_speed": y_speed,
        }

    def get_act_x(self):
        """Retorna o valor do registrador que
        representa o valor atual do eixo x

        :return: valor atual do eixo x
        """

        return self.act_x

    def get_act_y(self):
        """Retorna o valor do registrador que
        representa o valor atual do eixo y

        :return: valor atual do eixo y
        """

        return self.act_y
