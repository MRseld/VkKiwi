import MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout

if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(True)
    w = MainWindow.MainWindow()
    w.resize(200, 100)    
    sys.exit(app.exec_())
    