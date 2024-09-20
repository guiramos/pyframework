# trace/middleware.py
import logging
import uuid
from starlette.types import ASGIApp, Receive, Scope, Send
from .context import trace_id_var

class TraceIDMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app
        self.logger = logging.getLogger('TraceIDMiddleware')
        self.logger.setLevel(logging.INFO)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] == 'http':
            # Generate a unique trace_id
            trace_id = str(uuid.uuid4())
            # Store it in contextvars
            trace_id_var.set(trace_id)
        await self.app(scope, receive, send)
