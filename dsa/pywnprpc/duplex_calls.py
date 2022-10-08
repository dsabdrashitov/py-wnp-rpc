import logging
from typing import Any, BinaryIO, Callable, Union
from .input_pipe import InputPipe
from .output_pipe import OutputPipe
from .local_functions import LocalFunctions
from .remote_functions import RemoteFunctions
from .protocol_exception import ProtocolException
from .pipe_exception import PipeException
from .remote_error import RemoteError

_logger = logging.getLogger(__name__)


class DuplexCalls:

    def __init__(self, input_stream: BinaryIO, output_stream: BinaryIO, root_function: Union[Callable, None],
                 process_error: Callable[[Union[PipeException, ProtocolException]], Any]):
        self.input_pipe = InputPipe(input_stream)
        self.output_pipe = OutputPipe(output_stream)

        self.process_error = process_error

        self.local_functions = LocalFunctions(root_function)
        self.output_pipe.set_local_functions(self.local_functions)

        self.remote_functions = RemoteFunctions(self._make_call)
        self.input_pipe.set_remote_functions(self.remote_functions)

    def _make_call(self, func_id: int, args: tuple) -> Any:
        self._pcall(self._send_request, (func_id, args))
        return self._pcall(self._receive_reply, tuple())

    def _send_request(self, func_id: int, args: tuple):
        args_count = len(args)
        # Positive - arguments count, negative - returns count, zero - error
        self.output_pipe.write(1 + args_count)
        self.output_pipe.write(func_id)
        for i in range(args_count):
            self.output_pipe.write(args[i])

    def _receive_reply(self):
        while True:
            # Positive - arguments count, negative - returns count, zero - error
            header = self.input_pipe.read()
            if not isinstance(header, int):
                _logger.error("header is not int")
                raise ProtocolException()
            if header > 0:
                self._read_request(header - 1)
            elif header < 0:
                rets_count = -header - 1
                if rets_count == 0:
                    return
                rets = []
                for _ in range(rets_count):
                    rets.append(self.input_pipe.read())
                if rets_count == 1:
                    return rets[0]
                else:
                    return tuple(rets)
            else:
                err = self.input_pipe.read()
                raise RemoteError(err)

    def _read_request(self, args_count: int) -> None:
        func_id = self.input_pipe.read()
        if not isinstance(func_id, int):
            _logger.error("func_id is not int")
            raise ProtocolException()
        args = []
        for _ in range(args_count):
            args.append(self.input_pipe.read())

        func = self.local_functions.get_function(func_id)
        if func is None:
            self._send_error(f"no function with id {func_id}")
            return

        try:
            result = func(*args)
        except Exception as e:
            self._send_error(e)
            return
        self._send_results(result)

    def _send_error(self, err: Any) -> None:
        self.output_pipe.write(0)
        self.output_pipe.write(str(err))

    def _send_results(self, result: Union[Any, tuple]) -> None:
        if result is None:
            result = []
        if not isinstance(result, tuple):
            result = [result, ]
        self.output_pipe.write(-len(result) - 1)
        for i in range(len(result)):
            self.output_pipe.write(result[i])

    def _pcall(self, func: Callable, args: tuple) -> Any:
        try:
            return func(*args)
        except (PipeException, ProtocolException) as e:
            if self.process_error is not None:
                return self.process_error(e)
            else:
                raise e
