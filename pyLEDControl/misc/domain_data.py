import abc
import dataclasses
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from enum import IntEnum
from typing import Any, Callable, List, Union, Callable
from datetime import datetime, time


"""
Collection of domain specific data structures
"""


class ExecutionMode(IntEnum):
    REAL = 0
    EMULATED = 1


@dataclass_json
@dataclass
class AbstractDataComponent(abc.ABC):
    display_name: str

    @abc.abstractmethod
    def get_validator(self) -> Callable:
        raise NotImplementedError

    @abc.abstractmethod
    def definition_mapper(self, fields: dict) -> dict:
        raise NotImplementedError

    def definition_mapper(self, fields):
        definition = {}
        for v in dir(self):
            if not (
                (v.startswith("__") and v.endswith("__"))
                or v.startswith("_")
                or callable(getattr(self, v))
            ):
                definition[v] = getattr(self, v)
        return definition

    def get_definition(self) -> dict:
        fields: dict = self.__class__.__dict__["__dataclass_fields__"]
        return self.definition_mapper(fields)


@dataclass_json
@dataclass
class IntervalDataComponent(AbstractDataComponent):
    """Container to define upper and lower bounds for numbers like int and float."""

    type = "IntervalDataComponent"
    lower_bound: Union[int, float]
    lower_bound_inclusive: bool
    upper_bound: Union[int, float]
    upper_bound_inclusive: bool

    def get_validator(self):
        def validator(x: Union[int, float]) -> bool:
            check_lower_bound = (
                self.lower_bound <= x
                if self.lower_bound_inclusive
                else self.lower_bound < x
            )
            check_upper_bound = (
                x <= self.upper_bound
                if self.upper_bound_inclusive
                else x < self.upper_bound
            )
            return check_lower_bound and check_upper_bound

        return validator


@dataclass_json
@dataclass
class MultiselectDataComponent(AbstractDataComponent):
    """Container for multi-selection purposes"""

    type = "MultiselectDataComponent"
    strict: bool  # defines whether or not a exception shall be thrown if the incoming list contains a value which is not in the original list
    items: Union[
        List, Callable
    ]  # list of strings or a lambda which will be called to retrieve e.g. most recent info
    _items: Union[List, Callable] = field(init=False, repr=False)

    @property
    def items(self):
        if callable(self._items):
            return self._items()
        return self._items

    @items.setter
    def items(self, new) -> None:
        self._items = new

    def get_validator(self):
        def validator(li: list) -> bool:
            for x in li:
                if x not in self.items:
                    if self.strict:
                        raise ValueError(
                            f"Value {x} is not part of the multiselect list!"
                        )
                    else:
                        return False
            return True

        return validator


@dataclass_json
@dataclass
class SingleselectDataComponent(AbstractDataComponent):
    type = "SingleselectDataComponent"
    items: Union[
        List, Callable
    ]
    _items: Union[List, Callable] = field(init=False, repr=False)

    @property
    def items(self):
        if callable(self._items):
            return self._items()
        return self._items

    @items.setter
    def items(self, newVal) -> None:
        self._items = newVal

    def get_validator(self):
        def validator(li: list) -> bool:
            for x in li:
                if x not in self.items:
                    raise ValueError(
                        f"Value {x} is not part of the singleselect list!")
            return True

        return validator


@dataclass_json
@dataclass
class TimerDataComponent(AbstractDataComponent):
    """Container for timer purposes"""

    display_name: str ="Timer"
    type:str = "TimerDataComponent"
    start: int = 26820  # 7:45 AM
    end:int = 1800 # 0:30 PM
    days: Union[
        List, Callable
    ] = field(default_factory=lambda: ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"])
    enabled: bool = False

    @property
    def days(self):
        if callable(self._days):
            return self._days()
        return self._days

    @days.setter
    def days(self, newVal) -> None:
        self._days = newVal

    def get_validator(self) -> Callable:
        def validator(days: list) -> bool:
            for x in days:
                if x not in self.days:
                    raise ValueError(
                        f"Value {x} is not allowed!")
            return True

        return validator
