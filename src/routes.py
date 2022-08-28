from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles

from .endpoints import HomePage, ChatWebSockets

routes = [
    Route('/', HomePage),
    WebSocketRoute('/ws', ChatWebSockets),
    Mount('/static', app=StaticFiles(directory='static'))
]
