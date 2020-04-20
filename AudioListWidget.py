from PySide2  import QtGui 
from PySide2 import QtCore
from PySide2 import QtWidgets 
import tools
import ApiCalls
import AudioPlayer
import time
import threading

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

class AudioListWidget(QtWidgets.QWidget):
   audio= ApiCalls.Audios()

   def __init__(self, parent, ):
      super(AudioListWidget,self).__init__(parent)
      self.MyAudioOS=None;
      self.ActiveAudioList=None;
      self.loaddatatImage=[]
      self.LoadingGifStarted=False
      self.loading=False

      self.Playing=False;


      self.MainLayout=QtWidgets.QVBoxLayout()
      self.audioListWidget=QtWidgets.QListWidget()
      self.audioListWidget.itemClicked.connect(self.audioListItemClicked)
      self.audioPlaylistsListWIdget=QtWidgets.QListWidget();
      self.ControlPanel=QtWidgets.QHBoxLayout()
      self.ControlPanel.setAlignment(QtCore.Qt.AlignLeft)

      self.stopAndPLayIconLabel=QtWidgets.QLabel()
      self.backAudioIconLabel=QtWidgets.QLabel()
      self.nextAudioIconLabel=QtWidgets.QLabel()

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

      self.ControlPanel.addWidget(self.backAudioIconLabel)
      self.ControlPanel.addWidget(self.stopAndPLayIconLabel)
      self.ControlPanel.addWidget(self.nextAudioIconLabel)


      self.MainLayout.addLayout(self.ControlPanel)
      self.MainLayout.addWidget(self.audioListWidget)
      self.MainLayout.addWidget(self.audioPlaylistsListWIdget)

      self.setLayout(self.MainLayout)
      self.audioListWidget.setIconSize(QtCore.QSize(32,32))
      self.audioPlaylistsListWIdget.setIconSize(QtCore.QSize(32,32))

      delegate = HTMLDelegate(self.audioListWidget)
      self.audioListWidget.setItemDelegate(delegate)
     


   def audioListItemClicked(self,item):
       itemid:int=self.audioListWidget.row(item)
       item:dict=self.ActiveAudioList["response"]["items"][itemid]
       audio:dict= self.audio.getById(item["owner_id"],item["id"])["response"][0]
       AudioPlayer.setAudio( audio ["url"]);
       AudioPlayer.setVolume(50)
       AudioPlayer.play()
     

   
   def loadingAudios(self,count,offset):
         audioList= self.audio.get(count,offset)
         if(self.MyAudioOS==None):
             self.MyAudioOS=audioList;
             self.ActiveAudioList=self.MyAudioOS;

         for k in  audioList["response"]["items"]:
              item=QtWidgets.QListWidgetItem(self.playIconHandler.getImage(), 
              "<p><b>"+k['artist']+"</b><br> "+k["title"]+"</br></p>")
              item.setSizeHint(QtCore.QSize(50,40))
              self.audioListWidget.addItem(item)
       
             
   def loadingAlbums(self,count,offset):
         audioList= self.audio.getAlbums(count,offset,None)
         for k in  audioList["response"]["items"]:
            item=QtWidgets.QListWidgetItem(self.playlistIconHandler.getImage(),k["title"])
            self.audioPlaylistsListWIdget.addItem(item)


            
    
        
    