#!/usr/bin/env python3
# vim: fileencoding=utf-8

import os
import sys
import signal
from PyQt5.QtWidgets import QApplication

import piony


if __name__ == '__main__':
    cdir = os.path.dirname(os.path.abspath(__file__))
    Cfg_Ps = piony.ConfigParser()
    Arg_Ps = piony.ArgsParser()

    cfg = Cfg_Ps.read_file()
    args = Arg_Ps.parse()
    Arg_Ps.apply(args)
    bud = piony.ProfileParser().read_file()

    # mmc.read(os.path.abspath(args.input))
    # for f_out in args.output:
    #     mmc.write(os.path.abspath(f_out))
    # mmc.write('out.stdio', type=None if 'auto' == args.oftype else args.oftype)

    ## Close on 'Ctrl-C' system signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    wnd = piony.Window(cfg, bud, args)
    wnd.setWindowTitle(piony.__appname__)
    wnd.show()
    sys.exit(app.exec_())
