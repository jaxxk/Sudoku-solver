from tkinter import *
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui

import cv2
import numpy as np
import sys

class screenCap(QtWidgets.QWidget):
    img = None
    root = None

    def __init__(self):
        super().__init__()
        self.root = Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()

    def getImg(self):
        return self.img


    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()


    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()


    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        #self.root.destroy()
        #self.img = cv2.cvtColor(np.array(self.img), cv2.COLOR_BGR2RGB)


    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))


# Testing
if __name__ == '__main__':
    cap = QtWidgets.QApplication(sys.argv)
    window = screenCap()
    window.show()
    cap.aboutToQuit.connect(cap.deleteLater)
    cap.exec()
    img = window.getImg()
    cv2.imshow('Captured Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
