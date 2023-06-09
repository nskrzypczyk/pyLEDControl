#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from misc.logging import Log
from multiprocessing import Queue
import time
from server.server import Server
from control.led_controller import LedController


def main():
    log = Log(__name__)
    log.debug("Starting the application")

    queue = Queue()
    server_proc = Server(queue=queue)
    server_proc.start()
    led_controller = LedController(queue=queue)
    led_controller_proc = led_controller.start()

    try:
        while 1:
            time.sleep(3600)
    except KeyboardInterrupt:
        server_proc.terminate()
        led_controller_proc.terminate()


if __name__ == "__main__":
    main()
