#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from misc.logging import Log
from server.server import run_server
from multiprocessing import Process
import time


def main():
    log = Log(__name__)
    log.debug("Starting the application")
    server_proc: Process = Process(target=run_server)
    server_proc.start()

    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        server_proc.terminate()


if __name__ == "__main__":
    main()
