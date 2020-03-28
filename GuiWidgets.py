
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import ApiCalls
from vkObjects import convestationsObject
import tools
from threading import Thread
import time


class DialogListWidgetPanel(QtWidgets.QWidget):
    def __init__(self, parent):
        super(DialogListWidgetPanel, self).__init__(parent)
        self.ID=0

        self.ImageLabel = QtWidgets.QLabel()
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.innerlayout = QtWidgets.QVBoxLayout()
        self.unreadCount=0
        self.unreadCountsLabel=QtWidgets.QLabel()
        self.TitleLabel = QtWidgets.QLabel()
        self.TitleLabel.setStyleSheet("font-weight: bold; color: black")
        self.TextLabel = QtWidgets.QLabel()
        self.innerlayout.addWidget(self.TitleLabel)
        self.innerlayout.addWidget(self.TextLabel)

        self.mainLayout.addWidget(self.ImageLabel)
        self.mainLayout.addLayout(self.innerlayout)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.unreadCountsLabel)
        self.innerlayout.addStretch()
        self.mainLayout.addStretch

    def getID(self):
      return self.ID

    def getUnreadCount(self):
      return self.unreadCount

    def getText(self):
        return self.TextLabel.text()
    def getTitle(self):
        return self.TitleLabel.text()

    def getPixmap(self):
        return self.ImageLabel.pixmap()

    def setUnreadCount(self,count:int):
      self.unreadCount=count
      if(self.unreadCount>0 and self.unreadCount!=1463556740):
        self.setUnreadCountLabelValue(self.unreadCount)

    def setUnreadCountLabelValue(self,count):
      self.unreadCountsLabel.setText("("+str(count)+")")

    def setText(self, text):
        self.TextLabel.setText(text)

    def setTitleText(self, text):
        self.TitleLabel.setText(text)

    def setId(self,value:int):
      self.ID=value

    def setImage(self, image: QtGui.QPixmap):
        self.ImageLabel.setPixmap(image)
        self.ImageLabel.setFixedSize(QtCore.QSize(50, 50))

class longPollQT(ApiCalls.LongPoll,QtCore.QObject):
    newMessage=QtCore.Signal(int,ApiCalls.longpolldataobject.LongpolldataObject)
    def update(self):
        self.RequestServer()
        obj= self.getLongPolldataObject()
        for i in range(0,len(obj.updates)):
            if(obj.updates[i][0]==4):
                self.newMessage.emit(i,obj)

   
        

class DialogListWidget(QtWidgets.QWidget):
    MApi= ApiCalls.Messages()
    
    trigger = QtCore.Signal(int,int,str, str,str)
    newoffset = 0
    oldoffset=0
    count = 0

    def __init__(self, parent):
        super(DialogListWidget, self).__init__(parent)

        self.standartImage=QtGui.QPixmap("NP.jpg")
        self.trigger.connect(self.loadedSlot)
        self.loader = tools.LoadImage()
        

        t = Thread(target=self.LoadDialogs, args=(50,0))
        t.setDaemon(True)
        t.start()

        lt=Thread(target=self.LongPollStart)
        lt.setDaemon(True)
        lt.start()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.listview = QtWidgets.QListWidget()
        self.Vscroll = QtWidgets.QScrollBar()
        self.Vscroll.valueChanged.connect(self.Vscrolled)
        self.listview.setVerticalScrollBar(self.Vscroll)
        self.setLayout(self.layout)
        self.layout.addWidget(self.listview)

    def updateElement(self,oldPanel:DialogListWidgetPanel,item):

        w = DialogListWidgetPanel(self)
        print(oldPanel.getTitle())
        w.setId(oldPanel.getID())
        w.setText(oldPanel.getText())
        w.setTitleText(oldPanel.getTitle())
        w.setImage(oldPanel.getPixmap())
        w.setUnreadCount(oldPanel.getUnreadCount())
        self.listview.setItemWidget(item,w)


    def NewMessage(self,index,object: ApiCalls.longpolldataobject.LongpolldataObject):

          while self.loading==True:
            pass

          for i in range(0,self.listview.count()):

              w: DialogListWidgetPanel = self.listview.itemWidget(
                        self.listview.item(i))

              if(object.updates[index][3]==w.getID()):
                if object.updates[index][5]!=None:
                  w.setText(object.updates[index][5])
                if object.updates[index][7].attach1_type!=None:
                  w.setText(object.updates[index][7].attach1_type)
              
                item:QtWidgets.QListWidgetItem=self.listview.item(i) 

                self.listview.takeItem(i)
                self.listview.insertItem(0,item)   
                self.updateElement(w,item)
               
                break
               

    def LongPollStart(self):

        LPApi=longPollQT()
        LPApi.getLongPollServer()
        LPApi.setMode(10)
        LPApi.newMessage.connect(self.NewMessage)
        while True:
            LPApi.update()

    def Vscrolled(self, i):
        if(self.Vscroll.maximum() == i):
            if(self.newoffset != self.count):
                t = Thread(target=self.LoadDialogs, args=(50, self.newoffset))
                t.start()

    def loadImageThread(self, panel:DialogListWidgetPanel,url):
        panel.setImage(self.loader.Loadimage(url))

    def loadedSlot(self,id, unreadcount, title, text,imageUrl):
        item = QtWidgets.QListWidgetItem()

        w = DialogListWidgetPanel(self)
        print(title)
        print(str(imageUrl))
        if(imageUrl!=None and imageUrl!=""):
            t=Thread(target=self.loadImageThread,args=(w,imageUrl))
            t.setDaemon(True)
            t.start()
        else:
            t=Thread(target=self.loadImageThread,args=(w,"https://vk.com/images/camera_50.png?ava=1"))

            t.setDaemon(True)
            t.start()
        w.setId(id)
        w.setText(text)
        w.setTitleText(title)
        
        w.setUnreadCount(unreadcount)
        item.setSizeHint(w.sizeHint())
        self.listview.addItem(item)
        self.listview.setItemWidget(item, w)
      
    
      

    def LoadDialogs(self, count, offset):
        self.loading=True
        Converstations = self.MApi.get(count, offset, 1)
        self.count = Converstations.response.count
        for i in range(0, len(Converstations.response.items)):

            if (str(Converstations.response.items[i].conversation.peer.type) == "TypeEnum.CHAT"):
                self.LoadChatDialog(Converstations, i)
            elif (str(Converstations.response.items[i].conversation.peer.type) == "TypeEnum.USER"):
                self.LoadUserDialog(Converstations, i)
            else:
                self.LoadGroupDialog(Converstations, i)
        self.newoffset = self.newoffset + len(Converstations.response.items)
        
        #for i in range(0, len(Converstations.response.items)):
         #   try:
          #      if (str(Converstations.response.items[i].conversation.peer.type) == "TypeEnum.CHAT"):
           #         tz = Thread(target=self.LoadChatImage,
            #                    args=(Converstations, i))
                   
             #       tz.start()
              #  elif (str(Converstations.response.items[i].conversation.peer.type) == "TypeEnum.USER"):
               #     tz = Thread(target=self.LoadUserImage,
                #                args=(Converstations, i))
                 #   tz.start()
                #else:
                 #   tz = Thread(target=self.loadGroupImage,
                  #              args=(Converstations, i))
                 #   tz.start()
            #except Exception as ex:
             #   print(ex)
        self.oldoffset = self.oldoffset + len(Converstations.response.items)
        self.loading=False

    def loadGroupImage(self, conversations: convestationsObject.Convestation, index: int):
        conversation = conversations.response.items[index].conversation
        for i in range(0, len(conversations.response.groups)):
            group = conversations.response.groups[i]
            if(conversation.peer.id*-1 == group.id):
                if(group.photo_50 != None):
                    w: DialogListWidgetPanel = self.listview.itemWidget(
                        self.listview.item(self.oldoffset+index))
                    w.setImage(self.loader.Loadimage(group.photo_50))
                    time.sleep(0.2)
                    break

    def LoadUserImage(self, conversations: convestationsObject.Convestation, index: int):
        if(len(conversations.response.items[index].last_message.fwd_messages) > 0):
            textMessage = "[Пересланные сообщения]"
        else:
            textMessage = conversations.response.items[index].last_message.text
        conversation = conversations.response.items[index].conversation
        for i in range(0, len(conversations.response.profiles)):
            profile = conversations.response.profiles[i]
            if(conversation.peer.id == profile.id):
                w: DialogListWidgetPanel = self.listview.itemWidget(
                    self.listview.item(self.oldoffset+index))
                w.setImage(self.loader.Loadimage(profile.photo_50))
                time.sleep(0.2)
                
                break

    def LoadChatImage(self, conversations: convestationsObject.Convestation, index: int):
        conversation = conversations.response.items[index]
        if(conversation.conversation.chat_settings.photo != None):
            w = self.listview.itemWidget(self.listview.item(self.oldoffset+index))
            w.setImage(self.loader.Loadimage(
                conversation.conversation.chat_settings.photo.photo_50))
            time.sleep(0.2)
            

    def startloadImage(self, url):
        self.loader.Loadimage(url)

    def LoadGroupDialog(self, conversations: convestationsObject.Convestation, index: int):
        if(len(conversations.response.items[index].last_message.fwd_messages) > 0):
            textMessage = "[Пересланные сообщения]"
        elif(len(conversations.response.items[index].last_message.attachments) > 0):
            if(len(conversations.response.items[index].last_message.attachments) == 1):
                textMessage = "Вложение"
            else:
                textMessage = "[Вложения]"
        else:
            textMessage = conversations.response.items[index].last_message.text
        conversation = conversations.response.items[index].conversation

        for i in range(0, len(conversations.response.groups)):
            group = conversations.response.groups[i]
            if(conversation.peer.id*-1 == group.id):

                title = group.name+"[Группа]"

                try:
                  self.trigger.emit(group.id, conversation.unread_count, title, textMessage,group.photo_50)
                except:
                  self.trigger.emit(group.id, 0, title, textMessage,group.photo_50)
                break

          # Получение данных о юзере
    def LoadUserDialog(self, conversations: convestationsObject.Convestation, index: int):
        if(len(conversations.response.items[index].last_message.fwd_messages) > 0):
            textMessage = "[Пересланные сообщения]"

        elif(len(conversations.response.items[index].last_message.attachments) > 0):
            if(len(conversations.response.items[index].last_message.attachments) == 1):
                textMessage = "[Вложение]"
            else:
                textMessage = "[Вложения]"

        else:
            textMessage = conversations.response.items[index].last_message.text
        conversation = conversations.response.items[index].conversation

        for i in range(0, len(conversations.response.profiles)):
            profile = conversations.response.profiles[i]
            if(conversation.peer.id == profile.id):

                title = profile.first_name+" " + \
                    profile.last_name+"[Пользователь]"
                try:
                  self.trigger.emit(profile.id,conversation.unread_count, title, textMessage,profile.photo_50)
                except:
                  self.trigger.emit(profile.id,0, title, textMessage,profile.photo_50)
                break

    def LoadChatDialog(self, conversations: convestationsObject.Convestation, index: int):
      
            conversation = conversations.response.items[index]

            if(len(conversations.response.items[index].last_message.fwd_messages) > 0):
                textMessage = "[Пересланные сообщения]"
            elif(len(conversations.response.items[index].last_message.attachments) > 0):
                if(len(conversations.response.items[index].last_message.attachments) == 1):
                    textMessage = "Вложение"
                else:
                    textMessage = "[Вложения]"

            else:
                textMessage = conversations.response.items[index].last_message.text

            text = conversation.last_message.text
            title = conversation.conversation.chat_settings.title+"[Беседа]"
            if(conversation.conversation.chat_settings.photo==None):

                try:
                    self.trigger.emit(conversation.conversation.peer.id, 
                    conversation.conversation.unread_count, title, textMessage,
                    None)
                except:
                    self.trigger.emit(conversation.conversation.peer.id,0, title, textMessage,
                    None)
            else:


                try:
                    self.trigger.emit(conversation.conversation.peer.id, 
                    conversation.conversation.unread_count, title, textMessage,
                    conversation.conversation.chat_settings.photo.photo_50)
                except:
                    self.trigger.emit(conversation.conversation.peer.id,0, title, textMessage,
                    conversation.conversation.chat_settings.photo.photo_50)
            
        
