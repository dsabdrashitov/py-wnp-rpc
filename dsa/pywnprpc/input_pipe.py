import logging
from typing import List
from .pipe_exception import PipeException
from .protocol_exception import ProtocolException
from .types import decompose_type, mask_bytes_size, deserialize_int
from .types import CLASS_VOID, CLASS_INT
from .types import MASK_VOID

_logger = logging.getLogger(__name__)


class InputPipe:

    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.remote_functions = None
        self.class_switch = {
            CLASS_VOID: self._read_void,
            CLASS_INT: self._read_int,
        }

    def read(self):
        try:
            stored_objects = []
            return self._read(stored_objects)
        except OSError as e:
            _logger.error(e)
            raise PipeException()

    def _read(self, stored_objects: List):
        obj_type = self._read_raw(1)[0]
        obj_class, obj_mask = decompose_type(obj_type)
        if obj_class not in self.class_switch:
            _logger.error(f"unknown class {obj_class}")
            raise ProtocolException()
        read_method = self.class_switch[obj_class]
        result = read_method(obj_mask, stored_objects)
        return result

    def _read_raw(self, size: int) -> bytes:
        result = self.input_stream.read(size)
        if len(result) != size:
            _logger.error("not enough bytes in stream")
            raise ProtocolException()
        return result

    @staticmethod
    def _read_void(mask: int, _) -> None:
        if mask != MASK_VOID:
            _logger.error(f"void has wrong mask: {mask}")
            raise ProtocolException()
        return None

    def _read_int(self, mask: int, _) -> int:
        bytes_size = mask_bytes_size(mask)
        _logger.debug(f"reading {bytes_size} bytes int")
        bytes_arr = self._read_raw(bytes_size)
        result = deserialize_int(bytes_arr)
        return result
