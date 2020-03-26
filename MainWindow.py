import LoginWindow
import GuiWidgets
from PyQt5.QtCore import QThread, QTimer
from PyQt5 import QtWidgets 
from PyQt5 import QtGui
from PyQt5 import QtCore
import settings
import ApiCalls
        
class MyTableWidget(QtWidgets.QWidget):
    
    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)   
        self.tabs = QtWidgets.QTabWidget()

        self.dialoglist= GuiWidgets.DialogListWidget(self)

        self.dialogtab =QtWidgets.QWidget()
        self.tabs.addTab(self.dialogtab,"Диалоги")
        self.dialogtab.layout = QtWidgets.QVBoxLayout(self)

        self.dialogtab.layout.addWidget(self.dialoglist)

        self.dialogtab.setLayout(self.dialogtab.layout)       
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check)
        self.logged=False
        self.setWindowTitle("VkKivi")
        self.setGeometry(300, 300, 800, 600)
        self.window=LoginWindow.LoginDialog()
        if(self.logged==False):
            self.window.show()
            self.timer.start(300)   
        else:
            self.show()
   
       
    def initUi(self):
        self.mainLayout=QtWidgets.QVBoxLayout()
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
    
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
  
        self.menu = QtWidgets.QMenu(self)
      

        action1 = self.menu.addAction('закрыть')
        action1.triggered.connect(self.close)


  
    def show_context_menu(self, point):
        self.menu.exec(self.mapToGlobal(point))

    def showWidnow(self):
        self.initUi()
        self.show()
        self.resize(500,500)

    def check(self):
        if self.window.auth==True:
            self.timer.stop()
            self.window.hide()
            self.window.deleteLater()
            self.showWidnow()
            
           
            