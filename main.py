import asyncio
import logging
import websockets
import names
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from courses import main_

logging.basicConfig(level=logging.INFO)
# py_logger = logging.getLogger(__name__)
# py_logger.setLevel(logging.INFO)
# py_handler = logging.FileHandler("Program.log", mode='w')

class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            command = message.split(' ')
            if command[0] == 'exchange':
                try:
                    l = main_(command[1])
                except:
                    l=main_(1)
                x = await l
                await self.send_to_clients(f"{ws.name}: '{x}'")
                # py_logger.info(f"Testing the custom logger for module...")
            else:
                await self.send_to_clients(f"{ws.name}: '{message}'")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
