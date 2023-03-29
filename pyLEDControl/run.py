#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from misc.logging import Log
from multiprocessing import Process
import time
from server.server import Server
from control.led_controller import LedController
from control.led_service import LedService


def main():
    log = Log(__name__)
    log.debug("Starting the application")

    led_service = LedService(True)

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


if __name__ == "__main__":
    main()
