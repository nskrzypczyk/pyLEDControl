#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from dataclasses import dataclass

from control.abstract_effect_options import AbstractEffectOptions


class AbstractEffect(ABC):

    @dataclass
    class Options(AbstractEffectOptions):
        pass

    @staticmethod
    def run(matrix: type, effect_message, conn):
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
