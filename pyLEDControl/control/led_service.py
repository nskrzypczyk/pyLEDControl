#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from control.effects.abstract_effect import AbstractEffect
from control.effects.random_dot import RandomDot
from misc.logging import Log


class LedService():
    """
    Used for setting the mode of the Matrix.
    Both, flask and the LedController use the same instance of this class to exchange information since they are in seperate subprocesses. This class acts as a shared object between these two.
    """

    def __init__(self, init_with_default_effect=False) -> None:
        self.log = Log(__class__.__name__)
        self._observers = []
        self._effect: AbstractEffect = RandomDot(
        ).build() if init_with_default_effect else None
        self.effect_changed = False

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, val):
        self._effect = val
        self.effect_changed = True

    def bind(self, callback):
        self.log.debug("Binding function")
        self._observers.append(callback)
