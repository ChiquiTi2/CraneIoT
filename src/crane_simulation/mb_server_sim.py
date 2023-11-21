import asyncio
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










