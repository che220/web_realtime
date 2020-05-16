import os
import logging
import datetime as dt
import random
import asyncio
import websockets
import threading
from websockets.exceptions import ConnectionClosed

logging.basicConfig(format='%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s] %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))


async def send_msg(websocket):
    curr_time = dt.datetime.utcnow().isoformat() + "Z"
    client_ip, client_port = websocket.remote_address
    await websocket.send(f'sending thread: {curr_time}, '
                         f'client: {client_ip}:{client_port} thread: {threading.current_thread().ident}')
    await asyncio.sleep(2)


async def time(websocket: websockets.server.WebSocketServerProtocol, path):
    logger.info(f'function thread: {threading.current_thread().ident}: waiting 2 ...')
    while 1:
        try:
            client_ip, client_port = websocket.remote_address
            local_ip, local_port = websocket.local_address
            logger.info('client: local=%s:%s, remote=%s:%s', local_ip, local_port, client_ip, client_port)
            await send_msg(websocket)
#            await websocket.send(f'sending thread: {threading.current_thread().ident}: client: {client_ip}:{client_port}')
            #await asyncio.sleep(random.random() * 3)
        except ConnectionClosed:
            logger.info('connection closed')
            break


if __name__ == '__main__':
    logger.info(f'main thead: {threading.current_thread().ident}')
    start_server = websockets.serve(time, "localhost", 9001)
    logger.info('waiting 1 ...')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()