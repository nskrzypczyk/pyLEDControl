#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from control.adapter.abstract_matrix import AbstractMatrix
from control.effect_message import EffectMessage


class AbstractEffect(ABC):
    @staticmethod
    def run(matrix: type, effect_message: EffectMessage, conn):
        """Effect definition which will be called by MatrixProcess"""
        pass

    @staticmethod
    def is_terminated(conn):
        """
        Uses a multiprocessing pipe connection to receive a stop signal 
        which should be used to terminate the run() method.
        """
        if conn.poll():
            return conn.recv()
        else:
            return False
