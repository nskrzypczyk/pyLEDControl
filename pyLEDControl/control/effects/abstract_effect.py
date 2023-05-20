#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from control.adapter.abstract_matrix import AbstractMatrix
from control.effect_message import EffectMessage


class AbstractEffect(ABC):
    @staticmethod
    @abstractmethod
    def run(matrix: AbstractMatrix, effect_message: EffectMessage):
        """Runs the effect"""
        pass
