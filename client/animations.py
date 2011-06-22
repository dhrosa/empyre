from PyQt4.QtCore import pyqtSignal, Qt, pyqtProperty, QObject, QTimer, QPropertyAnimation, QRectF, QPointF, QLineF

from PyQt4.QtGui import QPen, QPainter, QPixmap, QColor

class Animation(QObject):
    updated = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, parent = None):
        super(Animation, self).__init__(parent)

    def start(self):
        raise NotImplementedError()

    def stop(Self):
        raise NotImplementedError()
    
    def paint(self, painter):
        raise NotImplementedError()


class LineAnimation(Animation):
    def __init__(self, x1, y1, x2, y2, color, duration, parent = None):
        super(LineAnimation, self).__init__(parent)
        self.start = QPointF(x1, y1)
        self.end = QPointF(x2, y2)
        self.__pos = self.start
        self.color = color
        self.anim = QPropertyAnimation(self, "pos", self)
        self.anim.setStartValue(self.start)
        self.anim.setEndValue(self.end)
        self.anim.setDuration(duration)
        self.anim.valueChanged.connect(self.updated)
        self.anim.finished.connect(self.finished)

    def getPos(self):
        return self.__pos

    def setPos(self, pos):
        self.__pos = pos

    pos = pyqtProperty("QPointF", getPos, setPos)

    def start(self):
        self.anim.start()

    def stop(self):
        self.anim.stop()

    def paint(self, painter):
        pen = QPen(self.color)
        pen.setWidthF(2.5)
        painter.setPen(pen)
        line = QLineF(self.start, self.pos)
        painter.drawLine(line)
        #draw arrowhead
        a = line.angle()
        l1 = QLineF.fromPolar(25, a - 155)
        l1.translate(self.pos)
        l2 = QLineF.fromPolar(25, a + 155)
        l2.translate(self.pos)
        painter.drawLine(l1)
        painter.drawLine(l2)

class BlinkingAnimation(Animation):
    def __init__(self, pixmap, period, parent = None):
        super(BlinkingAnimation, self).__init__(parent)
        self.pixmap = pixmap
        self.timer = QTimer()
        self.timer.setInterval(period / 2)
        self.timer.timeout.connect(self.toggle)
        self.on = False

    def toggle(self):
        self.on = not self.on
        self.updated.emit()

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def paint(self, painter):
        if self.on:
            painter.drawPixmap(0, 0, self.pixmap)
        

