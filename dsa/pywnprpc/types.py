from .protocol_exception import ProtocolException
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


def decompose_type(obj_type: int) -> Tuple[int, int]:
    if not((0 <= obj_type) and (obj_type <= TYPE_MAX)):
        raise ProtocolException()
    obj_class = obj_type >> MASK_BITS
    obj_mask = obj_type & MASK_MAX
    return obj_class, obj_mask
