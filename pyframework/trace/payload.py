# trace/payload.py
import json
import logging
import os
from logging.handlers import RotatingFileHandler
from starlette.types import ASGIApp, Receive, Scope, Send
from .filter import TraceIdFilter

class PayloadMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app
        self.logger = logging.getLogger('payload_logger')
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            os.path.join('logs', 'request_response.log'),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10
        )
        formatter = logging.Formatter('%(asctime)s - [%(trace_id)s] - %(message)s')
        handler.setFormatter(formatter)
        handler.addFilter(TraceIdFilter())
        self.logger.addHandler(handler)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        # Capture the request body
        body = b''
        more_body = True

        async def receive_wrapper():
            nonlocal body, more_body
            message = await receive()
            if message['type'] == 'http.request':
                body += message.get('body', b'')
                more_body = message.get('more_body', False)
            return message

        # Capture the response
        response_body = b''
        status_code = None

        async def send_wrapper(message):
            nonlocal response_body, status_code
            if message['type'] == 'http.response.start':
                status_code = message['status']
            elif message['type'] == 'http.response.body':
                response_body += message.get('body', b'')
            await send(message)

        # Call the next middleware or actual handler
        await self.app(scope, receive_wrapper, send_wrapper)

        # Log the request
        try:
            request_body = body.decode('utf-8')
            request_json = json.loads(request_body)
            request_body_str = json.dumps(request_json)
        except Exception:
            request_body_str = body.decode('utf-8', errors='replace')

        self.logger.info(f"{scope['method']} {scope['path']} {request_body_str}")

        # Log the response
        try:
            response_body_str = response_body.decode('utf-8')
            response_json = json.loads(response_body_str)
            response_body_str = json.dumps(response_json)
        except Exception:
            response_body_str = response_body.decode('utf-8', errors='replace')

        self.logger.info(f"response: {status_code} {response_body_str}")