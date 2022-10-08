import logging
from typing import List, Dict, Callable
from .remote_functions import RemoteFunctions
from .pipe_exception import PipeException
from .protocol_exception import ProtocolException
from .types import decompose_type, mask_bytes_size, deserialize_int, deserialize_float
from .types import CLASS_VOID, CLASS_BOOLEAN, CLASS_INT, CLASS_FLOAT, CLASS_STRING, CLASS_TABLE, CLASS_LINK
from .types import CLASS_FUNCTION
from .types import MASK_VOID, MASK_BOOL_TRUE, MASK_BOOL_FALSE

_logger = logging.getLogger(__name__)


class InputPipe:

    def __init__(self, input_stream):
        self.input_stream = input_stream
        self.remote_functions = None
        self.class_switch = {
            CLASS_VOID: self._read_void,
            CLASS_BOOLEAN: self._read_boolean,
            CLASS_INT: self._read_int,
            CLASS_FLOAT: self._read_float,
            CLASS_STRING: self._read_string,
            CLASS_TABLE: self._read_table,
            CLASS_LINK: self._read_link,
            CLASS_FUNCTION: self._read_function,
        }
        self.strings_encoding = "cp1252"  # default windows encoding, since library is for windows named pipes

    def set_strings_encoding(self, encoding: str):
        self.strings_encoding = encoding

    def set_remote_functions(self, remote_functions: RemoteFunctions):
        self.remote_functions = remote_functions

    def read(self):
        try:
            stored_objects = []
            return self._read(stored_objects)
        except OSError as e:
            _logger.error(e)
            raise PipeException()

    def _read(self, stored_objects: List[Dict]):
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

    @staticmethod
    def _read_boolean(mask: int, _) -> bool:
        if mask == MASK_BOOL_TRUE:
            return True
        elif mask == MASK_BOOL_FALSE:
            return False
        _logger.error(f"unknown boolean mask: {mask}")
        raise ProtocolException()

    def _read_int(self, mask: int, _) -> int:
        bytes_size = mask_bytes_size(mask)
        _logger.debug(f"reading {bytes_size} bytes of int")
        bytes_arr = self._read_raw(bytes_size)
        result = deserialize_int(bytes_arr)
        return result

    def _read_float(self, mask: int, _) -> float:
        bytes_size = mask_bytes_size(mask)
        _logger.debug(f"reading {bytes_size} bytes of float")
        bytes_arr = self._read_raw(bytes_size)
        result = deserialize_float(bytes_arr, mask)
        return result

    def _read_string(self, mask: int, _) -> str:
        length = self._read_int(mask, None)
        _logger.debug(f"length of string being read is {length}")
        bytes_arr = self._read_raw(length)
        result = bytes_arr.decode(self.strings_encoding)
        return result

    def _read_table(self, mask: int, stored_objects: List[Dict]) -> Dict:
        size = self._read_int(mask, None)
        _logger.debug(f"reading dict with {size} items")
        result = dict()
        stored_objects.append(result)
        for _ in range(size):
            key = self._read(stored_objects)
            val = self._read(stored_objects)
            # TODO: there is an issue with dicts can't be keys of dict
            result[key] = val
        return result

    def _read_link(self, mask: int, stored_objects: List[Dict]) -> Dict:
        link_id = self._read_int(mask, None)
        result = stored_objects[link_id]
        return result

    def _read_function(self, mask: int, _) -> Callable:
        if self.remote_functions is None:
            _logger.error("receiving of remote functions not allowed")
            raise ProtocolException()
        func_id = self._read_int(mask, None)
        result = self.remote_functions.get_function(func_id)
        return result
