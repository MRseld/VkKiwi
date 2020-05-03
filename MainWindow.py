# -*- coding: utf-8 -*-
from threading import Thread

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtCore import QTimer

import AudioListWidget
import DialogListWidget
import DialogWidget
import LoginWindow
import settings
import settingsWidget


class MyTableWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(MyTableWidget, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)

        self.tabs = QtWidgets.QTabWidget()
        self.dialoglistwidget = DialogListWidget.DialogListWidget(self)

        self.audiolistwidget = AudioListWidget.listWidgetAudio(self)
        self.dialogwidget = DialogWidget.WidgetDialog(self)
        self.tabs.addTab(self.dialoglistwidget, "Диалоги")
        self.tabs.addTab(self.dialogwidget, "Активынй диалог")
        self.tabs.addTab(self.audiolistwidget, "Музыка")

        t2 = Thread(target=self.audiolistwidget.loading_albums, args=(100, 0))
        t2.isDaemon = True;
        t2.start()

        t = Thread(target=self.audiolistwidget.loading_audios, args=(10000, 0))
        t.isDaemon = True;
        t.start()

        self.dialoglistwidget.listview.itemClicked.connect(self.ChatListItemClick)
        self.tabs.addTab(settingsWidget.SetttingsWidget(self), "Настрйки")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def ChatListItemClick(self, item):
        self.dialogwidget.resize(self.width(), self.height())
        settings.width = self.width()
        settings.height = self.height()
        self.tabs.setCurrentWidget(self.dialogwidget)
        t = Thread(target=self.dialogwidget.open_dialog, args=(self.dialoglistwidget.listview.itemWidget(item).ID,))
        t.start()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.pinned = True
        self.top = False
        # keyboard.add_hotkey('Ctrl + 1', self.openTopWindow)

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check)
        self.logged = False
        self.setWindowTitle("VkKiwi")
        self.window = LoginWindow.LoginDialog()
        if not self.logged:
            self.window.show()
            self.timer.start(300)
        else:
            self.show()

    def resizeEvent(self, event):
        settings.width = int(event.size().width())

    def openTopWindow(self):

        self.hide()
        if not self.top:
            if self.pinned:
                self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
                self.show()
            self.top = True
        else:
            if self.pinned:
                self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
                self.show()

            self.top = False

    def initUi(self):
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.menu = QtWidgets.QMenu(self)

        action1 = self.menu.addAction('закрыть')
        action1.triggered.connect(self.close)

        action2 = self.menu.addAction('закрпеить')
        action2.triggered.connect(self.pin)

        action3 = self.menu.addAction('Открепить')
        action3.triggered.connect(self.unpin)

    def pin(self):
        self.hide()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()
        self.pinned = True;

    def unpin(self):
        self.hide()
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        self.setWindowFlags(QtCore.Qt.Window)
        self.show()
        self.pinned = False;

    def show_context_menu(self, point):
        self.menu.exec_(self.mapToGlobal(point))

    def showWidnow(self):
        self.initUi()
        self.show()
        self.resize(500, 500)

    def check(self):
        if self.window.auth:
            self.timer.stop()
            self.window.hide()
            self.window.deleteLater()
            self.showWidnow()
