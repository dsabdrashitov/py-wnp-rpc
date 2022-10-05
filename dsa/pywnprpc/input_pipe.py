import logging
from .pipe_exception import PipeException
from .protocol_exception import ProtocolException
from .types import decompose_type

_logger = logging.getLogger(__name__)


class InputPipe:

    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.remote_functions = None

    def read(self):
        try:
            stored_objects = []
            return self._read(stored_objects)
        except OSError:
            raise PipeException()

    def _read(self, stored_objects):
        obj_type = self._read_raw(1)[0]
        obj_class, obj_mask = decompose_type(obj_type)
        _logger.info(f"{obj_class}, {obj_mask}")

    def _read_raw(self, size):
        result = self.input_stream.read(size)
        if len(result) != size:
            raise ProtocolException()
        return result
