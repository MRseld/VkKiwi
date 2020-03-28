import requests
import os
from PySide2  import QtGui 
from PySide2 import QtCore
import urllib
class LoadImage(QtCore.QObject):
   LoadFinished=QtCore.Signal(QtGui.QPixmap)
   def Loadimage(self,url:str):
      data = urllib.request.urlopen(url).read()
      pixmap = QtGui.QPixmap()
      pixmap.loadFromData(data)
      self.LoadFinished.emit(pixmap)
      return pixmap
  
      

 

           