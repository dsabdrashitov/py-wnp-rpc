import logging
from typing import Callable, Optional

_logger = logging.getLogger(__name__)


class LocalFunctions:

    def __init__(self, root_function: Optional[Callable] = None):
        self.function2id = {}
        self.id2function = {}
        if root_function is not None:
            self.function2id[root_function] = 0
        self.id2function[0] = root_function
        self.registered = 0

    def get_function(self, func_id: int) -> Callable:
        return self.id2function[func_id]

    def get_id(self, func: Callable) -> int:
        if func not in self.function2id:
            self.registered = self.registered + 1
            self.function2id[func] = self.registered
            self.id2function[self.registered] = func
        return self.function2id[func]
