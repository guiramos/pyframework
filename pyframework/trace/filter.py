import logging

from .context import trace_id_var

class TraceIdFilter(logging.Filter):
    def filter(self, record):
        record.trace_id = trace_id_var.get() or 'no-trace-id'
        return True