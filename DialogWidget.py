# -*- coding: utf-8 -*-
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWebEngine
from PySide2 import QtWebEngineWidgets
import ApiCalls
import tools
import threading 
import time
import settings


class DialogPanelWidget(QtWidgets.QWidget):
    def __init__(self, parent, ):

        super(DialogPanelWidget,self).__init__(parent, )
        self.layout=QtWidgets.QHBoxLayout()
        self.avatarLabel=QtWidgets.QLabel()
        self.textBrowser=QtWidgets.QTextBrowser()
        
        
      
        self.nameLabel=QtWidgets.QLabel()
        self.layout.addWidget(self.avatarLabel)
        self.innerLayout=QtWidgets.QVBoxLayout()
        self.innerLayout.addWidget(self.nameLabel)
        
        
        self.layout.addLayout(self.innerLayout)
        self.setLayout(self.layout)
       
        self.avatarLabel.setFixedSize(QtCore.QSize(50, 50))
       

    def setTextBrowserText(self,text):
       
        self.innerLayout.addWidget(self.textBrowser)
        self.innerLayout.addStretch()
        
        self.textBrowser.setText(str(text))
        self.textBrowser.document().adjustSize()
        
        self.textBrowser.setFixedHeight (self.textBrowser.document().size().height()+4) 
        

    def setNameLabel(self,name):
        self.nameLabel.setText(str(name))

    def setAvatar(self,data,round):
        if(round==True):
             handler=tools.ImageHandler()
             handler.setimageFromPixmap(data)
             handler.resizeImage(50,50)
             handler.roundImage(True,100)
             image=handler.getImage()
            

        self.avatarLabel.setPixmap(image)
        self.avatarLabel.setFixedSize(QtCore.QSize(50, 50))

    def addWidgetToMainLayout(self,widget):
        self.layout.addWidget(widget)

    def addWidgetToInnerLayout(self,widget):
        self.innerLayout.addWidget(widget)   #error QObject::setParent: Cannot set parent, new parent is in a different thread


class AudioLayout(QtWidgets.QHBoxLayout):

   
    def __init__(self, parent,audio):
        super().__init__(parent)
        self.playImageHandler=tools.ImageHandler()
        self.playImageHandler.setimageFromPath("icons/play2.ico")
        self.playing:bool=False
        self.setAlignment( QtCore.Qt.AlignLeft )
        self._id=None
        self._imageLabel=QtWidgets.QLabel()
        self._imageLabel.setPixmap(self.playImageHandler.getImage())
    

        self._titleLabel=QtWidgets.QLabel(audio["artist"]+":"+audio["title"])

        self.addWidget(self._imageLabel)
        self.addWidget(self._titleLabel)

    
    def setImage(self,pixmap:QtGui.QPixmap):
        self._imageLabel.setPixmap(pixmap)

    def setId(self,value):
        self._id=value

    def setTitleText(self,text):
        self._titleLabel.setText(str(text))

    def getId(self):
        self._id
    
class clickeDLabel(QtWidgets.QLabel):
    clicked= QtCore.Signal(QtGui.QMouseEvent)
    def mousePressEvent(self, ev):
        self.clicked.emit(ev)
    

    
    


class contextWidget(QtWidgets.QWidget):
    def __init__(self,parent):
        super(contextWidget,self).__init__(parent)
        self.layout= QtWidgets.QVBoxLayout();

        self.photoLabel=QtWidgets.QLabel("Фото")
        self.layout.addWidget(self.photoLabel)
        self.setLayout(self.layout)



class DialogWidget(QtWidgets.QWidget):
    trigger=QtCore.Signal(str,str,str,dict)

    
    def __init__(self, parent):
        
        super(DialogWidget,self).__init__(parent )

        self.popupWidget=contextWidget(parent)

        self.playImageHandler=tools.ImageHandler()
        self.playImageHandler.setimageFromPath("icons/play2.ico")

        self.sendMessageImageHandler=tools.ImageHandler();
        self.sendMessageImageHandler.setimageFromPath("icons/sent.png")

    
        self.sendMessageLabel=clickeDLabel()
        self.sendMessageLabel.clicked.connect(self.sendClicked)
        self.sendMessageLabel.setPixmap(self.sendMessageImageHandler.getImage())

    

        self.attachLabelImageHandler=tools.ImageHandler();
        self.attachLabelImageHandler.setimageFromPath("icons/attach.png")

        self.attachLabel=clickeDLabel()
        self.attachLabel.clicked.connect(self.attachClick)
        self.attachLabel.setPixmap(self.attachLabelImageHandler.getImage())
        

        self.messgeToolLayout=QtWidgets.QHBoxLayout()

        self.messageTextEdit=QtWidgets.QTextEdit()
        self.messageTextEdit.setFixedHeight(64);
        
        

        self.loader = tools.ImageHandler()
        self.standartImage=self.loader.getImageFromUrl("https://vk.com/images/icons/im_multichat_50.png")
   
        
        self.widgetSizehint=0
        self._attachmentsCount=0
       
        self.trigger.connect(self.loadSlot)
        self.MApi=ApiCalls.Messages()
        self.newOffset=0
        self.oldOffset=0
        self.dialogID=None
        self.layout=QtWidgets.QVBoxLayout(self)

       
        
       
        self.Vscroll = QtWidgets.QScrollBar()
        self.Vscroll.setSingleStep(10)

        self.listWidget=QtWidgets.QListWidget(self)
        self.listWidget.setVerticalScrollBar(self.Vscroll)
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)

        self.messgeToolLayout.addWidget(self.attachLabel)
        self.messgeToolLayout.addWidget(self.messageTextEdit)
        self.messgeToolLayout.addWidget(self.sendMessageLabel)

        self.layout.addWidget(self.listWidget)
        self.layout.addLayout(self.messgeToolLayout)

        self.setLayout(self.layout)

  
       
    def attachClick(self,event:QtGui.QMouseEvent):
        QtWidgets.QMenu("ts")
    def sendClicked(self,event:QtGui.QMouseEvent ):
        if(len( self.messageTextEdit.toPlainText())>0):
          ms=  ApiCalls.Messages()
        print(  ms.send(self.dialogID,self.messageTextEdit.toPlainText()))


    def OpenDialog(self,id):
        self.dialogID=id
        self.listWidget.clear()
        self._LoadMessages(50,0)
       

    def loadImageAvatarThread(self, panel:DialogPanelWidget,url):
        panel.setAvatar(tools.ImageHandler().getImageFromUrl(url),True)

    def loadImageAttachThread(self, width,height, label:QtWidgets.QLabel,url):

        handler=tools.ImageHandler()
        handler.setimageFromUrl(url)
        handler.resizeImage(width,height)
        
        label.setPixmap(handler.getImage())

    def loadVideoImageAttachThread(self, width,height, label:QtWidgets.QLabel,metaDataText,url):

        handler=tools.ImageHandler()
        handler.setimageFromUrl(url)
        handler.resizeRatio(width,height)
        
       

       

        #handler.drawImage(0,0,self.playImageHandler.getImage())

        handler.drawText(0,0,handler.getImage().width(),30,metaDataText)
        
        label.setPixmap(handler.getImage())

        
    def CreateImageLayout(self,images):
        self.setFixedWidth=settings.width
        gridLayout=QtWidgets.QGridLayout()
          
        gridLayout.setSpacing(1)
        gridLayout.setHorizontalSpacing(1)
        gridLayout.setVerticalSpacing(1)
        sz=0
        row=0
        column=0
        s=0
        
        for i  in range( len (images)):
            a=QtWidgets.QLabel()
            a.setPixmap(QtGui.QPixmap(100,100))
            t=threading.Thread(target=self.loadImageAttachThread,args=(100,100,a,images[i]["url"]))
           
            gridLayout.addWidget(a,row,column)  
            if self.width()-350>sz:
                gridLayout.setColumnMinimumWidth(column,100)
        
                column=column+1
                
     
            else:
                gridLayout.setRowMinimumHeight(row,100)
                sz=0
                column=0
                row=row+1
             
            sz=sz+80
            t.start()
        
        return gridLayout

    
    def CreateStickerLabel(self,sticker):
        self.setFixedWidth=settings.width
        l= QtWidgets.QLabel()
        l.setPixmap(  

                    tools.ImageHandler().getImageFromUrl( 
                        str(sticker["images"][0]["url"]
                    )
                )
            )
       
        return  l


    def CreteAudioLayout(self,audios):
        vLayout= QtWidgets.QVBoxLayout()
        for i in range(len(audios)):
            al=AudioLayout(self,audios[i])
            vLayout.addLayout(al)
        return vLayout
       
       

        
    def CreteVideoLayout(self,videos):

        self.setFixedWidth=settings.width
        gridLayout=QtWidgets.QGridLayout()
        gridLayout.setSpacing(1)
        gridLayout.setHorizontalSpacing(1)
        gridLayout.setVerticalSpacing(4)

        sz=0
        row=0
        column=0
        s=0
        
        for i  in range( len (videos)):
            a=QtWidgets.QLabel()
            a.setPixmap(QtGui.QPixmap(160,100))
            metadata=videos[i]["title"]+"("+ str(videos[i]["duration"])+" сек )"
            t=threading.Thread(target=self.loadVideoImageAttachThread,args=(160,100,a,metadata, videos[i]["image"][3]["url"]))
           
            gridLayout.addWidget(a,row,column)  
            if self.width()-1000>sz:
                column=column+1
            else:
                sz=0
                column=0
                row=row+1
            
            sz=sz+200
            t.start()
        return gridLayout
        

    def loadAttacment(self,attachments:dict):
        layoutdata= QtWidgets.QVBoxLayout()
        if(attachments["sticker"]!=None):
            layoutdata.addWidget(self.CreateStickerLabel(attachments["sticker"]))

        if( len (attachments["images"])>0):
            layoutdata.addLayout(self.CreateImageLayout(attachments["images"]))
        if(len (attachments["videos"])>0):
            layoutdata.addLayout(self.CreteVideoLayout(attachments["videos"]))
        if len(attachments["audios"])>0:
            layoutdata.addLayout(self.CreteAudioLayout(attachments["audios"]))
       
            
        return layoutdata
        

        
        
      

    def loadSlot(self,name,text,url,attachments):
        item=QtWidgets.QListWidgetItem()
        w=DialogPanelWidget(self)
        t=threading.Thread(target=self.loadImageAvatarThread,args=(w,url))
        t.start()
        if len(text)>0:
            w.setTextBrowserText(text)
             
            
           # w.textBrowser.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
                
        w.setNameLabel(name)
        w.setAvatar(self.standartImage,True)
        if(attachments!=None):
            atth=self.loadAttacment(attachments)
            w.innerLayout.addLayout(atth)
            
            item.setSizeHint(w.sizeHint())
        else:
            item.setSizeHint(w.sizeHint())

        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item,w)
   
        
    
    def _LoadAttachments(self,chat):
       sticker=None
       audios=[]
       images=[]
       videos=[]
       for i in range( len( chat["attachments"])):
         
           if(str(chat["attachments"][i]["type"]))=="photo":

               print( chat["attachments"][i]["photo"]["sizes"])
               for j in range (len (chat["attachments"][i]["photo"]["sizes"])):
                   
                    if  chat["attachments"][i]["photo"]["sizes"][j]["type"]=="q":
                        
                        images.append( chat["attachments"][i]["photo"]["sizes"][j])
                        break

                    elif   chat["attachments"][i]["photo"]["sizes"][j]["type"]=="p":
                        images.append(chat["attachments"][i]["photo"]["sizes"][j])
                        break
                    self._attachmentsCount=self._attachmentsCount+1
                
    
           if(str(chat["attachments"][i]["type"]))=="video":
              video= chat["attachments"][i]["video"]
              videos.append (video)

           if(str(chat["attachments"][i]["type"]))=="sticker":
               sticker=chat["attachments"][i]["sticker"]

           if (str(chat["attachments"][i]["type"])=="audio"):
               audios.append( chat["attachments"][i]["audio"])

            
       
       return {"images":images,"videos":videos,"audios":audios,"sticker":sticker}        
        
    def _LoadMessages(self,count,offset):
        History=self.MApi.getHistory(count,offset,self.dialogID,0,True)
        for i in  range(len(History["response"]["items"])):
           
            for j in range(len (History["response"]["profiles"])):
                if int(History["response"]["items"][i]["from_id"])==int(History["response"]["profiles"][j]["id"]):
                    profile=History["response"]["profiles"][j]
                    name=profile["first_name"]+" "+profile["last_name"]
                    photo=profile["photo_50"]

                    attachmentsWidget=None
                   
                    if "attachments" in History["response"]["items"][i]:
                       
                        self.trigger.emit(name,History["response"]["items"][i]["text"],photo,self._LoadAttachments(History["response"]["items"][i]))
                    else:
                        self.trigger.emit(name,History["response"]["items"][i]["text"],photo,None)
    """               
    def loadMessage(self,message):

        item=QtWidgets.QListWidgetItem()
        w=DialogPanelWidget(self)
        t=threading.Thread(target=self.loadImageAvatarThread,args=(w,url))
        t.start()
        if len(text)>0:
            w.setTextBrowserText(text)
             
            
           # w.textBrowser.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
                
        w.setNameLabel(name)
        w.setAvatar(self.standartImage,True)
        if(attachments!=None):
            atth=self.loadAttacment(attachments)
            w.innerLayout.addLayout(atth)
            
            item.setSizeHint(w.sizeHint())
        else:
            item.setSizeHint(w.sizeHint())

    """

           

