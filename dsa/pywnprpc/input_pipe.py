import logging

_logger = logging.getLogger(__name__)


class InputPipe:

    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.remote_functions = None

    def read(self):
        return None
