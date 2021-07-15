import io
import csv
from typing import List, Tuple


class CSVWriter:
    """Classe que armazena as funções para realizar
    o download do histórico solicitado"""

    def users_csv(self, content: List[Tuple]):
        """Recebe uma lista com todos os usuários e
        escreve em um arquivo csv

        :param content: Lista com todos os usuários
        :return: arquivo csv com o conteúdo escrito
        """

        output = io.StringIO()
        writer = csv.writer(output)

        line = ["Matrícula", "Nome", "E-mail", "Especial"]
        writer.writerow(line)
        for user in content:
            line = []
            line.append(user[0])
            line.append(user[1])
            line.append(user[2])
            line.append(user[3])
            writer.writerow(line)
        output.seek(0)

        return output

    def positions_csv(self, content: List[Tuple]):
        """Recebe uma lista com todas as posições e
        escreve em um arquivo csv

        :param content: Lista com todas as posições
        :return: arquivo csv com o conteúdo escrito
        """

        output = io.StringIO()
        writer = csv.writer(output)

        line = [
            "Nome",
            "Eixo X",
            "Eixo Y",
            "Trajetoria",
            "Velocidade X",
            "Velocidade Y",
            "Data e hora",
        ]
        writer.writerow(line)
        for position in content:
            line = []
            line.append(position[0])
            line.append(position[1])
            line.append(position[2])
            line.append(position[3])
            line.append(position[4])
            line.append(position[5])
            line.append(position[6])
            writer.writerow(line)
        output.seek(0)
        return output

    def sessions_csv(self, content: List[Tuple]):
        """Recebe uma lista com todas as sessões e
        escreve em um arquivo csv

        :param content: Lista com todas as sessões
        :return: arquivo csv com o conteúdo escrito
        """

        output = io.StringIO()
        writer = csv.writer(output)

        line = ["Matrícula", "Nome", "Hora do login", "Duração (min)"]
        writer.writerow(line)

        for session in content:
            line = []
            line.append(session[0])
            line.append(session[1])
            line.append(session[2])
            line.append(session[3])
            writer.writerow(line)
        output.seek(0)
        return output
