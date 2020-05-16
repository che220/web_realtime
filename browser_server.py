import os
import logging
import datetime as dt
import random
import pandas as pd
import numpy as np
import asyncio
import websockets
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


async def time(websocket, path):
    while 1:
        logger.info('waiting 2 ...')
        try:
            now = dt.datetime.utcnow().isoformat() + "Z"
            await websocket.send(now)
            await asyncio.sleep(random.random() * 3)
        except ConnectionClosed:
            logger.info('connection closed')
            break


if __name__ == '__main__':
    start_server = websockets.serve(time, "localhost", 9001)
    logger.info('waiting 1 ...')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()