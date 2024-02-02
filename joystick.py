from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget, QStyleFactory
import sys
from enum import Enum
from math import sin, cos, pi

from decorators import logged

class Direction(Enum):
    Left = 0
    Right = 1
    Up = 2
    Down = 3

@logged
class Joystick(QWidget):
    def __init__(self, parent=None):
        super(Joystick, self).__init__(parent)
        self.setMinimumSize(100, 100)
        self.movingOffset = QPointF(0, 0)
        self.grabCenter = False
        self.__maxRadius = 50
        self.angle = 0
        self.radius = 0
        self.X = 0
        self.Y = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        bounds = QRectF(-self.__maxRadius, -self.__maxRadius, self.__maxRadius * 2, self.__maxRadius * 2).translated(self._center())
        painter.drawEllipse(bounds)
        painter.setBrush(Qt.black)
        painter.drawEllipse(self._centerEllipse())

    def _centerEllipse(self):
        if self.grabCenter:
            return QRectF(-20, -20, 40, 40).translated(self.movingOffset)
        return QRectF(-20, -20, 40, 40).translated(self._center())

    def _center(self):
        return QPointF(self.width()/2, self.height()/2)


    def _boundJoystick(self, point):
        limitLine = QLineF(self._center(), point)
        if (limitLine.length() > self.__maxRadius):
            limitLine.setLength(self.__maxRadius)
        return limitLine.p2()

    def joystickDirection(self):
        if not self.grabCenter:
            return 0
        normVector = QLineF(self._center(), self.movingOffset)
        currentRadius = normVector.length()
        angle = normVector.angle()

        radius = min(currentRadius / self.__maxRadius, 1.0)

        radius = int(radius*100)
        angle = int(angle)

        radius = int(radius/10)*10
        angle = int(angle/10)*10

        if 45 <= angle < 135:
            return (Direction.Up, angle, radius)
        elif 135 <= angle < 225:
            return (Direction.Left, angle, radius)
        elif 225 <= angle < 315:
            return (Direction.Down, angle, radius)
        return (Direction.Right, angle, radius)


    def mousePressEvent(self, ev):
        self.grabCenter = self._centerEllipse().contains(ev.pos())
        return super().mousePressEvent(ev)

    def mouseReleaseEvent(self, event):
        self.grabCenter = False
        self.movingOffset = QPointF(0, 0)
        self.update()
        self.angle, self.radius = 0, 0
        self.X, self.Y = 0, 0
        #self.logger.debug("joystick - dropped - {}, {}".format(self.angle, self.radius))

    def mouseMoveEvent(self, event):
        if self.grabCenter:
            self.movingOffset = self._boundJoystick(event.pos())
            self.update()
        _, self.angle, self.radius = self.joystickDirection()
        self.X = (int)(self.radius*cos(self.angle*2*pi/360))
        self.Y = (int)(self.radius*sin(self.angle*2*pi/360))
        #self.logger.debug("joystick - moving - {}, {}".format(self.angle, self.radius))
