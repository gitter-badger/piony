from PyQt5.QtWidgets import QLayout, QWidgetItem
from PyQt5.QtCore import Qt, QPoint, QSize

from piony.gui import logger
from piony.common import ra2xy
from piony.gui.ringsegment import RingSegment


# TODO: replace with namedtuple
## Storage for inscribed layer data
class SegmentWrapper(object):
    def __init__(self, item):
        self.item = item
        self.weight = 1


# Rather SectorStrip, or SectorRing
class PieLayout(QLayout):
    def __init__(self, cfg, r, dr, spacing=0, margin=0, parent=None):
        logger.info('%s init', self.__class__.__qualname__)
        super().__init__(parent)
        self.cfg = cfg
        if parent is not None:
            self.setMargin(margin)
        self.r = r
        self.dr = dr
        self.setSpacing(spacing)
        self.sectors = []

    def R(self):
        return self.r + self.dr

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item, pos=None):
        sw = SegmentWrapper(item)
        if pos:
            self.sectors.insert(pos, sw)
        else:
            self.sectors.append(sw)
        # setDirty()
        # QLayout::invalidate();

    def addWidget(self, widget, pos=None):
        self.addChildWidget(widget)
        self.addItem(QWidgetItem(widget), pos)

    def count(self):
        return len(self.sectors)

    def expandingDirections(self):
        # return QtCore.Qt.Horizontal | QtCore.Qt.Vertical
        return Qt.Orientations()  # Qt.Orientation(0)

    def itemAt(self, index):
        if index >= 0 and index < len(self.sectors):
            return self.sectors[index].item
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.sectors):
            return self.sectors.pop(index)
        return None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, w):
        return w

    # @profile
    def setGeometry(self, rect):     # rect -- w/o margin
        super().setGeometry(rect)
        a = min(rect.width(), rect.height())
        self.r = (0.3 * a) // 2
        self.dr = (0.7 * a) // 2
        self.doLayout(QPoint(rect.width()/2, rect.height()/2))

    def sizeHint(self):
        return QSize(self.R(), self.R())

    def minimumSize(self):
        # size = QSize()
        # for item in self.sectors:
        #     size = size.expandedTo(item.minimumSize())
        # size += QSize(2 * self.margin(), 2 * self.margin())
        # return size
        return QSize(10, 10)

    def doLayout(self, center):
        # WARNING: case of empty list -- len([]) == 0
        a = float(360) / max(1, len(self.sectors))

        for i, wrapper in enumerate(self.sectors):
            item = wrapper.item
            wdg = item.widget()
            sp = self.spacing()  # may be linear or angle

            segment = RingSegment(self.r, a*i + sp/2., self.dr, a - sp)
            x, y = ra2xy(self.r, a*i)
            wdg.setGeometry(segment.geometry(center.x() + x, center.y() - y))
            wdg.gPath = segment.path()
            wdg.gText = segment.text_bbox_scr()
            wdg.setMask(segment.region())
