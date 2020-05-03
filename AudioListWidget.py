import threading
import time

import ApiCalls
import AudioPlayer
import tools
from  CustomObjects import  *


class listWidgetAudio(QtWidgets.QWidget):
    audio = ApiCalls.Audios()


    def __init__(self, parent, ):
        super(listWidgetAudio, self).__init__(parent)
        self.listPlayLists = []
        self.listAudios = None
        self.playIndex = 0

        self.layoutMain = QtWidgets.QVBoxLayout()
        self.listWidgetAudio = QtWidgets.QListWidget()
        self.listWidgetPlayLists = QtWidgets.QListWidget()
        self.panelMedia = QtWidgets.QVBoxLayout()
        self.layoutControlPanel = QtWidgets.QHBoxLayout()
        self.labelPlayPauseIcon =СlickableLabel()
        self.labelBackAudioIcon =СlickableLabel()
        self.labelAudioNextIcon =СlickableLabel()
        self.labelDuration = QtWidgets.QLabel("0");
        self.labelAudioTitle = QtWidgets.QLabel()
        self.sliderAudio = AudioSlider(QtGui.Qt.Orientation.Horizontal, self)
        self.imageHandlerPlaylist = tools.ImageHandler()
        self.imageHandlerStop = tools.ImageHandler()
        self.imageHandlerPlay = tools.ImageHandler()
        self.imageHandlerAudioBack = tools.ImageHandler()
        self.imageHandlerAudioNext = tools.ImageHandler()
        self.setLayout(self.layoutMain)

        self.listWidgetAudio.setIconSize(QtCore.QSize(32, 32))
        self.listWidgetPlayLists.setIconSize(QtCore.QSize(32, 32))
        delegate = HTMLDelegate(self.listWidgetAudio)
        self.listWidgetAudio.setItemDelegate(delegate)

        self.init_slots()
        self.init_images()
        self.init_layouts()

    def init_slots(self):
        self.listWidgetAudio.itemClicked.connect(self.listWidgetAudio_item_click)
        self.listWidgetPlayLists.itemClicked.connect(self.listWidgetPlayLists_item_click)
        self.layoutControlPanel.setAlignment(QtCore.Qt.AlignLeft)

        self.labelPlayPauseIcon.clicked.connect(self.labelPlayPauseIcon_click)
        self.labelBackAudioIcon.clicked.connect(self.labelBackAudioIcon_click)
        self.labelAudioNextIcon.clicked.connect(self.labelAudioNextIcon_click)
        self.sliderAudio.clicked.connect(self.sliderAudio_click)

        AudioPlayer.player.positionChanged.connect(self.audioPlayer_position_changed)
        AudioPlayer.player.durationChanged.connect(self.audioPlayer_duration_changed)

    def init_images(self):

        self.imageHandlerPlaylist.set_image_from_path("icons/playlist.png")
        self.imageHandlerStop.set_image_from_path("icons/audiostop.png")
        self.imageHandlerPlay.set_image_from_path("icons/audioplay.png")
        self.imageHandlerAudioBack.set_image_from_path("icons/audioback.png")
        self.imageHandlerAudioNext.set_image_from_path("icons/audionext.png")

        self.labelPlayPauseIcon.setPixmap(self.imageHandlerPlay.get_image())
        self.labelBackAudioIcon.setPixmap(self.imageHandlerAudioBack.get_image())
        self.labelAudioNextIcon.setPixmap(self.imageHandlerAudioNext.get_image())

    def init_layouts(self):
        self.layoutControlPanel.addWidget(self.labelBackAudioIcon)
        self.layoutControlPanel.addWidget(self.labelPlayPauseIcon)
        self.layoutControlPanel.addWidget(self.labelAudioNextIcon)
        self.layoutControlPanel.addLayout(self.panelMedia)
        self.layoutControlPanel.addWidget(self.labelDuration)

        self.panelMedia.addWidget(self.labelAudioTitle)
        self.panelMedia.addWidget(self.sliderAudio)

        self.layoutMain.addLayout(self.layoutControlPanel)
        self.layoutMain.addWidget(self.listWidgetAudio)
        self.layoutMain.addWidget(self.listWidgetPlayLists)

    def listWidgetAudio_clear(self):
        self.listWidgetAudio.clear()
        self.listWidgetAudio.update()
        self.listWidgetAudio.updateGeometry()

    def listWidgetAudio_item_click(self, item):
        itemid: int = self.listWidgetAudio.row(item)
        audio: dict = self.audio.getById(self.listAudios[itemid]["owner_id"], self.listAudios[itemid]["id"])
        self.playIndex = itemid;
        self.start_play(audio)

    def start_play(self, audio):
        self.sliderAudio.setValue(0);
        self.labelAudioTitle.setText(audio["response"][0]["artist"] + "\n" + audio["response"][0]["title"])
        AudioPlayer.setAudio(audio["response"][0]["url"]);
        AudioPlayer.setVolume(50)
        AudioPlayer.play()
        AudioPlayer.playing = True
        self.labelPlayPauseIcon.setPixmap(self.imageHandlerStop.get_image())

    def labelAudioNextIcon_click(self, event):
        if len(self.listAudios) > 0:
            if self.playIndex + 1 < len(self.listAudios):
                self.playIndex = self.playIndex + 1
                audio: dict = self.audio.getById(self.listAudios[self.playIndex]["owner_id"],
                                                 self.listAudios[self.playIndex]["id"])
                self.start_play(audio)

    def labelBackAudioIcon_click(self, event):
        if self.playIndex > 0:
            if len(self.listAudios) > 0:
                self.playIndex = self.playIndex - 1
                audio: dict = self.audio.getById(self.listAudios[self.playIndex]["owner_id"],
                                                 self.listAudios[self.playIndex]["id"])
                self.start_play(audio)

    def labelPlayPauseIcon_click(self, event):
        if AudioPlayer.playing:
            AudioPlayer.pause()
            self.labelPlayPauseIcon.setPixmap(self.imageHandlerPlay.get_image())
            AudioPlayer.playing = False
        else:
            if AudioPlayer.Isloaded():
                AudioPlayer.play()
                AudioPlayer.setPosition(AudioPlayer.getPosition())
                self.labelPlayPauseIcon.setPixmap(self.imageHandlerStop.get_image())
                AudioPlayer.playing = True

    def sliderAudio_click(self, value):
        AudioPlayer.setPosition(value)

    def listWidgetPlayLists_item_click(self, item):
        self.listWidgetAudio_clear()
        time.sleep(0.00001)
        itemid: int = self.listWidgetPlayLists.row(item)
        if itemid > 0:

            threading.Thread(target=self.loading_audio_from_an_album,
                             args=(10000, 0, self.listPlayLists[itemid - 1]["id"])).start()
        else:
            threading.Thread(target=self.loading_audios, args=(10000, 0)).start()

    def audioPlayer_position_changed(self, position):
        if position > 0:
            Ptime = tools.time_to_human_time(position)
            Duration = tools.time_to_human_time(AudioPlayer.activeDuration)
            self.labelDuration.setText(Ptime + "/" + Duration)
            self.sliderAudio.setValue(position)
            if position == AudioPlayer.activeDuration:
                self.playIndex = self.playIndex + 1
                audio: dict = self.audio.getById(self.listAudios[self.playIndex]["owner_id"],
                                                 self.listAudios[self.playIndex]["id"])
                self.start_play(audio)

    def audioPlayer_duration_changed(self, value):
        self.sliderAudio.setMaximum(value)
        Duration = tools.time_to_human_time(value)
        self.labelDuration.setText("0/" + Duration)
        AudioPlayer.activeDuration = value;

    def loading_audio_from_an_album(self, count, offset, albumID):
        audioList = self.audio.get(count, offset, None, albumID)
        self.listAudios = audioList["response"]["items"]
        for k in audioList["response"]["items"]:
            item = QtWidgets.QListWidgetItem(self.imageHandlerPlay.get_image(),
                                             "<p><b>" + k['artist'] + "</b><br> " + k["title"] + "</br></p>")
            item.setSizeHint(QtCore.QSize(50, 40))
            self.listWidgetAudio.addItem(item)

    def loading_audios(self, count, offset):
        audioList = self.audio.get(count, offset)
        self.listAudios = audioList["response"]["items"]
        for k in audioList["response"]["items"]:
            item = QtWidgets.QListWidgetItem(self.imageHandlerPlay.get_image(),
                                             "<p><b>" + k['artist'] + "</b><br> " + k["title"] + "</br></p>")
            item.setSizeHint(QtCore.QSize(50, 40))
            self.listWidgetAudio.addItem(item)

    def loading_albums(self, count, offset):
        audioList = self.audio.getAlbums(count, offset, None)
        if len(audioList["response"]["items"]) > 0:
            self.listPlayLists = audioList["response"]["items"]

            item = QtWidgets.QListWidgetItem(self.imageHandlerPlaylist.get_image(), "Мои аудио")
            self.listWidgetPlayLists.addItem(item)

            for k in audioList["response"]["items"]:
                item = QtWidgets.QListWidgetItem(self.imageHandlerPlaylist.get_image(), k["title"])
                self.listWidgetPlayLists.addItem(item)
