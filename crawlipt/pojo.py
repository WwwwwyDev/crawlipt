import json
from typing import Any

from crawlipt.annotation import check


class VariableBase:
    """
    This is a interface class for the variable.
    """

    @check
    def get(self, key: str) -> Any:
        raise NotImplementedError


    @check
    def __contains__(self, key: str):
        raise NotImplementedError


class Variable(VariableBase):
    @check
    def __init__(self, values: dict | str):
        if isinstance(values, str):
            values: dict = json.load(values)
        self.values = values

    @check
    def get(self, key: str) -> Any:
        return self.values.get(key)


    @check
    def __contains__(self, key: str):
        return key in self.values


class StoreBase:
    """
    This is a interface class for the store.
    """