import requests
import os
from PyQt5  import QtGui 
from PyQt5 import QtCore
import urllib
class LoadImage(QtCore.QObject):
   LoadFinished=QtCore.pyqtSignal(QtGui.QPixmap)
   def Loadimage(self,url:str):
      data = urllib.request.urlopen(url).read()
      pixmap = QtGui.QPixmap()
      pixmap.loadFromData(data)
      self.LoadFinished.emit(pixmap)
      return pixmap
  
      

 

           