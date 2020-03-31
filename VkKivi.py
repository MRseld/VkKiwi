import MainWindow
import sys
import settings
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(True)
    w = MainWindow.MainWindow()
    w.resize(200, 100)    
    app.exec_()