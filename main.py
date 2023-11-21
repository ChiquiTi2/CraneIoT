from src.crane_simulation import NmeaServer
import asyncio


if __name__ == '__main__':
    # My_Crane = Crane(1)
    # My_Crane.run_crane()
    # Server = NmeaServer()
    loop = asyncio.get_event_loop()
    server = NmeaServer('127.0.0.1',8888, loop)
    asyncio.run(Server.initiate_async_server())
