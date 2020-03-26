from PyQt5.QtCore import QThread, QTimer
from PyQt5 import QtWidgets 
from PyQt5 import QtGui
from PyQt5 import QtCore
import ApiCalls
from vkObjects import convestationsObject
import tools
from threading import Thread
import time



class DialogListWidgetPanel(QtWidgets.QWidget):
  def __init__(self,parent):
    super(QtWidgets.QWidget, self).__init__(parent)
    self.ImageLabel=QtWidgets.QLabel()
    self.mainLayout = QtWidgets.QHBoxLayout()
    self.innerlayout=QtWidgets.QVBoxLayout()

    self.TitleLabel=QtWidgets.QLabel()
    self.TitleLabel.setStyleSheet("font-weight: bold; color: black")
    self.TextLabel= QtWidgets.QLabel()
    self.innerlayout.addWidget(self.TitleLabel)
    self.innerlayout.addWidget(self.TextLabel)
    

    self.mainLayout.addWidget(self.ImageLabel)
    self.mainLayout.addLayout(self.innerlayout)
    self.setLayout(self.mainLayout)
    self.innerlayout.addStretch()
    self.mainLayout.addStretch()
   

  def setText(self, text):
    self.TextLabel.setText(text)
  def setTitleText(self, text):
    self.TitleLabel.setText(text)
  def setImage(self, image:QtGui.QPixmap):
    self.ImageLabel.setPixmap(image)
    self.ImageLabel.setFixedSize(QtCore.QSize(50,50))
    

  

class DialogListWidget(QtWidgets.QWidget):
     trigger = QtCore.pyqtSignal(str,str)
     offset=0
     count=0

     def __init__(self, parent):
         super(QtWidgets.QWidget, self).__init__(parent)
         self.trigger.connect(self.loadedSlot)  
         self.loader=tools.LoadImage()
         t=Thread(target=self.LoadDialogs,args=(100,self.offset))
         t.isDaemon=True
         t.start()
         self.layout = QtWidgets.QVBoxLayout(self)
         self.listview = QtWidgets.QListWidget()
         self.Vscroll= QtWidgets.QScrollBar()
         self.Vscroll.valueChanged.connect(self.Vscrolled)
       
         self.listview.setVerticalScrollBar(self.Vscroll)
         self.setLayout(self.layout)
         self.layout.addWidget(self.listview)

     def Vscrolled(self,i):
        if(self.Vscroll.maximum()==i):
          if(self.offset!=self.count):
           t=Thread(target=self.LoadDialogs,args=(100,self.offset))
           t.isDaemon=True
           t.start() 
     def loadedSlot(self,title,text):
       item= QtWidgets.QListWidgetItem()
      
       w=DialogListWidgetPanel(self)
       w.setText(text)
       w.setTitleText(title)
       item.setSizeHint(w.sizeHint()) 
       self.listview.addItem(item)
       self.listview.setItemWidget(item,w)
       
      
     def LoadDialogs(self,count,offset):
        Converstations=ApiCalls.Messages.get(count,offset,1)
        self.count=Converstations.response.count
        for i in range(0,len(Converstations.response.items)):
          
            
            if (str(Converstations.response.items[i].conversation.peer.type)=="TypeEnum.CHAT"):
              self.LoadChatDialog(Converstations,i)
            elif (str(Converstations.response.items[i].conversation.peer.type)=="TypeEnum.USER"):
              self.LoadUserDialog(Converstations,i)
            else:
              self.LoadGroupDialog(Converstations,i)
         
      
        time.sleep(1)
        for i in range(0,len(Converstations.response.items)):
          try:
              if (str(Converstations.response.items[i].conversation.peer.type)=="TypeEnum.CHAT"):
                tz=Thread(target= self.LoadChatImage,args=(Converstations,i))
                tz.start()
              elif (str(Converstations.response.items[i].conversation.peer.type)=="TypeEnum.USER"):
                tz=Thread(target= self.LoadUserImage,args=(Converstations,i))
                tz.start()
              else:
                tz=Thread(target=  self.loadGroupImage,args=(Converstations,i))
                tz.start()
          except:pass
        self.offset=self.offset+ len(Converstations.response.items)
          
      
     def loadGroupImage(self,conversations:convestationsObject.Convestation,index:int):
       conversation=conversations.response.items[index].conversation
       for i in range(0,len(conversations.response.groups)):
         group=conversations.response.groups[i]
         if(conversation.peer.id*-1==group.id):
           if(group.photo_50!=None):
            w:DialogListWidgetPanel=self.listview.itemWidget(self.listview.item(self.offset+index))
            w.setImage(self.loader.Loadimage(group.photo_50))
            time.sleep(0.1)
            break

     def LoadUserImage(self,conversations:convestationsObject.Convestation,index:int):
       if( len(conversations.response.items[index].last_message.fwd_messages)>0):
         textMessage="[Пересланные сообщения]"
       else:
         textMessage= conversations.response.items[index].last_message.text
       conversation=conversations.response.items[index].conversation
       for i in range(0,len(conversations.response.profiles)):
         profile=conversations.response.profiles[i]
         if(conversation.peer.id==profile.id):
            w:DialogListWidgetPanel=self.listview.itemWidget(self.listview.item(self.offset+index))
            w.setImage(self.loader.Loadimage(profile.photo_50))
            time.sleep(0.1)
            break

     def LoadChatImage(self,conversations:convestationsObject.Convestation,index:int):
         conversation=conversations.response.items[index]
         if(conversation.conversation.chat_settings.photo!=None):
          w=self.listview.itemWidget(self.listview.item(self.offset+index))
          w.setImage(self.loader.Loadimage(conversation.conversation.chat_settings.photo.photo_50))
          time.sleep(0.1)
         

     def startloadImage(self,url):
       self.loader.Loadimage(url)

     def LoadGroupDialog(self,conversations:convestationsObject.Convestation,index:int):
       if( len(conversations.response.items[index].last_message.fwd_messages)>0):
         textMessage="[Пересланные сообщения]"
       elif(len(conversations.response.items[index].last_message.attachments)>0):
         if(len(conversations.response.items[index].last_message.attachments)==1):
           textMessage="Вложение"
         else:
           textMessage="[Вложения]"
       else:
         textMessage= conversations.response.items[index].last_message.text
       conversation=conversations.response.items[index].conversation

       for i in range(0,len(conversations.response.groups)):
         group=conversations.response.groups[i]
         if(conversation.peer.id*-1==group.id):

           title=group.name+"[Группа]"
          
           self.trigger.emit(title,textMessage)
           break
         
     # Получение данных о юзере
     def LoadUserDialog(self,conversations:convestationsObject.Convestation,index:int):
       if( len(conversations.response.items[index].last_message.fwd_messages)>0):
         textMessage="[Пересланные сообщения]"
       
       elif(len(conversations.response.items[index].last_message.attachments)>0):
         if(len(conversations.response.items[index].last_message.attachments)==1):
           textMessage="Вложение"
         else:
           textMessage="[Вложения]"

       else:
         textMessage= conversations.response.items[index].last_message.text
       conversation=conversations.response.items[index].conversation

       for i in range(0,len(conversations.response.profiles)):
         profile=conversations.response.profiles[i]
         if(conversation.peer.id==profile.id):
          
           title=profile.first_name+" "+profile.last_name+"[Пользователь]"
           
           self.trigger.emit(title,textMessage)
           break

     def LoadChatDialog(self,conversations:convestationsObject.Convestation,index:int):
       photo=""
       try: 
         conversation=conversations.response.items[index]

         if( len(conversations.response.items[index].last_message.fwd_messages)>0):
            textMessage="[Пересланные сообщения]"
         elif(len(conversations.response.items[index].last_message.attachments)>0):
          if(len(conversations.response.items[index].last_message.attachments)==1):
           textMessage="Вложение"
          else:
           textMessage="[Вложения]"

         else:
            textMessage= conversations.response.items[index].last_message.text


         text=conversation.last_message.text
         title=conversation.conversation.chat_settings.title+"[Беседа]"
         self.trigger.emit(title,text)
       except Exception as  e:
         print(e)
