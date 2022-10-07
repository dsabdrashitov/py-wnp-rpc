from dsa.pywnprpc import InputPipe, RemoteFunctions
import logging

_logger = logging.getLogger(__name__)


def main():
    pipe_name = r"\\.\pipe\wnprpc_test"
    io = open(pipe_name, "r+b")
    input_pipe = InputPipe(io)

    def make_call(func_id, args):
        _logger.debug(f"Stub for remote function {func_id} was called with args={args}")
        return True
    input_pipe.set_remote_functions(RemoteFunctions(make_call))

    while True:
        obj = input_pipe.read()
        _logger.info(f"input.read() returned {obj}")
        if isinstance(obj, dict) and ("self" in obj):
            _logger.debug(f"dict has recursion: dict['self']={obj['self']}")
        if callable(obj):
            _logger.debug(f"call to remote function returned: {obj(1, False, 'hello')}")
        if obj is None:
            break

    io.close()


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
