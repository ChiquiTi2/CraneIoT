import asyncio
import pynmea2
import random
from pyModbusTCP.server import ModbusServer


async def handle_mb_server():
    new_mb_server = ModbusServer('localhost', 8889, no_block=True)
    new_mb_server.start()
    try:
        while True:
            measurement = [random.randrange(1, 100, 1) for i in range(4)]
            print(f"Measured Value: {measurement!r}")
            new_mb_server.data_hdl.write_h_regs(0, measurement, new_mb_server.ServerInfo())
            await asyncio.sleep(2)
    except KeyboardInterrupt:
        new_mb_server.stop()


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info('peername')
    print(f"Client Connected: {addr!r}")
    try:
        while True:
            nmea_msg = sim_nmea_measurement('MG')
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


def sim_nmea_measurement(talker: str) -> str:
    measurement = float(random.randrange(1,360,1))
    nmea_message = pynmea2.ROT(talker,'ROT', (str(measurement), ))
    return nmea_message.render()


async def main() -> None:
    asyncio.create_task(handle_mb_server())
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    try:
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        server.close()

asyncio.run(main())

