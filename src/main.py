#!/usr/bin/env python3

import signal
from core.Core import Core

def service_shutdown(signum, frame):
    print('Deteniendo el proceso (%d)' % signum)
    raise Exception()


def main():
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    try:
        core = Core()
        core.start()
    except Exception:
        core.shutdown_flag.set()
        core.join()
        exit(0)
