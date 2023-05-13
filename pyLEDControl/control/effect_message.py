#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import sys
from control.effects.abstract_effect import AbstractEffect

effects = "control.effects"
__import__(effects)
effect_list = sys.modules[effects]


class EffectMessage:
    effect_dict = {
        name: obj for name, obj in effect_list.__dict__.items() if isinstance(obj, type)
    }
    effect: AbstractEffect
    brightness: int

    def set_effect(self, effect: AbstractEffect | str) -> EffectMessage:
        if isinstance(effect, str):
            self.effect = EffectMessage.effect_dict[effect]
        else:
            self.effect = effect
        return self

    def set_brightness(self, brightness: int) -> EffectMessage:
        self.brightness = brightness
