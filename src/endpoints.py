from typing import Any, List

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from starlette.websockets import WebSocket

from websockets_actions.actions import WebSocketBroadcast


class HomePage(HTTPEndpoint):
    async def get(self, request: Request) -> Jinja2Templates.TemplateResponse:
        template = Jinja2Templates(directory='templates')
        return template.TemplateResponse('index.html', {'request': request})


class ChatWebSockets(WebSocketBroadcast):
    actions: List[str] = ['join', 'send_message', 'close']

    async def join(self, websocket: WebSocket, data: Any) -> None:
        await self.manager.broadcast({'action': 'join', 'message': data.get('username')})

    async def send_message(self, websocket: WebSocket, data: Any) -> None:
        await self.manager.broadcast({
            'action': 'newMessage',
            'username': data.get('username'),
            'message': data.get('message')
        })

    async def close(self, websocket: WebSocket, data: Any | None = None) -> None:
        await super().on_disconnect(websocket, 1000)
        await self.manager.broadcast_exclude(
            [websocket],
            {'action': 'disconnect', 'message': data.get('username')}
        )
