import requests
import os
from PySide2  import QtGui 
from PySide2 import QtCore
from PySide2 import QtWidgets 
import ApiCalls

import urllib

class LoadImage(QtCore.QObject):
   LoadFinished=QtCore.Signal(QtGui.QPixmap)
   def Loadimage(self,url:str):
      data = urllib.request.urlopen(url).read()
      pixmap = QtGui.QPixmap()
      pixmap.loadFromData(data)
      self.LoadFinished.emit(pixmap)
      return pixmap
  
class RoundImage(QtWidgets.QWidget):
    def __init__(self,  pixmap:QtGui.QPixmap,Antialiasing:bool,radius:int,width:int,height):
        super(RoundImage, self).__init__()
      
        self.width=width
        self.height=height
        self.radius = radius
        self.target = QtGui.QPixmap(QtCore.QSize(self.width,self.height))  
        self.target.fill(QtCore.Qt.transparent)    

        p =pixmap.scaled(  
            self.width, self.height, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)

        painter = QtGui.QPainter(self.target)
        if Antialiasing:
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            0, 0, self.width, self.height, self.radius, self.radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, p)
       
    def getImage(self):
        return self.target
    
       
class longPollQT(ApiCalls.LongPoll,QtCore.QObject):
    newMessageSignal=QtCore.Signal(int,dict)
    dialogIsreadSignal=QtCore.Signal(int,dict)
     
    def update(self):
            
        self.RequestServer()
        obj= self.getLongPolldata()
        print(str(obj["updates"]))
        for i in range(0,len(obj["updates"])):
            if(obj["updates"][i][0]==4):
                self.newMessageSignal.emit(i,obj)
            if(obj["updates"][i][0]==6):
                self.dialogIsreadSignal.emit(i,obj)
      

 

           