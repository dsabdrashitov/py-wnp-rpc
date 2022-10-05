from dsa.pywnprpc import InputPipe
import logging

_logger = logging.getLogger(__name__)


def main():
    pipe_name = r"\\.\pipe\wnprpc_test"
    io = open(pipe_name, "r+b")

    input_pipe = InputPipe(io)
    _logger.info(f"input.read() returned {input_pipe.read()}")

    io.close()


if __name__ == "__main__":
    logging.basicConfig()
    _logger.setLevel(logging.DEBUG)
    main()
