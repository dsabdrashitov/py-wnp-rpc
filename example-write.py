from dsa.pywnprpc import OutputPipe, LocalFunctions
import logging

_logger = logging.getLogger(__name__)


def main():
    pipe_name = r"\\.\pipe\wnprpc_test"
    io = open(pipe_name, "r+b")
    output_pipe = OutputPipe(io)
    output_pipe.set_local_functions(LocalFunctions())

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

    # strings
    output_pipe.write("Hell\no, Lua!")

    # dicts and functions
    table = {
        "a": 1,
        True: False,
        3.66: lambda: None,
        (lambda: None): "some value"
    }
    table["self"] = table
    output_pipe.write(table)

    # None
    output_pipe.write(None)

    io.close()


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
