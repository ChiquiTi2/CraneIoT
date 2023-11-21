import asyncio
import pynmea2
import random


async def handle_nmea_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    """
    Handle incoming NMEA client connections over websocket & send NMEA telegrams to them

    The NMEA telegrams contain random measurement simulations of the ROT NMEA type, with the sender's id being "MG".
    This functions calls sim_nmea_measurement to generate the NMEA telegrams. Though the reader param is not used,
    it is required if called by asyncio.start_server, as it is supposed to happen.

    Typical usage examples:
        server = await asyncio.start_server(nmea_server_sim.handle_nmea_client, '127.0.0.1', 8888)

    Args:
        reader: StreamReader object to pass incoming data to the handler
        writer: StreamWriter object to transmit outbound data towards the connected clients
    """
    client_addr = writer.get_extra_info('peername')
    print(f"Client Connected: {client_addr!r}")
    try:
        while True:
            nmea_msg = sim_nmea_rot_measurement(talker="MG")
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


def sim_nmea_rot_measurement(talker: str = "MG") -> str:
    """
    Simulates measurement values and returns them in the format of a NMEA sentence.

    By default, the sender id is set to be "MG" and the sentence type is set as "ROT" (Rotational speed)

    Typical usage examples:
        nmea_msg = sim_nmea_measurement(talker="MG", sentence_type="ROT")

    Args:
        talker: talker (i.e. sender) id of the NMEA sentence, by default "MG"
        sentence_type: type of the NMEA sentence, by default "ROT"; it defines also the format of the sentence itself

    Returns:

        ROT type NMEA sentence as a string, for example

        "$MGROT,35.6,A*4E"

        Message end also contains Line Feed & carriage return
    """
    measurement = float(random.randrange(1,360,1))
    nmea_message = pynmea2.ROT(talker=talker,sentence_type="ROT", data=(str(measurement), ))
    return nmea_message.render()