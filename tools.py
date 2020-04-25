# -*- coding: utf-8 -*-
import requests
import os
from PySide2  import QtGui 
from PySide2 import QtCore
from PySide2 import QtWidgets 
import ApiCalls

import urllib


        
class ImageHandler():
    _image:QtGui.QPixmap=None
   
    def getImageFromPath(self,path):
        return self._imageFromPath(path)
    def setimageFromPixmap(self,pixmap):
        self._image=pixmap
    def setimageFromUrl(self,url):
        self._image=self._imageFromUrl(url)

    def setimageFromPath(self,path):
        self._image=self._imageFromPath(path)
    
    def _imageFromPath(self,path):
        pix=QtGui.QPixmap(path)
        self.width=pix.width
        self.height=pix.height
        return pix
       
    def getImageFromUrl(self,url):
        self._image=self._imageFromUrl(url)
        return self._image

    def _imageFromUrl(self,url:str):      
      data = urllib.request.urlopen(url).read()      
      pix = QtGui.QPixmap()
      pix.loadFromData(data)

      return pix
      
    def resizeImage(self,width,height):
        self._image= self._image.scaled(QtCore.QSize(width,height),QtCore.Qt.IgnoreAspectRatio)

    def resizeRatio(self,width,height):
        self._image= self._image.scaled(QtCore.QSize(width,height),QtCore.Qt.KeepAspectRatio)

    def antialiasing(self):
        target = QtGui.QPixmap(QtCore.QSize(self.width,self.height))  
        target.fill(QtCore.Qt.transparent)    

        painter = QtGui.QPainter(target)
       
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

        path = QtGui.QPainterPath()
        path.addRoundedRect(0, 0, self._image.width(), self._image.height(), 0,0)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self._image)
        self._image=target


    def drawImage(self,posX,posY,Pixmap,width=None,height=None):
        painter= QtGui.QPainter(self._image)
        if width!=None and height!=None:
            
            painter.drawPixmap(posX, posY,width,height, Pixmap)

        else:  painter.drawPixmap(posX, posY,Pixmap.width(),Pixmap.height(), Pixmap)

        painter.end()
    
    
    
    def drawText(self,posX,posY,width,height,text):
        painter= QtGui.QPainter(self._image)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        painter.drawText(posX,posY,width,height, QtCore.Qt.AlignLeft, str(text))
        painter.end()

    def roundImage(self,Antialiasing:bool,radius:int):

        

        target = QtGui.QPixmap(QtCore.QSize(self._image.width(),self._image.height()))  
        target.fill(QtCore.Qt.transparent)    

        painter = QtGui.QPainter(target)
        if Antialiasing:
            painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
            painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

        path = QtGui.QPainterPath()
        path.addRoundedRect(
            0, 0, self._image.width(), self._image.height(), radius, radius)
        painter.setClipPath(path)
        painter.drawPixmap(0, 0, self._image)

        self._image=target

    def getImage(self):
        return self._image

  

       
  

    
       
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
      

 

           