from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def configure_client(port, baudrate):
    """Configura um cliente RTU
    :param port: porta serial
    :baudrate: baudrate
    :return: cliente com as configurações fornecidas
    """

    client = ModbusClient(
        method="rtu", port=port, baudrate=baudrate, parity="N", timeout=1, bytesize=8
    )
    return client
