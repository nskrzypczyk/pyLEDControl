#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from control.effects.abstract_effect import AbstractEffect
from pyLEDControl.control.effects.random_dot import RandomDot


class LedService():
    """
    Used for setting the mode of the Matrix.
    Both, flask and the LedController use the same instance of this class to exchange information since they are in seperate subprocesses. This class acts as a shared object between these two.
    """

    def __init__(self, init_with_default_effect=False) -> None:
        self.effect: AbstractEffect = RandomDot.build() if init_with_default_effect else None
