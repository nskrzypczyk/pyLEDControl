from dataclasses import dataclass
from enum import IntEnum
import abc
from typing import Callable, Union


class ExecutionMode(IntEnum):
    REAL = 0
    EMULATED = 1


class AbstractConstraint(abc.ABC):
    @abc.abstractmethod
    def getvalidator(x) -> Callable:
        raise NotImplementedError


# TODO: create interface for constraints => IFieldConstraint
@dataclass
class IntervalConstraint(AbstractConstraint):
    lower_bound:Union[int,float]
    lower_bound_inclusive:bool
    upper_bound: Union[int,float]
    upper_bound_inclusive:bool

    def get_validator(self):
        def validator(x:Union[int,float]) -> bool:
            # return self.lower_bound<=x<=self.upper_bound
            check_lower_bound = self.lower_bound<=x if self.lower_bound_inclusive else self.lower_bound<x
            check_upper_bound = x<=self.upper_bound if self.upper_bound_inclusive else x<self.upper_bound
            return check_lower_bound and check_upper_bound
        return validator