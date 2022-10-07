from .protocol_exception import ProtocolException
import struct
from typing import Tuple
import logging

_logger = logging.getLogger(__name__)

MASK_BITS = 2
MASK_MAX = (1 << MASK_BITS) - 1  # equals 3
CLASS_BITS = 6
CLASS_MAX = (1 << CLASS_BITS) - 1  # equals 63
TYPE_MAX = (1 << (MASK_BITS + CLASS_BITS)) - 1

MASK_INT8 = 0
MASK_INT16 = 1
MASK_INT32 = 2
MASK_INT64 = 3
MASK_FLOAT32 = MASK_INT32
MASK_FLOAT64 = MASK_INT64
MASK_BOOL_FALSE = 0
MASK_BOOL_TRUE = 1
MASK_VOID = 0

CLASS_VOID = 0
CLASS_BOOLEAN = 1
CLASS_INT = 2
CLASS_FLOAT = 3
CLASS_STRING = 4
CLASS_TABLE = 5
CLASS_LINK = 6  # class for already sent objects
CLASS_FUNCTION = 7


def compose_type(obj_class: int, obj_mask: int) -> int:
    if not((0 <= obj_class) and (obj_class <= CLASS_MAX)):
        err = "obj_class is out of bounds"
        _logger.fatal(err)
        raise ValueError(err)
    if not((0 <= obj_mask) and (obj_mask <= MASK_MAX)):
        err = "obj_mask is out of bounds"
        _logger.fatal(err)
        raise ValueError(err)
    return (obj_class << MASK_BITS) | obj_mask


def decompose_type(obj_type: int) -> Tuple[int, int]:
    if not((0 <= obj_type) and (obj_type <= TYPE_MAX)):
        _logger.error("obj_type is out of bounds")
        raise ProtocolException()
    obj_class = obj_type >> MASK_BITS
    obj_mask = obj_type & MASK_MAX
    return obj_class, obj_mask


def mask_bytes_size(obj_mask: int) -> int:
    if not((0 <= obj_mask) and (obj_mask <= MASK_MAX)):
        _logger.error("obj_mask is out of bounds")
        raise ProtocolException()
    return 1 << obj_mask


def deserialize_int(bytes_arr: bytes) -> int:
    result = int.from_bytes(bytes_arr, 'little', signed=True)
    return result


def deserialize_float(bytes_arr: bytes, mask: int) -> float:
    if mask == MASK_FLOAT64:
        return struct.unpack("<d", bytes_arr)[0]
    elif mask == MASK_FLOAT32:
        return struct.unpack("<f", bytes_arr)[0]
    _logger.error(f"unknown float mask: {mask}")
    raise ProtocolException()
