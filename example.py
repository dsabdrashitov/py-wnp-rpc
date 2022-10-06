from dsa.pywnprpc import InputPipe
import logging

_logger = logging.getLogger(__name__)


def main():
    pipe_name = r"\\.\pipe\wnprpc_test"
    io = open(pipe_name, "r+b")
    input_pipe = InputPipe(io)

    while True:
        obj = input_pipe.read()
        _logger.info(f"input.read() returned {obj}")
        if isinstance(obj, dict) and ("self" in obj):
            _logger.debug(f"dict has recursion: dict['self']={obj['self']}")
        if obj is None:
            break

    io.close()


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
