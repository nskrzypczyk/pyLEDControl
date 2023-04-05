#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from control.adapter.abstract_matrix import AbstractMatrix


class AbstractEffect(ABC):
    @staticmethod
    @abstractmethod
    def run(matrix: AbstractMatrix):
        """Runs the effect"""
        pass
