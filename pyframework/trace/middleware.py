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
            # Extract headers from scope and normalize them
            headers = {k.decode('latin1').lower(): v for k, v in scope.get('headers', [])}
            x_trace_id_bytes = headers.get('x-trace-id')
            if x_trace_id_bytes is not None:
                trace_id = x_trace_id_bytes.decode('utf-8')
                self.logger.debug(f"Received trace_id from header: {trace_id}")
            else:
                # Generate a new trace_id
                trace_id = str(uuid.uuid4())
                self.logger.debug(f"No trace_id found in headers. Generated new trace_id: {trace_id}")
            # Store it in contextvars
            trace_id_var.set(trace_id)
        await self.app(scope, receive, send)