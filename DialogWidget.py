# -*- coding: utf-8 -*-
import threading

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import CustomObjects
import ApiCalls
import settings
import tools
import  pprint
import time


class  WidgetMessage(QtWidgets.QWidget):
    
    def __init__(self, parent,message,type,metaData):
        self.attachmentCount=0;
        super(WidgetMessage, self).__init__(parent)
        self.labelAvatar=QtWidgets.QLabel()
        self.layoutMain=QtWidgets.QHBoxLayout()
        self.layoutInner= QtWidgets.QVBoxLayout()
        self.lw=None
        self.dataScrollIsVisible=False
        self.scroll=None
        self.labelName=QtWidgets.QLabel()
        self.textBrowserData=QtWidgets.QTextBrowser()

        self.layoutInner.addWidget(self.labelName)

        self.layoutMain.addWidget(self.labelAvatar)
        self.layoutMain.addLayout(self.layoutInner)
        self.layoutMain.setAlignment(QtCore.Qt.AlignLeft)

        self.layoutInner.setAlignment(QtCore.Qt.AlignLeft)

        self.setLayout(self.layoutMain)
        self.__load_data(message,type,metaData)

    def get_CountAttachments(self):
        return self.attachmentCount
    
    

    def __load_data(self,message,type,metadata):
        if type == CustomObjects.userType.user:
            self.set_name_value(metadata["first_name"]+" "+metadata["last_name"])
        elif type == CustomObjects.userType.group:
            self.set_name_value(metadata["name"])

        if len( message["text"]) > 0:

            self.set_text_value(message["text"])
            self.layoutInner.addWidget(self.textBrowserData)

        if len (message["attachments"]) > 0:
            self.__load_attacments(message["attachments"])
        threading.Thread(target=self.__load_avatar, args=(metadata["photo_50"],)).start()

    def __load_attacments(self,attachments):
        self.photos=[]
        self.audios=[]
        self.videos=[]
        for i in attachments:
            if i["type"] == "photo":
                self.photos.append(i["photo"])
                self.attachmentCount=self.attachmentCount+1;
            if i["type"]=="audio":
                self.audios.append(i["audio"])
            if i["type"]=="video":
                self.videos.append(i["video"])
                self.attachmentCount=self.attachmentCount+1;
            
        if len(self.photos)>0:
            #self.layoutInner.addLayout( self.__create_images_layout(self.photos))
            kf=self.__create_imageList_widget(self.photos)
            self.layoutInner.addWidget(kf)

        if len(self.audios)>0:
           self.layoutInner.addLayout(  self.__create_audios_layout(self.audios))
        if len(self.videos)>0:
            self.__create_videos_layout(self.videos)

    def __create_videos_layout(self,videos):
        listWidgetVideos=QtWidgets.QListWidget()
        pprint.pprint(videos)
    
    def __load_img_attach_thread(self,width,height, item:QtWidgets.QTableWidgetItem, url:str):
        s= tools.ImageHandler()
        s.set_image_from_url(url)
        s.resize_image(width,height)
        item.setIcon(QtGui.QIcon(s.get_image()));

    def __load_img_sticker_threage(self,width,height,label:QtWidgets.QLabel, url:str):
        s=tools.ImageHandler()
        s.set_image_from_url(url)
        s.resize_image(width,height)
        label.setPixmap(s.get_image())

    def __create_imageList_widget(self,photos):
                self.setFixedWidth = settings.width-50
                
                self.lw=QtWidgets.QListWidget()
                self.lw.setFixedHeight(50)
                self.scroll =CustomObjects.DataScrollBar(self)
                self.lw.setVerticalScrollBar(self.scroll)
                self.lw.setIconSize(QtCore.QSize(100,100))
                self.lw.setViewMode(QtWidgets.QListWidget.IconMode)
                self.setFixedWidth = settings.width-50
                for i in photos:
                    a = QtWidgets.QLabel()
                    mypix=QtGui.QPixmap(100,100)
                    mypix.fill(QtCore.Qt.gray)
                    item=QtWidgets.QListWidgetItem(QtGui.QIcon(mypix),"")
                    t = threading.Thread(target=self.__load_img_attach_thread, args=(100, 100, item, i["sizes"][0]["url"])).start()                    
                    self.lw.addItem(item)
                self.lw.setFixedWidth(settings.width-50)
                self.lw.update()
                self.lw.updateGeometry()
                self.lw.setResizeMode(QtWidgets.QListWidget.ResizeMode().Adjust);

                                
                return self.lw

    def __create_audios_layout(self,audios):
        layoutData= QtWidgets.QVBoxLayout()
        for i in audios:
            layoutInner=QtWidgets.QHBoxLayout()
            pixImage=tools.ImageHandler().get_image_from_path("icons/audioplay.png")
            labelImage=QtWidgets.QLabel()
            labelImage.setPixmap(pixImage)

            a = QtWidgets.QLabel(i["artist"]+"\n" + i["title"])

            layoutInner.addWidget(labelImage)
            layoutInner.addWidget(a)
            layoutInner.setAlignment(QtCore.Qt.AlignLeft)
            layoutData.addLayout(layoutInner)

        return  layoutData


    def __create_images_layout(self,photos):
        self.setFixedWidth = settings.width-50
        gridLayout = QtWidgets.QGridLayout()

        gridLayout.setSpacing(1)
        gridLayout.setHorizontalSpacing(1)
        gridLayout.setVerticalSpacing(1)
        sz = 0
        row = 0
        column = 0
        for i in photos:
            a = QtWidgets.QLabel()
            mypix=QtGui.QPixmap(100,100)
            mypix.fill(QtCore.Qt.gray)
            a.setPixmap(mypix)
            t = threading.Thread(target=self.__load_img_attach_thread, args=(100, 100, a, i["sizes"][0]["url"]))

            gridLayout.addWidget(a, row, column)
            if self.width() - 0 > sz:
                gridLayout.setColumnMinimumWidth(column, 100)
                column = column + 1
            else:
                gridLayout.setRowMinimumHeight(row, 100)
                sz = 0
                column = 0
                row = row + 1
            sz = sz + 80
            t.start()
        return gridLayout

    def __load_avatar(self,url):
       handlerImageAvatar= tools.ImageHandler()
       handlerImageAvatar.set_image_from_url(url)
       handlerImageAvatar.round_image(True,50)
       self.set_avatar_pixmap(handlerImageAvatar.get_image())
       handlerImageAvatar=None

    def set_avatar_pixmap(self,pixmap:QtGui.QPixmap):
        self.labelAvatar.setPixmap(pixmap)

    def set_text_value(self,text):
        self.textBrowserData.setText(str(text))
        self.textBrowserData.document().adjustSize()
        self.textBrowserData.setFixedHeight(self.textBrowserData.document().size().height() + 4)

    def set_name_value(self,text):
        self.labelName.setText(str(text))


class WidgetDialog(QtWidgets.QWidget):
    apiMessage=ApiCalls.Messages();
    signalMessageLoad=QtCore.Signal(dict,str,dict)
    def __init__(self, parent):
        super().__init__(parent)
        self.imageHandlerUserDefault=tools.ImageHandler()
        self.imageHandlerUserDefault.set_image_from_url("https://vk.com/images/camera_50.png?ava=1")
        self.imageHandlerUserDefault.round_image(True,50)

        self.peer_id=None
        self.signalMessageLoad.connect(self.slot_message_load)

        self.layoutMain=QtWidgets.QVBoxLayout()
        self.layoutControl=QtWidgets.QHBoxLayout()
        self.listWidget=QtWidgets.QListWidget()

        self.labelSendIcon=CustomObjects.СlickableLabel()
        self.labelAttachIcon=CustomObjects.СlickableLabel()

        self.textEditMessage= QtWidgets.QTextEdit()
        self.textEditMessage.setFixedHeight(40)
        self.init_images()
        self.init_layout()
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy().ScrollBarAlwaysOff )

    def resizeEvent(self,ev):
        ev:QtGui.QResizeEvent=ev
        for i   in range(0, self.listWidget.count()):
           wi:WidgetMessage= self.listWidget.itemWidget( self.listWidget.item(i))
           if wi.lw!=None:
                wi.lw.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy().ScrollBarAlwaysOff)
                ws=ev.size().width()-wi.lw.width()
                if wi.get_CountAttachments()!=1:
                    if ev.oldSize().width()<ev.size().width():
                        print("--")
                        wi.lw.setFixedWidth(ev.size().width()-200)
                    else:
                        print("++")
                        wi.lw.setFixedWidth(ev.size().width()-200)



    def init_images(self):
        self.handlerSendIcon=tools.ImageHandler()
        self.handlerSendIcon.set_image_from_path("icons/sent.png")
        self.handlerAttachIcon=tools.ImageHandler()
        self.handlerAttachIcon.set_image_from_path("icons/attach.png")
        self.labelSendIcon.setPixmap(self.handlerSendIcon.get_image())
        self.labelAttachIcon.setPixmap(self.handlerAttachIcon.get_image())

    def init_layout(self):
        self.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.listWidget)
        self.layoutMain.addLayout(self.layoutControl)
        self.layoutControl.addWidget(self.labelAttachIcon)
        self.layoutControl.addWidget(self.textEditMessage)
        self.layoutControl.addWidget(self.labelSendIcon)

    def open_dialog(self,peer_id:int):
        self.listWidget.clear()
        self.peer_id=peer_id
        self.__load_dialogs(50,0)

    def resizeData(self,wi,item):
        wi.lw.setFixedHeight(wi.lw.height()+ wi.lw.verticalScrollBar().maximum())
        item.setSizeHint(QtCore.QSize(wi.sizeHint().width(),wi.sizeHint().height()+ wi.lw.height()-60 ))
    
    def slot_message_load(self,message,type,metadata): # слот в основном потоке окна

        item = QtWidgets.QListWidgetItem()
        wi = WidgetMessage(self, message,type, metadata)
        item.setSizeHint(wi.sizeHint())
        wi.set_avatar_pixmap(self.imageHandlerUserDefault.get_image())
        if wi.scroll!=None:
            wi.scroll.resized.connect(
                lambda: self.resizeData(wi,item) )

        if wi.get_CountAttachments()>0:
                wi.lw.setFixedHeight(120)
                item.setSizeHint(QtCore.QSize(wi.sizeHint().width(),wi.sizeHint().height()+wi.lw.height()-50))
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item,wi)

    def __load_dialogs(self,count,offset):#метод в другом потоке

        data=self.apiMessage.getHistory(count,offset,self.peer_id,0,1)
        k=0
        for i  in data["response"]["items"]:
            if "profiles" in data["response"]:
                for j in data["response"]["profiles"]:
                    if j["id"] == i["from_id"]:
                        self.signalMessageLoad.emit(i,CustomObjects.userType.user,j)
                        break

            if "groups" in data["response"]:
                for j in data["response"]["groups"]:
                    if j["id"]*-1 == i["from_id"]:
                        self.signalMessageLoad.emit(i, CustomObjects.userType.group, j)

                        break
            k=k+1
            if k==50:
                time.sleep(0.05)
                self.listWidget.update()
                k=0

