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

    @check
    def set(self, method: str, value: Any):
        pass


class Store(StoreBase):

    def __init__(self, is_replace=False):
        """
        :param is_replace: need replace the value of method or not
        """
        self.is_replace = is_replace
        self.data = {}

    @check
    def set(self, method: str, value: Any) -> None:
        if method in self.data.keys():
            if self.is_replace:
                self.data[method] = value
            else:
                self.data[method].append(value)
            return
        if self.is_replace:
            self.data[method] = value
        else:
            self.data[method] = [value]
