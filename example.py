import dsa.pywnprpc as wnprpc
import logging

_logger = logging.getLogger(__name__)


def main():
    _logger.info(wnprpc)


if __name__ == "__main__":
    logging.basicConfig()
    _logger.setLevel(logging.DEBUG)
    main()
