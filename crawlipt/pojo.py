import json
from typing import Any

from crawlipt.annotation import check


class VariableBase:

    @check
    def get(self, key: str) -> Any:
        raise NotImplementedError

    @check(exclude="value")
    def set(self, key: str, value: Any) -> Any:
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

    @check(exclude="value")
    def set(self, key: str, value: Any):
        self.values[key] = value

    @check
    def __contains__(self, key: str):
        return key in self.values


class VariableError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
