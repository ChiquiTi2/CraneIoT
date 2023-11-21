# import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
# import pytest
# import pytest_mock
from src.crane_simulation.sensors import Crane


# from crane_simulation.sensors import rot_sensor
# from crane_simulation.sensors import crane_system
# from crane_simulation.sensors import initialize_modbus_server
# import socket
# from modbus_tcp_server.network import ModbusTCPServer
# from modbus_tcp_server.data_source import TestingDataSource

# print(globals())


@patch.object(src.crane_simulation.sensors, 'gethostbyname')
def test_init_server_sock(mock: MagicMock):
    Crane._init_server_sock(42)
    mock.assert_called()
    pass


# class TestCrane(unittest.TestCase):
#
#     @patch.object(Crane, "__crane_mb_Data")
#     def test_crane_mb_sensors(self, mocked_attr):
#         MyTestCrane = Crane(1)
#         sensor_meas = MyTestCrane.__mb_sensor(1, 1)
#         PropertyMock.assert_called_once_with()




# if __name__ == '__main__':
#     unittest.main()

