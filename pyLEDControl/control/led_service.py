#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from control.effects.abstract_effect import AbstractEffect
from control.effects.random_dot import RandomDot


class LedService():
    """
    Used for setting the mode of the Matrix.
    Both, flask and the LedController use the same instance of this class to exchange information since they are in seperate subprocesses. This class acts as a shared object between these two.
    """

    __instance = None

    @staticmethod
    def instance():
        if LedService.__instance == None:
            LedService()
        return LedService.__instance

    def __init__(self, init_with_default_effect=False) -> None:

        if LedService.__instance != None:
            raise Exception(f"{__class__.__name__} already has an instance!")
        else:
            LedService.__instance = self
            self.effect_dict = {
                "RandomDot": RandomDot
            }
            self._effect: AbstractEffect = None
            self.effect_changed = False

    def val(self):
        return self

    @property
    def effect(self) -> AbstractEffect:
        return self._effect

    @effect.setter
    def effect(self, val: AbstractEffect):
        self._effect = val()
        self._effect.build()
        self.effect_changed = True
