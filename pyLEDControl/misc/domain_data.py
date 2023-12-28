import abc
import dataclasses
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Callable, Union


"""
Collection of domain specific data structures
"""

class ExecutionMode(IntEnum):
    REAL = 0
    EMULATED = 1

@dataclass
class AbstractConstraint(abc.ABC):
    display_name: str
    @abc.abstractmethod
    def get_validator(self) -> Callable:
        raise NotImplementedError

    @abc.abstractmethod
    def definition_mapper(self, fields:dict) -> dict:
        raise NotImplementedError
    
    def definition_mapper(self, fields):
        definition = {}
        for v in dir(self):
            if not ((v.startswith("__") and v.endswith("__") or v.startswith("_")) or callable(getattr(self, v))):
                definition[v] = getattr(self, v)
        return definition

    def get_definition(self) -> dict:
        fields:dict = self.__class__.__dict__["__dataclass_fields__"]
        return self.definition_mapper(fields)

@dataclass
class IntervalConstraint(AbstractConstraint):
    """Constraint to define upper and lower bounds for numbers like int and float."""
    type = "IntervalConstraint"
    lower_bound: Union[int, float]
    lower_bound_inclusive: bool
    upper_bound: Union[int, float]
    upper_bound_inclusive: bool

    def get_validator(self):
        def validator(x: Union[int, float]) -> bool:
            check_lower_bound = self.lower_bound <= x if self.lower_bound_inclusive else self.lower_bound < x
            check_upper_bound = x <= self.upper_bound if self.upper_bound_inclusive else x < self.upper_bound
            return check_lower_bound and check_upper_bound
        return validator
    
@dataclass
class MultiselectConstraint(AbstractConstraint):
    """Constraint for multi-selection purposes"""
    type = "MultiselectConstraint"
    items:list # list of strings
    strict:bool # defines whether or not a exception shall be thrown if the incoming list contains a value which is not in the original list

    def get_validator(self):
        def validator(li:list) -> bool:
            for x in li:
                if x not in self.items:
                    if self.strict:
                        raise ValueError(f"Value {x} is not part of the multiselect list!")
                    else:
                        return False
            return True
        return validator
    
@dataclass
class SingleselectConstraint(AbstractConstraint):
    type = "SingleselectConstraint"
    items: list 
    
    def get_validator(self):
        def validator(li:list) -> bool:
            for x in li:
                if x not in self.items:
                    raise ValueError(f"Value {x} is not part of the multiselect list!")
            return True
        return validator
