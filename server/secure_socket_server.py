import os
import logging
import pandas as pd
import numpy as np
import asyncio
import websockets
import ssl
import pathlib
from websockets.exceptions import ConnectionClosed

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

pd.set_option('display.width', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_colwidth', 5000)
pd.set_option('max_columns', 600)
pd.set_option('display.float_format', lambda x: '%.2f' % x)  # disable scientific notation for print
np.set_printoptions(linewidth=5000, suppress=True)  # print out all values, regardless length. no scientific notation


async def hello(websocket, path):
    while 1:
        logger.info('waiting 2 ...')
        try:
            name = await websocket.recv()
            logger.info(f"< {name}")

            greeting = f"Hello {name}!"

            await websocket.send(greeting)
            logger.info(f"> {greeting}")
        except ConnectionClosed:
            logger.error("Connection closed by client.")
            break


if __name__ == '__main__':
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    localhost_pem = pathlib.Path(__file__).with_name("localhost.crt")
    ssl_context.load_cert_chain(localhost_pem)

    start_server = websockets.serve(hello, "localhost", 9001, ssl=ssl_context)
    logger.info('waiting 1 ...')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
