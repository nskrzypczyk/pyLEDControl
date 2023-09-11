#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix


class AbstractEffect(ABC):
    class Options(AbstractEffectOptions):
        pass

    @staticmethod
    def run(matrix: type, effect_message: Options, conn):
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
