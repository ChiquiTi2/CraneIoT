import asyncio

import pynmea2

import mb_server_sim
import nmea_server_sim


async def async_manager() -> None:
    """
    Handles the execution of parallel asynchronous tasks

    There are two parallel processes: Updating the Modbus server simulated measurements & transmitting the additional
    simulated measurements via NMEA. For the NMEA messages, the asyncio.start_server function is used, based on an
    underlying websocket. The server is supposed to run forever unless the program is stopped by Keyboard interrupt.
    """
    asyncio.create_task(mb_server_sim.handle_mb_server_sim(port=8889, no_measurements=4))
    server = await asyncio.start_server(nmea_server_sim.handle_nmea_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")
    try:
        async with server:
            await server.serve_forever()
    except KeyboardInterrupt:
        server.close()


if __name__ == "__main__":
    print(pynmea2.ROT("MG","ROT",("32.0","A")))
    #asyncio.run(async_manager())