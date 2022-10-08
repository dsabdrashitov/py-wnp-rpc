from dsa.pywnprpc import DuplexCalls
import logging

_logger = logging.getLogger(__name__)


def main():
    pipe_name = r"\\.\pipe\wnprpc_test"
    io = open(pipe_name, "r+b")

    def process_error(err):
        raise err
    dc = DuplexCalls(io, io, None, process_error)

    print(dc._make_call(0, ("hello", 3.14, None, False)))

    io.close()


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
