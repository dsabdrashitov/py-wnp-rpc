import logging
from typing import Union
from .duplex_calls import DuplexCalls
from .pipe_exception import PipeException
from .protocol_exception import ProtocolException

_logger = logging.getLogger(__name__)


class RPCClient:

    PIPE_NAME_FORMAT = "\\\\.\\pipe\\%s"

    def __init__(self, name: str):
        pipe_name = self.pipe_address(name)
        self.io = open(pipe_name, "r+b")
        self.calls = DuplexCalls(self.io, self.io, None, self._process_error)

    def set_strings_encoding(self, encoding: str):
        if self.calls is not None:
            self.calls.set_strings_encoding(encoding)

    def active(self) -> bool:
        return self.io is not None

    def root_call(self, *args):
        return self.calls.call_remote_root(*args)

    def close(self) -> None:
        self.calls = None
        if self.io is not None:
            self.io.close()
            self.io = None

    def _process_error(self, err: Union[PipeException, ProtocolException]) -> None:
        self.close()
        raise err

    @staticmethod
    def pipe_address(name: str) -> str:
        return RPCClient.PIPE_NAME_FORMAT % name
