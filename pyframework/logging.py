import contextvars
import json
import os
import platform
import uuid
from logging.handlers import RotatingFileHandler
import logging

from fastapi import Request

from starlette.middleware.base import BaseHTTPMiddleware

APP_NAME = os.getenv('APP_NAME', "app")

log_format = '%(asctime)s - %(name)-15s - %(message)s'
log_formatter = logging.Formatter(log_format)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)


def get_default_log_dir():
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.getenv('APPDATA'), APP_NAME)
    elif system == 'Darwin':  # macOS
        return os.path.join(os.path.expanduser('~'), 'Library', 'Logs', APP_NAME)
    elif system == 'Linux':
        return os.path.join(os.path.expanduser('~'), '.local', 'share', APP_NAME, 'logs')
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")


log_dir = os.getenv('LOG_PATH', get_default_log_dir())
main_app_log_path = os.path.join(log_dir, 'logs', 'app.log')

# logging.basicConfig(level=logging.INFO, format=log_format)
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5  # keep 5 backup logs
app_log_file = main_app_log_path
rolling_file_handler = RotatingFileHandler(app_log_file, maxBytes=log_max_size, backupCount=log_backup_count)
rolling_file_handler.setFormatter(log_formatter)

uvicorn_logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            # Using fixed-width formatting for each field
            "format": "%(asctime)s - %(levelname)6s - %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",  # Default is sys.stderr
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["console"], "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}



# At the top of your main file or a common utilities file
import contextvars

trace_id_var = contextvars.ContextVar('trace_id', default=None)


class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get() or 'no-trace-id'
        return True


class PayloadMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger('payload_logger')
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(
            os.path.join(log_dir, 'logs', 'request_response.log'),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10  # keep 5 backup logs
        )
        formatter = logging.Formatter('%(asctime)s - [%(trace_id)s] - %(message)s')
        handler.setFormatter(formatter)
        handler.addFilter(TraceIdFilter())
        self.logger.addHandler(handler)

    async def dispatch(self, request: Request, call_next):
        # Generate a unique trace_id
        trace_id = str(uuid.uuid4())
        trace_id_var.set(trace_id)

        # Log the incoming request
        request_body = await request.body()
        request_json = {}
        if request_body:
            try:
                request_json = json.loads(request_body)
            except json.JSONDecodeError:
                pass
        self.logger.info(f"{request.method} {request.url.path} {json.dumps(request_json)}")

        # Proceed with the request
        response = await call_next(request)

        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iter(response_body)

        response_text = b''.join(response_body).decode('utf-8')
        try:
            response_json = json.loads(response_text)
            self.logger.info(f"response: {response.status_code} {json.dumps(response_json)}")
        except json.JSONDecodeError:
            self.logger.info(f"response: {response.status_code} {response_text}")

        return response