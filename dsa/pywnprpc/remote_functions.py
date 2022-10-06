import logging
from typing import Callable, Any, Tuple

_logger = logging.getLogger(__name__)


class RemoteFunctions:

    def __init__(self, make_call: Callable[[int, Tuple], Any]):
        self.make_call = make_call
        self.id2function = dict()

    def get_function(self, func_id: int) -> Callable:
        # TODO: implement
        _logger.warning(f"This is only stub. func_id={func_id}")
        return lambda: None
