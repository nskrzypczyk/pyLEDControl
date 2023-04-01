#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from control.effects.abstract_effect import AbstractEffect
from control.effects.random_dot import RandomDot
from dataclasses import dataclass


class EffectMessage():
    effect_dict = {
        "RandomDot": RandomDot
    }
    effect: AbstractEffect
    effect_changed: bool

    def set_effect(self, effect: AbstractEffect | str) -> EffectMessage:
        if isinstance(effect, str):
            self.effect = EffectMessage.effect_dict[effect]
        else:
            self.effect = effect
        return self

    def set_effect_changed(self, changed: bool) -> EffectMessage:
        self.effect_changed = changed
        return self
