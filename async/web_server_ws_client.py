import os
import logging
import asyncio
import websockets

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


async def hello():
    uri = "ws://localhost:9001/echo"
    async with websockets.connect(uri) as websocket:
        await websocket.send("this is a ws messa234ge")
        greeting = await websocket.recv()
        logger.info(f"< {greeting}")


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(hello())