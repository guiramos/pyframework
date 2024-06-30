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
