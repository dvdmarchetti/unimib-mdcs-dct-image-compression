from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QLabel, QWidget


class ResizableAspectRatioLabel(QLabel):
    def __init__(self, parent=None):
        super(ResizableAspectRatioLabel, self).__init__(parent)
        self.parent = parent
        self.scale = False
        self.pixmap = QPixmap()

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        self.repaint()

    def setShouldScale(self, shouldScale):
        self.scale = shouldScale
        self.repaint()

    def paintEvent(self, event):
        if self.pixmap != None and (not self.pixmap.isNull()):
            size = self.size()
            painter = QPainter(self)
            point = QPoint(0,0)

            scaledPix = self.pixmap.scaled(size, Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation) if self.scale else self.pixmap

            point.setX((size.width() - scaledPix.width())/2)
            point.setY((size.height() - scaledPix.height())/2)

            painter.drawPixmap(point, scaledPix)
        super().paintEvent(event)
