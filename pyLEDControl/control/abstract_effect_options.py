#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import abc
from dataclasses import dataclass, fields
from misc.domain_data import IntervalConstraint, SingleselectConstraint


# TODO: REFACTORING / INVESTIGATION: replace regular variables with new classes like e.g. "MultiselectOption" which contains attributes like "display_name" (for frontend), "constraint" etc. That will simplify parsing in the frontend.

@dataclass
class AbstractEffectOptions(abc.ABC):
    """ Definition of effect related options.
        - Naming convention for constraints:
            - {attribute_name}_constraint
        - Currently only one optional constraint per attribute!
    """
    br_file_path = "brightness.txt"
    brightness: int
    effect: type

    brightness_constraint = IntervalConstraint(
        "Brightness", 0, True, 100, True)
    # TODO: Dont make this hard coded
    effect_constraint = SingleselectConstraint("Effect", ["DigiClock",
                                                          "GameOfLife",
                                                          "OFF",
                                                          "RainbowWave",
                                                          "RandomDot",
                                                          "Spotify",
                                                          "Wave",
                                                          "Weather",
                                                          "Shuffle"])
    
    def __post_init__(self):
        self.set_brightness(self.brightness)

    def __eq__(self, other):
        if isinstance(other, AbstractEffectOptions):
            return hash(self) == hash(other)
        return False
    
    def __hash__(self):
        return hash(self.to_dict())

    def set_brightness(self, br: int) -> None:
        with open(self.br_file_path, "w") as f:
            f.write(str(br))

    def get_brightness(self) -> float:
        self.brightness = int(open(self.br_file_path, "r").read())
        return self.brightness / 100

    def to_dict(self) -> str:
        field_values = {}
        for field in fields(self):
            if not field.metadata.get("static", False):
                field_name = field.name
                field_value = getattr(self, field_name)
                if not isinstance(field_value, type):
                    field_values[field_name] = field_value
                else:
                    field_values[field_name] = self.__dict__[field_name].__name__
        return field_values