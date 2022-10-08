import logging

_logger = logging.getLogger(__name__)


class DictAsAKey:

    def __init__(self, d: dict):
        self.d = d

    def get_dict(self) -> dict:
        return self.d

    def __eq__(self, other):
        if not hasattr(other, "d"):
            return False
        return self.d is other.d

    def __hash__(self):
        return hash(id(self.d))

    def __repr__(self):
        return f"DictAsAKey({id(self.d)})"
