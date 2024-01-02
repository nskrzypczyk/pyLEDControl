from multiprocessing.managers import BaseManager
import time
from multiprocessing import Pipe, Process, Queue
from multiprocessing.managers import NamespaceProxy, BaseProxy
import types

from control.abstract_effect_options import AbstractEffectOptions
from control.adapter.abstract_matrix import AbstractMatrix
from control.adapter.real_matrix import RealMatrix
from control.effects.abstract_effect import AbstractEffect
from misc.logging import Log

class SharedOptionsManager(BaseManager):
    pass

def build_proxy_class(target):
    """ It is necessary to expose all methods and attributes """
    def __getattr__(self, key):
        result = self._callmethod('__getattribute__', (key,))
        if isinstance(result, types.MethodType):
            def wrapper(*args, **kwargs):
                return self._callmethod(key, args, kwargs)
            return wrapper
        return result
    dic = {'types': types, '__getattr__': __getattr__}
    proxy_name = target.__name__ + "Proxy"
    ProxyType = type(proxy_name, (NamespaceProxy,), dic)
    ProxyType._exposed_ = tuple(dir(target))
    return ProxyType

class MatrixProcess:
    def __init__(self, matrix: AbstractMatrix) -> None:
        self.matrix = matrix
        self.log: Log = Log("MatrixProcesss")

    def loop(self, matrix, queue: Queue):
        proc: Process = None
        current_options: AbstractEffectOptions = None
        while 1:
            try:
                if queue.empty():
                    self.log.info("Queue is empty")
                else:
                    queue_data = queue.get(block=False) # get effect and corresponding options from queue
                    effect_class: AbstractEffect = queue_data[0]
                    options: AbstractEffectOptions = queue_data[1]
                    if current_options is None or (options.effect != current_options.effect): # if the effect changes
                        self.log.debug(
                            "Effect has changed. Restarting process")

                        if proc:
                            conn_p.send(True) # send kill signal to current effect
                            proc.join() # wait for termination of current effect

                        # create new pipes
                        conn_p, conn_c = Pipe(True)
                        OptionProxy = build_proxy_class(options.__class__)
                        SharedOptionsManager.register(options.__class__.__name__, options.__class__.init_with_instance, OptionProxy)
                        options_mgr = SharedOptionsManager()
                        options_mgr.start()
                        shared_options = options_mgr.Options(options)
                        # create and start new effect process
                        proc = Process(
                            target=effect_class.run, args=[
                                matrix, shared_options, conn_c
                            ]
                        )
                        proc.start()

                        current_options = options
                    elif options != current_options: # if just the options changed
                        shared_options.update_instance(options) # send new options via shared object to current effect
                        options_mgr.connect()
                        current_options = options
                time.sleep(1)
            except KeyboardInterrupt:
                self.log.debug("Terminating")

    def run(self, queue: Queue):
        self.log.debug("run method called.")
        self.loop(self.matrix, queue)
