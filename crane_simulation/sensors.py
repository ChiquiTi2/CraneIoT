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
from modbus_tcp_server.network import ModbusTCPServer
from modbus_tcp_server.data_source import TestingDataSource
import pynmea2


class Crane:
    """Minimal Crane Control System with sensors

    This is a minimal implementation of a crane control system, providing measurements of a few sensors.
    Its purpose is to be used as a test system to handle similar measurements in an IIOT gateway.

    Attributes:
        unit_id: ID of the implemented Modbus Server instance
    """
    __crane_mb_server = None
    __crane_mb_data = TestingDataSource()
    unit_id: int

    def __init__(self,unit_id: int):
        """Initializes the instance based on Modbus Server Unit ID

            Args:
                unit_id: ID of the implemented Modbus Server instance
        """
        self.unit_id = unit_id

    def run_crane(self):
        """Run the crane instance simulation

        Call this method with no arguments to run the crane simulation. It will set up a Modbus server and cycle through an eternal loop,
        providing random measurements for temperature via Modbus & NMEA ROT Sensor data.
        """
        temp_sensors_address = [1, 2, 3, 4]
        self.__initialize_modbus_server()
        while True:
            for adr in temp_sensors_address:
                self.__mb_sensor(self.unit_id, adr)
            self.rot_sensor()

    def __mb_sensor(self, unit_id: int, data_adr: int) -> int:
        """Write random sensor measurement to Modbus Server

        This is a private method to write a sensor measurement to the Crane's Modbus Server Database.
        Data will be written to a holding register. In addition, the measurement value
        will be returned as an integer.

        Args:
            unit_id: Integer value representing the Modbus Server Unit ID
            data_adr: Address of the holding register to be written onto

        Returns:
            measurement: Integer value of the simulated measurement
        """
        measurement = random.randrange(20, 90, 1)
        self.__crane_mb_data.set_holding_register(unit_id, data_adr, measurement)
        return measurement

    @staticmethod
    def rot_sensor() -> pynmea2.ROT:
        """Simulate random Rotational speed measurement as NMEA ROT message

        This static method simulates a random measurement and returns it as NMEA ROT type message,
        according to NMEA 0183 standard.

        Returns:
            nmea_message: String of the NMEA message correctly formatted as ROT type

        """
        rot_meas = random.randrange(0, 360, 1)
        fl_rot_meas = float(rot_meas)
        nmea_message = pynmea2.ROT('CR', 'ROT', (str(fl_rot_meas),)).render()
        return nmea_message

    def __initialize_modbus_server(self):
        """Initialize and start a Modbus server instance

        Private method to initialize the Modbus Server instance with the host device's socket (i.e. local host) and port 502
        and set it to run.
        """
        host_name = socket.gethostname()
        server_ip = socket.gethostbyname(host_name)
        server_port = 502
        self.__crane_mb_server = ModbusTCPServer(server_ip, server_port, self.__crane_mb_data).start()
        return







