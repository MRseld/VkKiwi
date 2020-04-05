
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import ApiCalls
import tools
import threading 
import time
from DialogWidget import DialogWidget
from multiprocessing import Process
import settings
        
class DialogListWidgetPanel(QtWidgets.QWidget):
    def __init__(self, parent):
        super(DialogListWidgetPanel, self).__init__(parent)
        self.ID=0
        self.ImageLabel=QtWidgets.QLabel()
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.innerlayout = QtWidgets.QVBoxLayout()
        self.unreadCount=0
        self.unreadCountsLabel=QtWidgets.QLabel()
        self.TitleLabel = QtWidgets.QLabel()
        self.TitleLabel.setStyleSheet("font-weight: bold; color: black")
        self.TextLabel = QtWidgets.QLabel()
        #self.TextLabel.setStyleSheet("font-style:italic; color: #859900")
    
        self.innerlayout.addWidget(self.TitleLabel)
        self.innerlayout.addWidget(self.TextLabel)
        
        self.mainLayout.addWidget(self.ImageLabel)
        self.mainLayout.addLayout(self.innerlayout)
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.unreadCountsLabel)
        self.innerlayout.addStretch()
            
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
        self.setUnreadCountLabelValue("("+str(self.unreadCount)+")")
      elif self.unreadCount==0:
          self.setUnreadCountLabelValue("")

    def setUnreadCountLabelValue(self,count):
      self.unreadCountsLabel.setText(str(count))

    def setText(self, text):
        self.TextLabel.setText(text)

    def setTitleText(self, text):
        self.TitleLabel.setText(text)

    def setId(self,value:int):
      self.ID=value
    def setImage(self, image: QtGui.QPixmap,round:bool==False):
        if(round==True):
            
            image=tools.RoundImage(image,True,100,50,50).getImage()
       
       
        self.ImageLabel.setPixmap(image)
        self.ImageLabel.setFixedSize(QtCore.QSize(50, 50))


class DialogListWidget(QtWidgets.QWidget):
    
    MApi= ApiCalls.Messages()
    WlistWidgets=list()
    trigger = QtCore.Signal(int,int,str, str,str)
    
    newoffset = 0
    oldoffset=0
    count = 0

    def __init__(self, parent):
        self.LoadingGifStarted=False
        self.loadingsImage=False
        super(DialogListWidget, self).__init__(parent)
        self.Conversations=None
       
        #self.standartImage=QtGui.QPixmap("NP.jpg")
       
        self.trigger.connect(self.loadedSlot)
        

        self.loader = tools.LoadImage()
        self.standartImage=self.loader.Loadimage("https://vk.com/images/icons/im_multichat_50.png")
   

        self.timerQ = QtCore.QTimer(self)
        self.timerQ.timeout.connect(self.check)
        self.timerQ.start(50)

        self.timerQP = QtCore.QTimer(self)
        self.timerQP.timeout.connect(self.LoadingGif)
        self.timerQP.start(100)

        self.loadingLabel=QtWidgets.QLabel()
        self.loadingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loadgif=QtGui.QMovie("progress_gray.gif")
        self.loadingLabel.setMovie(self.loadgif)
        self.loadingLabel.setStyleSheet("text-align:  center;")
        


        t =threading.Thread(target=self.LoadDialogs, args=(50,0))
        t.start()

        

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.loadingLabel)
        self.listview = QtWidgets.QListWidget()
        #self.listview.setStyleSheet("background: #282828")
  
       

        self.Vscroll = QtWidgets.QScrollBar()
        self.Vscroll.valueChanged.connect(self.Vscrolled)
        self.listview.setVerticalScrollBar(self.Vscroll)
        

        self.setLayout(self.layout)

        self.layout.addWidget(self.listview)
        lt=threading.Thread(target=self.LongPollStart)
        
        lt.start()
   
       


    def updateElement(self,oldPanel:DialogListWidgetPanel,item):

        w = DialogListWidgetPanel(self)
        print(oldPanel.getTitle())
        w.setId(oldPanel.getID())
        w.setText(oldPanel.getText())
        w.setTitleText(oldPanel.getTitle())
        w.setImage(oldPanel.getPixmap(),False)
        w.setUnreadCount(oldPanel.getUnreadCount())
        self.listview.setItemWidget(item,w)
   

    def LoadingGif(self):
        if self.LoadingGifStarted==False:
            if self.loading==True:
                self.loadingLabel.show()
                self.loadgif.start()
                self.LoadingGifStarted=True
        else:
            if self.loading==False:
                self.loadgif.stop()
                self.loadingLabel.hide()
                self.LoadingGifStarted=False

    def GetFlags(self,Flags):
        t=Flags
        """
        'UNREAD':1,'OUTBOX':2,'REPLIED':4,'IMPORTANT':8,'CHAT':16,'FRIENDS':32,'SPAM':64,
        'DELETED':128,'FIXED':256,'MEDIA':512,'UNKNOWN1':1024,'UNKNOWN2':2048,'UNKNOWN3':4096,
        'UNREAD_MULTICHAT':8192, 'UNKNOWN4':16384,'UNKNOWN5': 32768,'HIDDEN':65536,'DELETE_FOR_ALL':131072,
        'NOT_DELIVERED':262144,'UNKNOWN6':524288,'UNKNOWN7':1048576,'UNKNOWN8':2097152,'UNKNOWN9':4194304
        """
        correctFlags=[]

        FLAGS={'UNKNOWN9':4194304,'UNKNOWN8':2097152,'UNKNOWN7':1048576,'UNKNOWN6':524288,
        'NOT_DELIVERED':262144,'DELETE_FOR_ALL':131072,'HIDDEN':65536,'UNKNOWN5': 32768,'UNKNOWN4':16384,
        'UNREAD_MULTICHAT':8192,'UNKNOWN3':4096,'UNKNOWN2':2048,'UNKNOWN1':1024,'MEDIA':512,'FIXED':256,'DELETED':128,
        'SPAM':64,'FRIENDS':32,'CHAT':16,'IMPORTANT':8,'REPLIED':4,'OUTBOX':2, 'UNREAD':1}
        for flag in FLAGS:
            if t - int(FLAGS[flag])>0:
                t=t - int(FLAGS[flag])
                correctFlags.append(flag)
        return correctFlags
                
                
            

    def newMessageSlot(self,index,object):
        
        
        for i in range(0,self.listview.count()):

              w: DialogListWidgetPanel = self.listview.itemWidget(
                        self.listview.item(i))
              if w!=None:

                if(object["updates"][index][3]==w.getID()):
                    if object["updates"][index][5]!=None:
                        w.setText(object["updates"][index][5])

                    if "attach1_type" in object["updates"][index][7]:
                        w.setText(object["updates"][index][7]["attach1_type"])

                    if "OUTBOX" in  self.GetFlags (object["updates"][index][2]):
                        w.setUnreadCount(0)
                
                    else:w.setUnreadCount(w.getUnreadCount()+1)
                    
              
                    item:QtWidgets.QListWidgetItem=self.listview.item(i) 

                    self.listview.takeItem(i)
                    self.listview.insertItem(0,item)   
                    self.updateElement(w,item)
               
                    break
    
    def dialogIsreadSlot(self,index,object:dict):
       if self.loading==False:

        for i in range(0,self.listview.count()):
            w: DialogListWidgetPanel = self.listview.itemWidget(
                        self.listview.item(i))

            if(object["updates"][index][1]==w.getID()):
                w.setUnreadCount(0)
                w.update()
                break
     
    def LongPollStart(self):

        LPApi=tools.longPollQT()
        LPApi.getLongPollServer()
        LPApi.setMode(10)
        LPApi.newMessageSignal.connect(self.newMessageSlot)
        LPApi.dialogIsreadSignal.connect(self.dialogIsreadSlot)
        while True:
            while self.loading==True:
                time.sleep(0.2)
            LPApi.update()

    def Vscrolled(self, i):
        if(self.Vscroll.maximum() == i):
            if(self.newoffset != self.count):
                if self.loading==False:
                    t = threading.Thread(target=self.LoadDialogs, args=(50, self.newoffset))
                    t.start()

    def loadImageThread(self, panel:DialogListWidgetPanel,url):
        panel.setImage(self.loader.Loadimage(url),True)
       

    def loadedSlot(self,id, unreadcount, title, text,imageUrl):
        item = QtWidgets.QListWidgetItem()
         

        w = DialogListWidgetPanel(self)
        self.WlistWidgets.append(w)
        w.setId(id)
        w.setText(text)
        w.setTitleText(title)
        w.setImage(self.standartImage,True)
      
        
        w.setUnreadCount(unreadcount)
        item.setSizeHint(QtCore.QSize(w.width(),60))
        self.listview.addItem(item)
        self.listview.setItemWidget(item, w)

    def check(self):
      k:bool=False
      if(self.loadingsImage==True):
          for i in  range(0,len(self.Conversations["response"]["items"])):
              w: DialogListWidgetPanel = self.listview.itemWidget(
                            self.listview.item(self.oldoffset+i))
              if w==None:
                  k=True
                  break

          if k!=True:
              threading.Thread(target= self.ImageLoadings()).start()
              self.loadingsImage==False

    
    def ImageLoadings(self):
        print("start loading iMAGE")
        for i in range(0, len(self.Conversations["response"]["items"])):
            try:
                if (str(self.Conversations["response"]["items"][i]["conversation"]["peer"]["type"]) == "chat"):
                   
                    tz = threading.Thread(target=self.LoadChatImage,
                               args=( i,))
                    tz.start()
                    
                elif (str(self.Conversations["response"]["items"][i]["conversation"]["peer"]["type"]) == "user"):
                    tz = threading.Thread(target=self.LoadUserImage,args=(i,))
                    tz.start()
   
                else:
                    tz =threading.Thread(target=self.loadGroupImage,args=( i,))
                    tz.start()
         
            except Exception as ex:
             print(str(ex))

        self.oldoffset = self.oldoffset + len(self.Conversations["response"]["items"])
        self.loading=False

    def LoadDialogs(self, count, offset):
        self.loading=True
        
        self.Conversations = self.MApi.get(count, offset, 1)
        self.count = self.Conversations["response"]["count"]
        
        for i in range(0, len(self.Conversations["response"]["items"])):
            time.sleep(0.03)
          
            if (str(self.Conversations["response"]["items"][i]["conversation"]["peer"]["type"]) == "chat"):
            
                    self.LoadChatDialog(i)
                       
     
            elif (str(self.Conversations["response"]["items"][i]["conversation"]["peer"]["type"]) == "user"):
                        
                        self.LoadUserDialog(i)
                          
            else:   
                   
                    self.LoadGroupDialog(i)
 
        self.newoffset = self.newoffset + len(self.Conversations["response"]["items"])
        self.loadingsImage=True
        
        
       

    def loadGroupImage(self, index):
        
            conversation = self.Conversations["response"]["items"][index]["conversation"]
            for i in range(0, len(self.Conversations["response"]["groups"])):
                group = self.Conversations["response"]["groups"][i]
                if(int(conversation["peer"]["id"])*-1 == group["id"]):
                    if "photo_50" in group:
    
                        w: DialogListWidgetPanel = self.listview.itemWidget(
                            self.listview.item(self.oldoffset+index))
                        
                        w.setImage(self.loader.Loadimage(group["photo_50"]),True)
                        
                        break

    def LoadUserImage(self,  index):
        
           
            conversation =self.Conversations["response"]["items"][index]["conversation"]
            for i in range(0, len(self.Conversations["response"]["profiles"])):
                profile = self.Conversations["response"]["profiles"][i]
                if(conversation["peer"]["id"] == profile["id"]):

                    w: DialogListWidgetPanel = self.listview.itemWidget(
                            self.listview.item(self.oldoffset+index))
                  
                   
                    w.setImage(self.loader.Loadimage(profile["photo_50"]),True)
                    
                    break
        

    def LoadChatImage(self,  index):
            
            conversation =self.Conversations["response"]["items"][index]["conversation"]
            if("photo" in  conversation["chat_settings"]):
           
                w: DialogListWidgetPanel = self.listview.itemWidget(
                        self.listview.item(self.oldoffset+index))

                
                w.setImage(self.loader.Loadimage(conversation["chat_settings"]["photo"]["photo_50"]),True)


    def LoadGroupDialog(self, index: int):
        if(len(self.Conversations["response"]["items"][index]["last_message"]["fwd_messages"]) > 0):
            textMessage = "[Пересланные сообщения]"
        elif(len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) > 0):
            if(len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) == 1):
                textMessage = "Вложение"
            else:
                textMessage = "[Вложения]"
        else:
            textMessage = self.Conversations["response"]["items"][index]["last_message"]["text"]
        conversation = self.Conversations["response"]["items"][index]["conversation"]

        for i in range(0, len(self.Conversations["response"]["groups"])):
            group = self.Conversations["response"]["groups"][i]
            if(conversation["peer"]["id"]*-1 == group["id"]):

                title = group["name"]+"[Группа]"

                
                if "unread_count" in conversation:
                    self.trigger.emit(group["id"], conversation["unread_count"], title, textMessage,group["photo_50"])
                else:
                    self.trigger.emit(group["id"], 0, title, textMessage,group["photo_50"])
                
                break

    def LoadUserDialog(self,  index: int):
        if(len(self.Conversations["response"]["items"][index]["last_message"]["fwd_messages"])> 0):
            textMessage = "[Пересланные сообщения]"

        elif(len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) > 0):
            if(len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) == 1):
                textMessage = "[Вложение]"
            else:
                textMessage = "[Вложения]"

        else:
            textMessage = self.Conversations["response"]["items"][index]["last_message"]["text"]
        conversation = self.Conversations["response"]["items"][index]["conversation"]

        for i in range(0, len(self.Conversations["response"]["profiles"])):
            profile = self.Conversations["response"]["profiles"][i]
            if(conversation["peer"]["id"] == profile["id"]):

                title = profile["first_name"]+" " + \
                    profile["last_name"]+"[Пользователь]"
                
                if("unread_count"in conversation):
                        self.trigger.emit(profile["id"],conversation["unread_count"], title, textMessage,profile["photo_50"])
                  
                else:
                  self.trigger.emit(profile["id"],0, title, textMessage,profile["photo_50"])

              
                break
                

    def LoadChatDialog(self, index: int):
      
            conversation =self.Conversations["response"]["items"][index]

            if(len(self.Conversations["response"]["items"][index]["last_message"]["fwd_messages"]) > 0):
                textMessage = "[Пересланные сообщения]"
            elif(len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) > 0):
                if(len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) == 1):
                    textMessage = "Вложение"
                else:
                    textMessage = "[Вложения]"

            else:
                textMessage = self.Conversations["response"]["items"][index]["last_message"]["text"]

            text = conversation["last_message"]["text"]
            title = conversation["conversation"]["chat_settings"]["title"]+"[Беседа]"
            if("photo" in conversation["conversation"]["chat_settings"]):
                Ucount=0
                if "unread_count" in conversation["conversation"]:
                    Ucount=int(conversation["conversation"]["unread_count"])
                    
              
                self.trigger.emit(conversation["conversation"]["peer"]["id"], 
                Ucount, title, textMessage,
                conversation["conversation"]["chat_settings"]["photo"]["photo_50"])
                
            else:
                Ucount=0
                if "unread_count" in conversation["conversation"]:
                    Ucount=int(conversation["conversation"]["unread_count"])

                self.trigger.emit(conversation["conversation"]["peer"]["id"], 
                Ucount, title, textMessage,
                None)




           
            
        

    