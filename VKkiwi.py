# -*- coding: utf-8 -*-
import MainWindow
from PySide2.QtWidgets import QApplication
import  tools
if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(True)
    w = MainWindow.MainWindow()
    w.resize(200, 100)
    app.exec_()
