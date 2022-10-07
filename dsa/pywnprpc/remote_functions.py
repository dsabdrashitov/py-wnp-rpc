import logging
from typing import Callable, Any, Tuple

_logger = logging.getLogger(__name__)


class RemoteFunctions:

    def __init__(self, make_call: Callable[[int, Tuple], Any]):
        self.make_call = make_call
        self.id2function = dict()

    def get_function(self, func_id: int) -> Callable:
        if func_id in self.id2function:
            return self.id2function[func_id]

        def func(*args):
            return self.make_call(func_id, args)

        self.id2function[func_id] = func
        return func
