import asyncio
import pynmea2
import random
from pyModbusTCP.server import ModbusServer


async def handle_mb_server_sim(host: str = "localhost", port: int = 502,
                               no_measurements: int = 1, rand_range: list[int, int] = (1, 100)) -> None:
    """Start & Manage a Modbus TCP Server instance for random measurement simulation

    This function initiates & keeps a Modbus TCP server running forever on the host & port provided, or default values.
    It will simulate measurements & write them to the holding registers, starting to count from register 0.

    Args:
        host: information on the supposed host to run the Modbus Server on; by default it is `localhost`
        port: The port at which the Modbus server should serve; by default it is 502 (standard Modbus port)
        no_measurements: Number of measurements to simulate; each measurement will be available by a single
            holding register; by default 1 measurement
        rand_range: The min & max value for the random number range; by default 1 - 100
    """
    mb_server = ModbusServer(host=host, port=port, no_block=True)
    mb_server.start()
    try:
        while True:
            measurement = [random.randrange(start=rand_range[0], stop=rand_range[1], step=1)
                           for i in range(no_measurements)]
            print(f"Measured Value: {measurement!r}")
            mb_server.data_hdl.write_h_regs(0, measurement, mb_server.ServerInfo())
            await asyncio.sleep(2)
    except KeyboardInterrupt:
        mb_server.stop()


async def handle_nmea_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    """
    Handle incoming NMEA client connections over websocket & send NMEA telegrams to them

    The NMEA telegrams contain random measurement simulations of the ROT NMEA type, with the sender's id being "MG".
    This functions calls sim_nmea_measurement to generate the NMEA telegrams. Though the reader param is not used,
    it is required if called by asyncio.start_server, as it is supposed to happen.

    Args:
        reader: StreamReader object to pass incoming data to the handler
        writer: StreamWriter object to transmit outbound data towards the connected clients
    """
    client_addr = writer.get_extra_info('peername')
    print(f"Client Connected: {client_addr!r}")
    try:
        while True:
            nmea_msg = sim_nmea_measurement(talker="MG", sentence_type="ROT")
            print(f"Send: {nmea_msg!r}")
            writer.write(nmea_msg.encode())
            await writer.drain()
            await asyncio.sleep(2)
    except ConnectionResetError:
        print("Connection Reset error, closing writer")
        writer.close()
    except KeyboardInterrupt:
        print("Closing the connection")
        writer.close()


def sim_nmea_measurement(talker: str = "MG", sentence_type: str = "ROT") -> str:
    """
    Simulates measurement values and returns them in the format of a NMEA sentence.

    By default, the sender id is set to be "MG" and the sentence type is set as "ROT" (Rotational speed)

    Args:
        talker: talker (i.e. sender) id of the NMEA sentence, by default "MG"
        sentence_type: type of the NMEA sentence, by default "ROT"; it defines also the format of the sentence itself
    """
    measurement = float(random.randrange(1,360,1))
    nmea_message = pynmea2.ROT(talker=talker,sentence_type=sentence_type, data=(str(measurement), ))
    return nmea_message.render()







