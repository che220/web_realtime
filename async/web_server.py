from aiohttp import web
import threading


async def handle(request):
    print('handle:', threading.current_thread().ident)  # same thread as below
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def wshandler(request):
    print('ws:', threading.current_thread().ident)  # same thread as above
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        print('msg type:', msg.type)
        if msg.type == web.WSMsgType.text:
            await ws.send_str("Hello, {}".format(msg.data))
        elif msg.type == web.WSMsgType.binary:
            await ws.send_bytes(msg.data)
        elif msg.type == web.WSMsgType.close:
            break

    return ws


app = web.Application()
app.router.add_get('/echo', wshandler)
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)

web.run_app(app, port=9001)
