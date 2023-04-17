#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from control.effects.abstract_effect import AbstractEffect
from control.effects import RandomDot, Wave, RainbowWave, DigiClock


class EffectMessage():
    effect_dict = {
        "RandomDot": RandomDot,
        "Wave": Wave,
        "RainbowWave": RainbowWave,
        "DigiClock": DigiClock
    }
    effect: AbstractEffect

    def set_effect(self, effect: AbstractEffect | str) -> EffectMessage:
        if isinstance(effect, str):
            self.effect = EffectMessage.effect_dict[effect]
        else:
            self.effect = effect
        return self
