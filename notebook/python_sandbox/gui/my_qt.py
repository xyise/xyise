import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsView,
    QLabel, QApplication, QGraphicsScene, QGraphicsRectItem, QAction, qApp, QLineEdit, QSplitter, QFrame, QGraphicsWidget, QGraphicsItem, QComboBox, QPushButton, QSlider, QDesktopWidget)
from PyQt5.QtGui import QPixmap, QIcon, QDragEnterEvent, QDragLeaveEvent, QMouseEvent, QDrag, QDropEvent, QPaintEvent, QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QMimeData, QObject, pyqtSignal, QBasicTimer, QTimerEvent, QRectF
import pyqtgraph as pg
import numpy as np

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout()

        lbl = QLabel(self)
        lbl.setText('My Text Label')
        hbox.addWidget(lbl)

        pw = (pg.PlotWidget())
        hbox.addWidget(pw)

        p1 = pw.plotItem
        p1.setTitle('This is Title')
        p1.setLabels(left='axis 1')

        p1.plot([1,2,3,4,8,16,32])
        p1.addItem(pg.PlotCurveItem([10,20,30], pen='b'))

        p2 = pg.ViewBox()
        p1.showAxis('right')
        p1_s = (QGraphicsScene)(p1.scene())
        p1_s.addItem(p2)
        p1.getAxis('right').linkToView(p2)
        p2.setXLink(p1)
        p1.getAxis('right').setLabel('axis 2', color='#0000ff')

        p2.addItem(pg.PlotCurveItem([3200, 1600], pen='b'))

        p1vb = (QGraphicsWidget)(p1.vb)
        p1vb.sceneBoundingRect()

        pg.GraphicsWidget

        self.setLayout(hbox)

        self.show()


def run():
    app = QApplication([])
    e = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':

    run()
