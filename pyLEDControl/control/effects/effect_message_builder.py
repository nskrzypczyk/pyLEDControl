from __future__ import annotations
from typing import Union
from control.effects import effect_dict
from control.abstract_effect_options import AbstractEffectOptions


class EffectMessageBuilder:
    def __init__(self) -> None:
        self.msg = AbstractEffectOptions()

    def set_effect(self, effect: Union[type, str]) -> EffectMessageBuilder:
        if isinstance(effect, str):
            self.msg.effect = effect_dict[effect]
        else:
            self.msg.effect = effect
        return self

    def set_brightness(self, brightness: int) -> EffectMessageBuilder:
        self.msg.brightness = brightness
        self.msg.set_brightness(brightness)
        return self

    def build(self):
        return self.msg
