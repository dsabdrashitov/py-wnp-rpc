from dsa.pywnprpc import RPCClient, RemoteError
import logging

_logger = logging.getLogger(__name__)

NAME = "wnprpc_test"


def main():
    client = RPCClient(NAME)
    _logger.info(client.active())

    try:
        client.root_call("wrong password")
        raise AssertionError("previous line had to throw RemoteError")
    except RemoteError as e:
        # This is ok
        _logger.error(e)

    func_dict = client.root_call("password")
    _logger.info(func_dict)

    func_print = func_dict["print"]
    func_error = func_dict["error"]
    func_stop = func_dict["stop"]

    _logger.info(func_print(1, False, None, 3.66, {"a": "b"}))

    try:
        func_error("this error should return as RemoteError")
        raise AssertionError("previous line had to throw RemoteError")
    except RemoteError as e:
        # This is ok
        _logger.error(e)

    func_stop()

    client.close()
    _logger.info(client.active())


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
