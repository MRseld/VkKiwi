from PySide2  import QtGui 
from PySide2 import QtCore
from PySide2 import QtWidgets 
import tools
import ApiCalls
import AudioPlayer
import time
import threading
import settings

class AudioSlider(QtWidgets.QSlider):
    def __init__(self, orientation, parent):
        super().__init__(orientation, parent)
        self.setOrientation(orientation)
        self.setStyleSheet("QSlider::groove:horizontal {\
          border: 1px solid black;\
          height: 8px;\
          }\
          QSlider::handle:horizontal {\
              width: 10px; \
              height: 8px;\
              background: white;\
              border-radius:4px;\
          }\
          QSlider::add-page:qlineargradient {\
                  background: lightgrey;\
                  margin:1px\
         }\
         QSlider::sub-page:qlineargradient {\
                      background: black;\
                          margin:1px;}")

    def enterEvent (self,enterEvent ):
        self.setStyleSheet("QSlider::groove:horizontal {\
          border: 1px solid black;\
          height: 8px;\
          }\
          QSlider::handle:horizontal {\
              width: 10px; \
              height: 8px;\
              background: white;\
              border-radius:4px;\
          }\
          QSlider::add-page:qlineargradient {\
                  background: lightgrey;\
                  margin:1px\
         }\
         QSlider::sub-page:qlineargradient {\
                      background: black;\
                          margin:1px;}")

    def mousePressEvent(self, event):
        super(AudioSlider, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def pixelPosToRangeValue(self, pos):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderHandle, self)

        if self.orientation() == QtCore.Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1;
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == QtCore.Qt.Horizontal else pr.y()
        return QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)

    def leaveEvent(self,leaveEvent):
         self.setStyleSheet("QSlider::groove:horizontal {\
          border: 1px solid black;\
          height: 8px;\
          }\
          QSlider::handle:horizontal {\
              height: 8px;\
              background: black;\
          }\
          QSlider::add-page:qlineargradient {\
                  background: lightgrey;\
         }\
         QSlider::sub-page:qlineargradient {\
                      background: black;\
                          }")

class HTMLDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HTMLDelegate, self).__init__(parent)
        self.doc = QtGui.QTextDocument(self)


    def paint(self, painter, option, index):
        painter.save()
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setHtml(options.text)
        options.text = ""
        style = QtWidgets.QApplication.style() if options.widget is None \
            else options.widget.style()
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, options, painter)

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
        if option.state & QtWidgets.QStyle.State_Selected:
            ctx.palette.setColor(QtGui.QPalette.Text, option.palette.color(
                QtGui.QPalette.Active, QtGui.QPalette.HighlightedText))
        else:
            ctx.palette.setColor(QtGui.QPalette.Text, option.palette.color(
                QtGui.QPalette.Active, QtGui.QPalette.Text))
        textRect = style.subElementRect(QtWidgets.QStyle.SE_ItemViewItemText, options, None)
        if index.column() != 0:
            textRect.adjust(5, 0, 0, 0)
        constant = 4
        margin = (option.rect.height() - options.fontMetrics.height()) // 2
        margin = margin - constant
        textRect.setTop(textRect.top() + margin)

        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        self.doc.documentLayout().draw(painter, ctx)
        painter.restore()

class ClickeDLabel(QtWidgets.QLabel):
    clicked= QtCore.Signal(QtGui.QMouseEvent)
    def mousePressEvent(self, ev):
        self.clicked.emit(ev)
    

class AudioListWidget(QtWidgets.QWidget):
    audio= ApiCalls.Audios()

    def __init__(self, parent, ):
      super(AudioListWidget,self).__init__(parent)
      self.MyPlayLists=[]
      self.ActiveAudioList=None;
      self.loaddatatImage=[]
      self.LoadingGifStarted=False
      self.loading=False

      self.Playing=False;


      self.MainLayout=QtWidgets.QVBoxLayout()
      self.audioListWidget=QtWidgets.QListWidget()
      self.audioListWidget.itemClicked.connect(self.audioListItemClicked)

      self.audioPlaylistsListWIdget=QtWidgets.QListWidget()

      self.audioPlaylistsListWIdget.itemClicked.connect(self.playlistItemClicker)

      self.mediaPanel=QtWidgets.QVBoxLayout()

      self.ControlPanel=QtWidgets.QHBoxLayout()
      self.ControlPanel.setAlignment(QtCore.Qt.AlignLeft)

      self.stopAndPLayIconLabel=ClickeDLabel()
      self.backAudioIconLabel=ClickeDLabel()
      self.nextAudioIconLabel=ClickeDLabel()
      self.durationLabel=QtWidgets.QLabel("0");
      self.AudioTitleLabel=QtWidgets.QLabel()

      self.playlistIconHandler=tools.ImageHandler()
      self.playlistIconHandler.setimageFromPath("icons/playlist.png")

      self.stopIconHandler=tools.ImageHandler()
      self.stopIconHandler.setimageFromPath("icons/audiostop.png")
      self.playIconHandler=tools.ImageHandler()
        
      self.playIconHandler.setimageFromPath("icons/audioplay.png")

      self.backAudioIconHandler=tools.ImageHandler()
      self.backAudioIconHandler.setimageFromPath("icons/audioback.png")

      self.nextAudioIconHandler=tools.ImageHandler()
      self.nextAudioIconHandler.setimageFromPath("icons/audionext.png")

      self.stopAndPLayIconLabel.setPixmap(self.stopIconHandler.getImage())
      self.backAudioIconLabel.setPixmap(self.backAudioIconHandler.getImage())
      self.nextAudioIconLabel.setPixmap(self.nextAudioIconHandler.getImage())

      self.audioslider=AudioSlider(QtGui.Qt.Orientation.Horizontal,self)
          

      self.ControlPanel.addWidget(self.backAudioIconLabel)
      self.ControlPanel.addWidget(self.stopAndPLayIconLabel)
      self.ControlPanel.addWidget(self.nextAudioIconLabel)
      self.ControlPanel.addLayout(self.mediaPanel)

      self.ControlPanel.addWidget(self.durationLabel)

      
      self.mediaPanel.addWidget(self.AudioTitleLabel)
      self.mediaPanel.addWidget(self.audioslider)
      
      

      self.MainLayout.addLayout(self.ControlPanel)
      self.MainLayout.addWidget(self.audioListWidget)
      self.MainLayout.addWidget(self.audioPlaylistsListWIdget)

      self.setLayout(self.MainLayout)

      self.audioListWidget.setIconSize(QtCore.QSize(32,32))
      self.audioPlaylistsListWIdget.setIconSize(QtCore.QSize(32,32))

      delegate = HTMLDelegate(self.audioListWidget)
      self.audioListWidget.setItemDelegate(delegate)

      AudioPlayer.player.positionChanged.connect(self.positionChanged)
      AudioPlayer.player.durationChanged.connect(self.durationChanged)

    def nextAudioClick(self,event):
       pass
    
    def backAudioClick(self,event):
        pass
    def playPauseClick(self,event):
        pass

    def playlistItemClicker(self,item):
       self.audioListWidget.clear()
       self.audioListWidget.update()
       self.audioListWidget.updateGeometry()
       time.sleep(0.00001)
       itemid:int= self.audioPlaylistsListWIdget.row(item)
       items:dict=self.MyPlayLists;
       if(itemid>0):
        idd=items[itemid-1]["id"]
        threading.Thread(target= self.uploadingAudioFromAnAlbum,args=(10000,0,idd)).start()
       else:
        threading.Thread(target= self.loadingAudios,args=(10000,0)).start()
        

    def audioListItemClicked(self,item):
       itemid:int=self.audioListWidget.row(item)
       items:dict=self.ActiveAudioList;
       audio:dict= self.audio.getById(items[itemid]["owner_id"],items[itemid]["id"])
       audio=audio["response"]

       self.startPlay(audio)
    def startPlay(self,audio):
        print(str(audio))
       
        self.audioslider.setValue(0);
        self.AudioTitleLabel.setText(audio[0]["artist"]+"\n"+audio[0]["title"])
        AudioPlayer.setAudio( audio[0]["url"]);
        AudioPlayer.setVolume(50)
        AudioPlayer.play()

    def positionChanged(self,data):
        n=data/1000
        d=int(n) 
        minutes=int(d/60)
        seconds=int(d%60)
        Ptime=str(minutes)+":"+str(seconds)

        n=AudioPlayer.activeDuration/1000
        d=int(n) 
        minutes=int(d/60)
        seconds=int(d%60)

        Dtime=str(minutes)+":"+str(seconds)

        self.durationLabel.setText(Ptime +"/"+Dtime)
        self.audioslider.setValue(data)

    def durationChanged(self,data):
       self.audioslider.setMaximum(data)
       print("duration "+str(data))
       n=data/1000
       d=int(n) 
       minutes=int(d/60)
       seconds=int(d%60)
       Dtime=str(minutes)+":"+str(seconds)
       self.durationLabel.setText("0/"+Dtime)
       AudioPlayer.activeDuration=data;

    def uploadingAudioFromAnAlbum(self,count,offset,albumID):
       audioList=self.audio.get(count,offset,None,albumID)
       self.ActiveAudioList=audioList["response"]["items"]
       for k in  audioList["response"]["items"]:
              item=QtWidgets.QListWidgetItem(self.playIconHandler.getImage(), 
              "<p><b>"+k['artist']+"</b><br> "+k["title"]+"</br></p>")
              item.setSizeHint(QtCore.QSize(50,40))
              self.audioListWidget.addItem(item)
       

    def loadingAudios(self,count,offset):
         audioList= self.audio.get(count,offset)
         self.ActiveAudioList=audioList["response"]["items"]
         for k in  audioList["response"]["items"]:
              item=QtWidgets.QListWidgetItem(self.playIconHandler.getImage(), 
              "<p><b>"+k['artist']+"</b><br> "+k["title"]+"</br></p>")
              item.setSizeHint(QtCore.QSize(50,40))
              self.audioListWidget.addItem(item)
       
             
    def loadingAlbums(self,count,offset):
         audioList= self.audio.getAlbums(count,offset,None)
         if(len(audioList["response"]["items"])>0):
             self.MyPlayLists=audioList["response"]["items"]

             item=QtWidgets.QListWidgetItem(self.playlistIconHandler.getImage(),"Мои аудио")
             self.audioPlaylistsListWIdget.addItem(item)

             for k in  audioList["response"]["items"]:
                item=QtWidgets.QListWidgetItem(self.playlistIconHandler.getImage(),k["title"])
                self.audioPlaylistsListWIdget.addItem(item)


            
    
        
    