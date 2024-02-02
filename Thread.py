from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

class ThreadSignals(QtCore.QObject):
    finished = QtCore.pyqtSignal()

class Thread(QtCore.QRunnable):

    def __init__(self, fn, *args, **kwargs):
        QtCore.QRunnable.__init__(self)
        self.fn = fn
        self.signals = ThreadSignals()
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn()
        self.signals.finished.emit()