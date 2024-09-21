# services/base.py
import logging

from ..logging import app_log_file_rolling_file_handler, app_console_handler


class BaseService:
    def __init__(self):
        # Create a logger with the name of the service class
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)

        # Create a handler that writes log entries to a file
        # logs_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        # os.makedirs(logs_dir, exist_ok=True)

        # Add the handlers to the logger
        self.logger.addHandler(app_log_file_rolling_file_handler)
        self.logger.addHandler(app_console_handler)

        # Avoid propagating logs to the root logger
        self.logger.propagate = False
