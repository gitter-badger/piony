#!/usr/bin/env python3
# vim: fileencoding=utf-8

import sys
import yaml
import logging.config
from piony.common import expand_pj

G_LOG_PATH = ':/cfgs/log.yml'
with open(expand_pj(G_LOG_PATH), 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))


if __name__ == '__main__':

    ## Send args to listener and close
    from piony.system.client import Client
    client = Client()
    client.connect()
    if client.socket.waitForConnected(2000):
        # DEV: send also [0] element -- to use client pwd for pathes in cmdline
        client.send(sys.argv[1:])
        client.socket.close()

    else:
        from signal import signal, SIGINT, SIG_DFL
        ## Close on 'Ctrl-C' system signal.
        ## WARNING: No cleanup possible (can't implement because of Qt).
        signal(SIGINT, SIG_DFL)

        import inject
        from piony.gstate import GState

        def config(binder):
            binder.bind(GState, GState(sys.argv))
        inject.configure(config)

        from PyQt5.QtWidgets import QApplication
        from piony.main import MainApplication
        app = QApplication(sys.argv)
        main = MainApplication()
        sys.exit(app.exec_())
