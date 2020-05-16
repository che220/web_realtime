import os
import logging
import asyncio
import websockets

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


async def hello():
    uri = "ws://localhost:9001"
    async with websockets.connect(uri) as websocket:
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