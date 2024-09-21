# services/base.py
import logging
from logging.handlers import RotatingFileHandler
import os

from . import trace_id_format
from .filter import TraceIdFilter

class BaseService:
    def __init__(self):
        # Create a logger with the name of the service class
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        # Create a handler that writes log entries to a file
        logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, 'service.log'),
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=10
        )

        # Create a console handler
        console_handler = logging.StreamHandler()

        # Define a formatter that includes the trace_id
        formatter = logging.Formatter(trace_id_format)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the TraceIdFilter to include trace_id in log records
        file_handler.addFilter(TraceIdFilter())
        console_handler.addFilter(TraceIdFilter())

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Avoid propagating logs to the root logger
        self.logger.propagate = False
