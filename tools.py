# -*- coding: utf-8 -*-
import requests
import os
from PySide2  import QtGui 
from PySide2 import QtCore
from PySide2 import QtWidgets 
import ApiCalls
import  time
import urllib

def time_to_human_time(timeValue):

    d=int( timeValue/1000)
    minutes=int(d/60)
    seconds=int(d%60)
    return  str(minutes)+":"+str(seconds)
def time_to_date(timeValue):
    return  time.localtime(timeValue)

class ImageHandler():
    _image:QtGui.QPixmap=None
   
    def get_image_from_path(self,path):
        return self._imageFromPath(path)

    def set_image_from_pixmap(self,pixmap):
        self._image=pixmap
    def set_image_from_url(self,url):
        self._image=self._imageFromUrl(url)

    def set_image_from_path(self,path):
        self._image=self._imageFromPath(path)
    
    def _imageFromPath(self,path):
        pix=QtGui.QPixmap(path)
        self.width=pix.width
        self.height=pix.height
        return pix
       
    def get_image_from_url(self,url):
        self._image=self._imageFromUrl(url)
        return self._image

    def _imageFromUrl(self,url:str):      
      data = urllib.request.urlopen(url).read()      
      pix = QtGui.QPixmap()
      pix.loadFromData(data)

      return pix
      
    def resize_image(self,width,height):
        self._image= self._image.scaled(QtCore.QSize(width,height),QtCore.Qt.IgnoreAspectRatio)

    def resize_ratio(self,width,height):
        self._image= self._image.scaled(QtCore.QSize(width,height),QtCore.Qt.KeepAspectRatio)

    def draw_image(self,posX,posY,Pixmap,width=None,height=None):
        painter= QtGui.QPainter(self._image)
        if width!=None and height!=None:
            
            painter.drawPixmap(posX, posY,width,height, Pixmap)

        else:  painter.drawPixmap(posX, posY,Pixmap.width(),Pixmap.height(), Pixmap)

        painter.end()

    def draw_text(self,posX,posY,width,height,text):
        painter= QtGui.QPainter(self._image)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        painter.drawText(posX,posY,width,height, QtCore.Qt.AlignLeft, str(text))
        painter.end()

    def round_image(self,Antialiasing:bool,radius:int):

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

    def get_image(self):
        return self._image
       
class longPollQT(ApiCalls.LongPoll,QtCore.QObject):
    signalNewMessage=QtCore.Signal(int,dict)
    signalDialogIsread=QtCore.Signal(int,dict)
     
    def update(self):
        self.RequestServer()
        obj= self.getLongPolldata()
        print(str(obj["updates"]))
        for i in range(0,len(obj["updates"])):
            if(obj["updates"][i][0]==4):
                self.signalNewMessage.emit(i,obj)
            if(obj["updates"][i][0]==6):
                self.signalDialogIsread.emit(i,obj)
      
