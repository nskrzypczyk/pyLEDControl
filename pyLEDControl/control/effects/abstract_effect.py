#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from dataclasses import dataclass
from typing import Union

from control.abstract_effect_options import AbstractEffectOptions


class AbstractEffect(ABC):

    @dataclass
    class Options(AbstractEffectOptions):
        pass

    @staticmethod
    def run(matrix: type, effect_message, conn, *args, **kwargs):
        """Effect definition which will be called by MatrixProcess"""
        pass

    @staticmethod
    def is_terminated(conn) -> bool:
        """
        Uses a multiprocessing pipe connection to receive a stop signal
        which should be used to terminate the run() method.
        """
        if conn.poll():
            pipe_data = conn.recv()
            if isinstance(pipe_data,bool):
                return pipe_data
            else:
                return False
        else:
            return False

    @staticmethod
    def get_new_options(conn) -> Union[None, AbstractEffectOptions]:
        """
        Uses a multiprocessing pipe connection to receive updated effect related options. 
        """
        if conn.poll():
            pipe_data = conn.recv()
            if isinstance(pipe_data, AbstractEffectOptions):
                return pipe_data
        else:
            return None