import logging
from typing import Iterable, BinaryIO, Any, Dict
from .pipe_exception import PipeException
from .types import compose_type, int_mask, serialize_int, serialize_float
from .types import CLASS_VOID, CLASS_BOOLEAN, CLASS_INT, CLASS_FLOAT, CLASS_STRING, CLASS_TABLE, CLASS_LINK
from .types import MASK_VOID, MASK_BOOL_TRUE, MASK_BOOL_FALSE, MASK_FLOAT64

_logger = logging.getLogger(__name__)


class OutputPipe:

    _COUNT_KEY_OBJECT = object()
    _COUNT_KEY = id(_COUNT_KEY_OBJECT)

    def __init__(self, output_stream: BinaryIO):
        self.output_stream = output_stream
        self.local_functions = None
        self.strings_encoding = "cp1252"  # default windows encoding, since library is for windows named pipes
        self.class_switch = {
            type(None): self._write_void,
            bool: self._write_boolean,
            int: self._write_int,
            float: self._write_float,
            str: self._write_string,
            dict: self._write_table,
        }

    def set_strings_encoding(self, encoding: str):
        self.strings_encoding = encoding

    def write(self, obj: Any) -> None:
        try:
            stored_objects = dict()
            stored_objects[self._COUNT_KEY] = 0
            self._write(obj, stored_objects)
        except OSError as e:
            _logger.error(e)
            raise PipeException()

    def _write(self, obj: Any, stored_objects: Dict[int, int]) -> None:
        _logger.debug(f"writing {obj}")
        python_type = type(obj)
        if python_type not in self.class_switch:
            err = f"type {python_type} not supported"
            _logger.error(err)
            raise TypeError(err)
        write_method = self.class_switch[python_type]
        # noinspection PyArgumentList
        write_method(obj, stored_objects)

    def _write_raw(self, sequence_of_bytes: Iterable[int]) -> None:
        block = bytes(sequence_of_bytes)
        _logger.debug(f"write block of {len(block)} bytes")
        self.output_stream.write(block)

    def _write_void(self, _0, _1) -> None:
        obj_type = compose_type(CLASS_VOID, MASK_VOID)
        self._write_raw([obj_type, ])

    def _write_boolean(self, obj: bool, _) -> None:
        if obj:
            obj_mask = MASK_BOOL_TRUE
        else:
            obj_mask = MASK_BOOL_FALSE
        obj_type = compose_type(CLASS_BOOLEAN, obj_mask)
        self._write_raw([obj_type, ])

    def _write_int(self, obj: int, _) -> None:
        obj_mask = int_mask(obj)
        obj_type = compose_type(CLASS_INT, obj_mask)
        self._write_raw([obj_type, ])
        self._write_raw(serialize_int(obj, obj_mask))

    def _write_float(self, obj: float, _) -> None:
        obj_type = compose_type(CLASS_FLOAT, MASK_FLOAT64)
        self._write_raw([obj_type, ])
        self._write_raw(serialize_float(obj, MASK_FLOAT64))

    def _write_string(self, obj: str, _) -> None:
        raw = obj.encode(self.strings_encoding)
        length = len(raw)
        obj_mask = int_mask(length)
        obj_type = compose_type(CLASS_STRING, obj_mask)
        self._write_raw([obj_type, ])
        self._write_raw(serialize_int(length, obj_mask))
        self._write_raw(raw)

    def _write_table(self, obj: dict, stored_objects: Dict[int, int]) -> None:
        if id(obj) in stored_objects:
            self._write_link(obj, stored_objects)
            return
        stored_objects[id(obj)] = stored_objects[self._COUNT_KEY]
        stored_objects[self._COUNT_KEY] = stored_objects[self._COUNT_KEY] + 1

        size = len(obj)
        obj_mask = int_mask(size)
        obj_type = compose_type(CLASS_TABLE, obj_mask)
        self._write_raw([obj_type, ])
        self._write_raw(serialize_int(size, obj_mask))
        done = 0
        for k, v in obj.items():
            self._write(k, stored_objects)
            self._write(v, stored_objects)
            done += 1

        if done != size:
            err = "table size changed"
            _logger.error(err)
            raise RuntimeError(err)

    def _write_link(self, obj: dict, stored_objects: Dict[Any, int]) -> None:
        link_id = stored_objects[id(obj)]
        obj_mask = int_mask(link_id)
        obj_type = compose_type(CLASS_LINK, obj_mask)
        self._write_raw([obj_type, ])
        self._write_raw(serialize_int(link_id, obj_mask))
