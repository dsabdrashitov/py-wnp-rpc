from dsa.pywnprpc import OutputPipe
import logging

_logger = logging.getLogger(__name__)


def main():
    pipe_name = r"\\.\pipe\wnprpc_test"
    io = open(pipe_name, "r+b")
    output_pipe = OutputPipe(io)

    # booleans
    output_pipe.write(True)
    output_pipe.write(False)

    # ints
    output_pipe.write(1)
    output_pipe.write(-128)
    output_pipe.write(32767)
    output_pipe.write(-2147483648)
    output_pipe.write(2147483647 * 2147483648 + 2147483647)

    # floats
    output_pipe.write(1.0)
    output_pipe.write(-3.66)

    # None
    output_pipe.write(None)

    io.close()


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
