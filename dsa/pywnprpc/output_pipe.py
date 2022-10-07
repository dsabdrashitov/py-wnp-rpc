import logging
from typing import Iterable, BinaryIO, Any, Dict
from .pipe_exception import PipeException
from .types import compose_type
from .types import CLASS_VOID
from .types import MASK_VOID

_logger = logging.getLogger(__name__)


class OutputPipe:

    def __init__(self, output_stream: BinaryIO):
        self.output_stream = output_stream
        self.local_functions = None
        self.strings_encoding = "cp1252"  # default windows encoding, since library is for windows named pipes
        self.class_switch = {
            type(None): self._write_void,
        }

    def write(self, obj: Any) -> None:
        try:
            stored_objects = dict()
            count_key = object()
            stored_objects[count_key] = 0
            self._write(obj, stored_objects)
        except OSError as e:
            _logger.error(e)
            raise PipeException()

    def _write(self, obj: Any, stored_objects: Dict[Any, int]) -> None:
        python_type = type(obj)
        if python_type not in self.class_switch:
            err = f"type {python_type} not supported"
            _logger.fatal(err)
            raise TypeError(err)
        write_method = self.class_switch[python_type]
        write_method(obj, stored_objects)

    def _write_raw(self, sequence_of_bytes: Iterable[int]):
        self.output_stream.write(bytes(sequence_of_bytes))

    def _write_void(self, _0, _1):
        obj_type = compose_type(CLASS_VOID, MASK_VOID)
        self._write_raw([obj_type, ])
