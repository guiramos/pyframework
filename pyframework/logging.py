from logging.handlers import RotatingFileHandler
import logging

log_format = '%(asctime)s - %(name)-27s - %(message)s'
log_formatter = logging.Formatter(log_format)

# logging.basicConfig(level=logging.INFO, format=log_format)
log_max_size = 10 * 1024 * 1024  # 10 MB
log_backup_count = 5  # keep 5 backup logs
app_log_file = 'logs/app.log'
rolling_file_handler = RotatingFileHandler(app_log_file, maxBytes=log_max_size, backupCount=log_backup_count)
rolling_file_handler.setFormatter(log_formatter)


uvcorn_logging_config = {
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
