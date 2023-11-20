"""NMEA message handling server class & functions"""
import asyncio

import pynmea2

class NmeaServer():
    def __init__(self, ip: str, port: int, loop: asyncio.AbstractEventLoop):
        self.__ip: str = ip
        self.__port:int = port
        self.__loop: asyncio.AbstractEventLoop = loop
        print(f"Server initialized with {self.__ip}:{self.__port}")

    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    @property
    def loop(self):
        return self.__loop

    def start_server(self):
        try:
            self.server = asyncio.start_server(
                self.accept_client, self.ip, self.port)
            self.loop.run_until_complete(self.server)
            self.loop.run_forever()
        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("Keyboard Interrupt Detected. Shutting down!")

    def accept_client(self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter):
        task = asyncio.Task(self.handle_client(client_reader, client_writer))
        client_ip = client_writer.get_extra_info('peername')[0]
        client_port = client_writer.get_extra_info('peername')[1]
        print(f"New Connection: {client_ip}:{client_port}")

    async def handle_client(self, client_reader: asyncio.StreamReader, client_writer: asyncio.StreamWriter):
        while True:
            client_message = str((await client_reader.read(255)).decode('utf8'))
            if client_message.startswith("quit"):
                break

            print(f"{client_message}")
            await client_writer.drain()
        print("Client Disconnected!")

    async def initiate_async_server(self):
        server = await asyncio.start_server(
            self.handle_nmea_data, '127.0.0.1', 8888)
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')
        async with server:
            await server.serve_forever()

    @staticmethod
    async def handle_nmea_data(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        message = "This is a test"
        writer.write(message.encode())
        print("Writing...")
        await writer.drain()
        print("Message written")
        writer.close()
        await writer.wait_closed()
