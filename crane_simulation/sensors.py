"""Classes & functions to simulate sensors or complete machinery systems

The contained classes & functions can be used e.g. for testing other code for
processing data from machinery systems.
It currently contains only the option to simulate a crane control system with Modbus & NMEA data sent

Classes & Functions:
    * class Crane: Minimal Crane Control System with sensors

Typical usage examples:
    myCrane = Crane(unit_id)
    myCrane.run()
    myCrane.rot_sensor()
"""
import socket
import random
from typing import Any

from modbus_tcp_server.network import ModbusTCPServer
from modbus_tcp_server.data_source import TestingDataSource
import pynmea2
import asyncio


class Crane:
    """Minimal Crane Control System with sensors

    This is a minimal implementation of a crane control system, providing measurements of a few sensors.
    Its purpose is to be used as a test system to handle similar measurements in an IIOT gateway.

    Attributes:
        unit_id: ID of the implemented Modbus Server instance
    """
    __crane_mb_server: ModbusTCPServer
    __crane_mb_data = TestingDataSource()
    unit_id: int
    nmea_port = 8000

    def __init__(self, unit_id: int):
        """Initializes the instance based on Modbus Server Unit ID

            Args:
                unit_id: ID of the implemented Modbus Server instance
        """
        self.unit_id = unit_id

    async def run_crane(self) -> None:
        """Run the crane instance simulation

        Call this method with no arguments to run the crane simulation. It will set up a Modbus server and cycle
         through an eternal loop, providing random measurements for temperature via Modbus & NMEA ROT Sensor data.
        """
        await self.__initialize_modbus_server()
        server_sock = await self.__init_server_sock(self.nmea_port)
        q1 = asyncio.Queue()
        q2 = asyncio.Queue()
        _, _, client_sock, client_addr = asyncio.create_task(self.connect_nmea_client(server_sock))
        while True:
            # producers
            mb_producers = [asyncio.create_task(self.__mb_sensor(self.unit_id, i, q1) for i in range(4))]
            nmea_producer = asyncio.create_task(self.rot_sensor("CR", q2))
            mb_consumer = asyncio.create_task(self.write_mb_data(q1))
            nmea_consumer = asyncio.create_task(self.transmit_nmea(q2, client_sock))

    @staticmethod
    async def __mb_sensor(unit_id: int, data_adr: int, q: asyncio.Queue) -> None:
        """Write random sensor measurement to Modbus Server

        This is a private method to write a sensor measurement to the Crane's Modbus Server Database.
        Data will be written to a holding register. In addition, the measurement value
        will be returned as an integer.

        Args:
            unit_id: Integer value representing the Modbus Server Unit ID
            data_adr: Address of the holding register to be written onto
            q: Asyncio Queue object for asynchronous coroutines
        """
        meas_val = random.randrange(20, 90, 1)
        measurement = {"unit_id": unit_id, "data_adr": data_adr, "meas_val": meas_val}
        await q.put(measurement)
        await asyncio.sleep(2)
        return

    @staticmethod
    async def rot_sensor(talker: str, q: asyncio.Queue) -> None:
        """Simulate random Rotational speed measurement as NMEA ROT message

        This static method simulates a random measurement and returns it as NMEA ROT type message,
        according to NMEA 0183 standard.

        Args:
            talker(str): two letter talker ID for the NMEA telegram, e.g. CR for crane
            q(asyncio.Queue): Message Queue object for asynchronous coroutines
        """
        rot_meas = random.randrange(0, 360, 1)
        fl_rot_meas = float(rot_meas)
        nmea_message = pynmea2.ROT(talker, 'ROT', (str(fl_rot_meas),)).render()
        await q.put(nmea_message)
        await asyncio.sleep(2)
        return

    @staticmethod
    async def connect_nmea_client(server: socket.socket) -> tuple[socket.socket, Any]:
        """Listen for an NMEA client to connect to the server

        NMEA Server method which waits for a client to connect and returns the clients details
        (client_socket, client_address). The server will connect to max. 3 clients. Static class method.

        Args:
            server(socket.socket): Socket of the server itself

        Returns:
            client_sock, client_addr (tuple[socket.socket, Any]): Return the client details (socket & address)
        """
        server.listen(3)
        client_sock, client_addr = server.accept()
        return client_sock, client_addr

    async def write_mb_data(self, q: asyncio.Queue) -> None:
        """Write measurement results i Modbus register

        Write the values retrieved from asynchronous Queue to the corresponding register on the Modbus server.
        The information in the queue is available in the format (unit_id, mb_reg_adr, meas_val)

        Args:
            q(asyncio.Queue): The async Queue containing the values to be written into MB Server
        """
        [unit_id, adr_reg, meas_val] = await q.get()
        self.__crane_mb_data.set_holding_register(unit_id, adr_reg, meas_val)
        return

    @staticmethod
    async def transmit_nmea(q: asyncio.Queue, client_sock: socket.socket):
        """Transmit NMEA telegram via Websocket

        This method handles the actual transmitting of NMEA message via Websocket as a Client. Used with asyncio.

        Args:
            q(Queue): Async Queue containing the NMEA message to be sent.
            client_sock(socket.socket): Socket of the Client who is waiting for NMEA messages
        """
        nmea_message = await q.get()
        client_sock.sendall(nmea_message.encode())
        return

    async def __initialize_modbus_server(self):
        """Initialize and start a Modbus server instance

        Private method to initialize the Modbus Server instance with the host device's socket (i.e. local host)
        and port 502 and set it to run.
        """
        host_name = socket.gethostname()
        server_ip = socket.gethostbyname(host_name)
        server_port = 502
        self.__crane_mb_server = ModbusTCPServer(server_ip, server_port, self.__crane_mb_data).start()
        return

    @staticmethod
    async def __init_server_sock(port: int) -> socket.socket:
        """Initialize the websocket for data streaming"""
        host_name = socket.gethostname()
        host = socket.gethostbyname(host_name)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((host, port))
        return server
