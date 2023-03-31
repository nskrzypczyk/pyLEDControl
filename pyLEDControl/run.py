#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from misc.logging import Log
import multiprocessing.managers
from multiprocessing import Value, Manager, Queue
import time
from server.server import Server
from control.led_controller import LedController
from control.led_service import LedService
from misc.data_manager import DataManager


def main():
    log = Log(__name__)
    log.debug("Starting the application")

    DataManager.register("LedService", LedService)
    with DataManager() as manager:
        led_service: multiprocessing.managers.pro = manager.LedService()
        print(led_service.val().effect)
        server_proc = Server(service=led_service)
        server_proc.start()
        led_controller = LedController(service=led_service)
        led_controller_proc = led_controller.start()

        try:
            while 1:
                time.sleep(1)
        except KeyboardInterrupt:
            server_proc.terminate()
            led_controller_proc.terminate()
            manager.close()


if __name__ == "__main__":
    main()
