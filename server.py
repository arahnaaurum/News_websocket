import os
import asyncio
from aiohttp import web

WS_FILE = os.path.join(os.path.dirname(__file__), 'websocket.html')

# Создаем очередь, которую будем использовать для хранения новостей
channel = asyncio.Queue()


# обработчик для POST - запросов с новостями
async def newshandler(request):
    result = await request.post()
    print('POST       :', result)
    await channel.put(result)
    return web.Response(text='OK')


# обработчик для GET - запросов
async def wshandler(request):
    resp = web.WebSocketResponse()
    available = resp.can_prepare(request)
    if not available:
        with open(WS_FILE, "rb") as fp:
            return web.Response(body=fp.read(), content_type="text/html")

    await resp.prepare(request)
    print("Было создано новое подключение")
    request.app["sockets"].append(resp)

    while True:
        res = await channel.get()
        for ws in request.app["sockets"]:
            await ws.send_str(res['text'])
            print('Текст отправлен')
            await ws.ping('Pinged')
    return resp


async def on_shutdown(app):
    for ws in app["sockets"]:
        await ws.close()


loop = asyncio.get_event_loop()
app = web.Application()
app["sockets"] = []
app.add_routes([web.get('/', wshandler),
               web.post('/news', newshandler)])


web.run_app(app, loop=loop)
if __name__ == '__main__':
    web.run_app(app)