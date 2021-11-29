#!/usr/bin/env python3

import signal
from core.Core import Core

def service_shutdown(signum, frame):
    """
    Intento de ontrolar señales
    """
    print('Deteniendo el proceso (%d)' % signum)
    raise Exception()


def main():
    """
    Función principal que inicia el programa
    """
    signal.signal(signal.SIGTERM, service_shutdown)
    signal.signal(signal.SIGINT, service_shutdown)
    try:
        while True:
            core = Core()
            core.start()
            print('inicio')

    except Exception:
        core.shutdown_flag.set()
        core.join()
        exit(0)


if __name__=='__main__':
    main()
