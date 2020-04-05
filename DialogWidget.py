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
             image=tools.RoundImage(data,True,100,50,50).getImage()

        self.avatarLabel.setPixmap(image)
        self.avatarLabel.setFixedSize(QtCore.QSize(50, 50))

    def addWidgetToMainLayout(self,widget):
        self.layout.addWidget(widget)

    def addWidgetToInnerLayout(self,widget):
        self.innerLayout.addWidget(widget)   #error QObject::setParent: Cannot set parent, new parent is in a different thread





class DialogWidget(QtWidgets.QWidget):
    trigger=QtCore.Signal(str,str,str,dict)

    def __init__(self, parent):
        self.loader = tools.LoadImage()
        self.standartImage=self.loader.Loadimage("https://vk.com/images/icons/im_multichat_50.png")
   
        super(DialogWidget,self).__init__(parent )
        self.widgetSizehint=0
        self._attachmentsCount=0
        self.Images=[]
        self.Videos=[]
        self.Audios=[]
        self.trigger.connect(self.loadSlot)
        self.MApi=ApiCalls.Messages()
        self.newOffset=0
        self.oldOffset=0
        self.dialogID=None
        self.layout=QtWidgets.QVBoxLayout(self)
        self.setLayout(self.layout)
        self.listWidget=QtWidgets.QListWidget(self)
        
        self.layout.addWidget(self.listWidget)
        self.Vscroll = QtWidgets.QScrollBar()
        self.Vscroll.setSingleStep(10)
        self.listWidget.setVerticalScrollBar(self.Vscroll)
        self.listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel);


    def loadImageAvatarThread(self, panel:DialogPanelWidget,url):
        panel.setAvatar(self.loader.Loadimage(url),True)

    def loadImageAttachThread(self, label:QtWidgets.QLabel,url):
        pix=self.loader.Loadimage(url)
        pix=pix.scaled(QtCore.QSize(80,80),QtCore.Qt.KeepAspectRatio);

        label.setPixmap(pix)

    

    def loadAttacment(self,images):
        self.setFixedWidth=settings.width
        k=QtWidgets.QGridLayout()
        k.setSpacing(1)
        sz=0
        row=0
        column=0
        s=0
        print(str(images))
        
        for i  in range( len (images)):
            a=QtWidgets.QLabel()
            a.setPixmap(QtGui.QPixmap(80,80))
            t=threading.Thread(target=self.loadImageAttachThread,args=(a,images[i]["url"]))
            t.start()
            k.addWidget(a,row,column)  
            if self.width()-200>sz:
                column=column+1
            else:
                sz=0
                column=0
                row=row+1
            
            sz=sz+120
        self._attachmentsCount=0
        
        return k

    def loadSlot(self,name,text,url,images):
        print("1")
        item=QtWidgets.QListWidgetItem()
        w=DialogPanelWidget(self)
        t=threading.Thread(target=self.loadImageAvatarThread,args=(w,url))
        t.start()
        if len(text)>0:
            w.setTextBrowserText(text)
             
            
           # w.textBrowser.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred);
                
        w.setNameLabel(name+"("+str(len (self.Images))+")")
        w.setAvatar(self.standartImage,True)
        if(images!=None):
            atth=self.loadAttacment(images)
            w.innerLayout.addLayout(atth)
            
            item.setSizeHint(w.sizeHint())
        else:
            item.setSizeHint(w.sizeHint())

        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item,w)
        
    def OpenDialog(self,id):
        self.dialogID=id
        self.listWidget.clear()
        self._LoadMessages(50,0)
       
        
    
    def _LoadAttachments(self,chat):
       image=[]
       videos=[]
       for i in range( len( chat["attachments"])):
         
           if(str(chat["attachments"][i]["type"]))=="photo":

               print( chat["attachments"][i]["photo"]["sizes"])
               for j in range (len (chat["attachments"][i]["photo"]["sizes"])):
                   
                    if  chat["attachments"][i]["photo"]["sizes"][j]["type"]=="m":
                        
                        image.append( chat["attachments"][i]["photo"]["sizes"][j])
                        break

                    elif   chat["attachments"][i]["photo"]["sizes"][j]["type"]=="p":
                        image.append(chat["attachments"][i]["photo"]["sizes"][j])
                        break
                    self._attachmentsCount=self._attachmentsCount+1
                
    
           if(str(chat["attachments"][i]["type"]))=="video":
                videos.append(self.standartImage)
       return image          
        
    def _LoadMessages(self,count,offset):
        History=self.MApi.getHistory(count,offset,self.dialogID,0,True)
        print(str(History))
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
                   

           

