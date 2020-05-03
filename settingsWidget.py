# -*- coding: utf-8 -*-
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore


class SetttingsWidget(QtWidgets.QWidget):
    def __init__(self, parent, ):
        super(SetttingsWidget, self).__init__(parent)
        self.v = QtWidgets.QVBoxLayout()
        self.setLayout(self.v)
        self.lab = QtWidgets.QLabel("Настройки")
        self.v.addWidget(self.lab)
