import os
import logging
import ssl
import pathlib
import asyncio
import websockets

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("localhost.crt")
ssl_context.load_verify_locations(localhost_pem)


async def hello():
    uri = "wss://localhost:9001"
    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        while 1:
            logger.info('What is your name?')
            name = input()

            await websocket.send(name)
            if name == 'q':
                break

            logger.info(f"> {name}")
            greeting = await websocket.recv()
            logger.info(f"< {greeting}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello())