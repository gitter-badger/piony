#!/usr/bin/env python3
# vim: fileencoding=utf-8

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint

from piony.widget.bud import BudWidget
from piony.hgevent import HGEventMixin


class Window(QtWidgets.QWidget, HGEventMixin):
    def __init__(self, cfg, bud):
        super().__init__()
        self.cfg = cfg

        self.opts = self.cfg['Window']
        self.bud = BudWidget(bud, self.cfg, self)
        self.bM3 = False
        self.bFirstMove = False
        self.ppos = QPoint()
        self.setWnd()
        self.setContent(bud)
        self.resize(self.sizeHint())
        self.centerOnCursor()

    ## --------------
    def setWnd(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        wflags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint
        # if not __debug__:
        #     wflags |= Qt.X11BypassWindowManagerHint
        self.setWindowFlags(wflags)
        self.installEventFilter(self)
        self.setMouseTracking(True)

    def setContent(self, bud):
        if not self.cfg['Window'].getboolean('no_tooltip'):
            QtWidgets.QToolTip.setFont(QtGui.QFont('Ubuntu', 12))
            self.setToolTip('Slice No=1 <i>Click at any empty space to close.</i>')

        # Context menu -- can be used to add new shortcuts "on the fly"
        aQuit = QtWidgets.QAction("E&xit", self, shortcut="Ctrl+Q",
                                  triggered=QtWidgets.QApplication.instance().quit)
        self.addAction(aQuit)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)

    ## --------------
    def sizeHint(self):
        return self.bud.sizeHint()

    def minimumSize(self):
        return self.bud.minimalSize()

    def centerOnCursor(self):
        fg = self.frameGeometry()
        cp = QtGui.QCursor.pos()
        # cp = QtGui.QApplication.desktop().cursor().pos()
        # screen = QtGui.QApplication.desktop().screenNumber(cp)
        # sg = QtGui.QApplication.desktop().screenGeometry(screen)
        fg.moveCenter(cp)
        self.move(fg.topLeft())  # self.setGeometry(fg)

    ## --------------
    def paintEvent(self, e):
        p = QtWidgets.QStylePainter(self)  # p.begin(self)
        self.drawCleanBkgr(p)
        p.end()

    def drawCleanBkgr(self, p):
        p.setPen(Qt.NoPen)
        p.setBrush(QtGui.QColor(0, 0, 0, 0))
        p.drawRect(self.rect())
