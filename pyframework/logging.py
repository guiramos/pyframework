
import os
import platform
from logging.handlers import RotatingFileHandler
import logging

from pyframework.trace import trace_id_format

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
    "filters": {
        "trace_id_filter": {
            "()": "pyframework.trace.filter.TraceIdFilter",
        },
    },
    "formatters": {
        "default": {
            "format": trace_id_format
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "filters": ["trace_id_filter"],
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
            "filters": ["trace_id_filter"],
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
            "filters": ["trace_id_filter"],
        },
    },
}




