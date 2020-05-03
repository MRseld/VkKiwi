# -*- coding: utf-8 -*-
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import ApiCalls
import tools
import threading
import time


class DialogListWidgetPanel(QtWidgets.QWidget):
    def __init__(self, parent):
        super(DialogListWidgetPanel, self).__init__(parent)
        self.ID = 0
        self.labelImage = QtWidgets.QLabel()
        self.layoutMain = QtWidgets.QHBoxLayout()
        self.layoutInner = QtWidgets.QVBoxLayout()
        self.unreadCount = 0
        self.unreadCountsLabel = QtWidgets.QLabel()
        self.labelTitle = QtWidgets.QLabel()
        self.labelTitle.setStyleSheet("font-weight: bold; color: black")
        self.labelText = QtWidgets.QLabel()
        # self.labelText.setStyleSheet("font-style:italic; color: #859900")

        self.layoutInner.addWidget(self.labelTitle)
        self.layoutInner.addWidget(self.labelText)

        self.layoutMain.addWidget(self.labelImage)
        self.layoutMain.addLayout(self.layoutInner)
        self.setLayout(self.layoutMain)
        self.layoutMain.addWidget(self.unreadCountsLabel)
        self.layoutInner.addStretch()

    def get_id(self):
        return self.ID

    def getUnreadCount(self):
        return self.unreadCount

    def get_text(self):
        return self.labelText.text()

    def get_title(self):
        return self.labelTitle.text()

    def get_pixmap(self):
        return self.labelImage.pixmap()

    def setUnreadCount(self, count: int):

        self.unreadCount = count
        if self.unreadCount > 0 and self.unreadCount != 1463556740:
            self.setUnreadCountLabelValue("(" + str(self.unreadCount) + ")")
        elif self.unreadCount == 0:
            self.setUnreadCountLabelValue("")

    def setUnreadCountLabelValue(self, count):
        self.unreadCountsLabel.setText(str(count))

    def set_text(self, text):
        self.labelText.setText(text)

    def set_title_text(self, text):
        self.labelTitle.setText(text)

    def set_id(self, value: int):
        self.ID = value

    def set_image(self, image: QtGui.QPixmap, round: bool == False):
        if (round == True):
            iamgeHandler = tools.ImageHandler()

            iamgeHandler.set_image_from_pixmap(image)
            iamgeHandler.resize_image(50, 50)
            iamgeHandler.round_image(True, 50)

            image = iamgeHandler.get_image()

        self.labelImage.setPixmap(image)
        self.labelImage.setFixedSize(QtCore.QSize(50, 50))


class DialogListWidget(QtWidgets.QWidget):
    MApi = ApiCalls.Messages()
    WlistWidgets = list()
    trigger = QtCore.Signal(int, int, str, str, str)

    newoffset = 0
    oldoffset = 0
    count = 0

    def __init__(self, parent):
        self.loadingGifMovieStarted = False
        self.loadingsImage = False
        super(DialogListWidget, self).__init__(parent)
        self.Conversations = None

        # self.standartImage=QtGui.QPixmap("NP.jpg")

        self.trigger.connect(self.slot_data_loaded)

        self.imagehandler = tools.ImageHandler()
        self.standartImage = self.imagehandler.get_image_from_url("https://vk.com/images/icons/im_multichat_50.png")

        self.timerQ = QtCore.QTimer(self)
        self.timerQ.timeout.connect(self.check)
        self.timerQ.start(50)

        self.timerQP = QtCore.QTimer(self)
        self.timerQP.timeout.connect(self.LoadingGif)
        self.timerQP.start(100)

        self.labelLoading = QtWidgets.QLabel()
        self.labelLoading.setAlignment(QtCore.Qt.AlignCenter)
        self.movieGifLoad = QtGui.QMovie("progress_gray.gif")
        self.labelLoading.setMovie(self.movieGifLoad)
        self.labelLoading.setStyleSheet("text-align:  center;")

        t = threading.Thread(target=self.load_dialogs, args=(100, 0))
        t.start()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.labelLoading)
        self.listview = QtWidgets.QListWidget()
        # self.listview.setStyleSheet("background: #282828")

        self.Vscroll = QtWidgets.QScrollBar()
        self.Vscroll.valueChanged.connect(self.Vscrolled)
        self.listview.setVerticalScrollBar(self.Vscroll)

        self.setLayout(self.layout)

        self.layout.addWidget(self.listview)
        lt = threading.Thread(target=self.longPoll_start)

        lt.start()

    def updateElement(self, oldPanel: DialogListWidgetPanel, item):

        w = DialogListWidgetPanel(self)
        print(oldPanel.get_title())
        w.set_id(oldPanel.get_id())
        w.set_text(oldPanel.get_text())
        w.set_title_text(oldPanel.get_title())
        w.set_image(oldPanel.get_pixmap(), False)
        w.setUnreadCount(oldPanel.getUnreadCount())
        self.listview.setItemWidget(item, w)

    def LoadingGif(self):
        if self.loadingGifMovieStarted == False:
            if self.loading == True:
                self.labelLoading.show()
                self.movieGifLoad.start()
                self.loadingGifMovieStarted = True
        else:
            if self.loading == False:
                self.movieGifLoad.stop()
                self.labelLoading.hide()
                self.loadingGifMovieStarted = False

    def get_flags(self, Flags):
        t = Flags
        correctFlags = []

        FLAGS = {'UNKNOWN9': 4194304, 'UNKNOWN8': 2097152, 'UNKNOWN7': 1048576, 'UNKNOWN6': 524288,
                 'NOT_DELIVERED': 262144, 'DELETE_FOR_ALL': 131072, 'HIDDEN': 65536, 'UNKNOWN5': 32768,
                 'UNKNOWN4': 16384,
                 'UNREAD_MULTICHAT': 8192, 'UNKNOWN3': 4096, 'UNKNOWN2': 2048, 'UNKNOWN1': 1024, 'MEDIA': 512,
                 'FIXED': 256, 'DELETED': 128,
                 'SPAM': 64, 'FRIENDS': 32, 'CHAT': 16, 'IMPORTANT': 8, 'REPLIED': 4, 'OUTBOX': 2, 'UNREAD': 1}
        for flag in FLAGS:
            if t - int(FLAGS[flag]) > 0:
                t = t - int(FLAGS[flag])
                correctFlags.append(flag)
        return correctFlags

    def slot_new_message(self, index, object):
        for i in range(0, self.listview.count()):
            w: DialogListWidgetPanel = self.listview.itemWidget(
                self.listview.item(i))
            if w is not None:
                if object["updates"][index][3] == w.get_id():
                    if object["updates"][index][5] is not None:
                        w.set_text(object["updates"][index][5])

                    if "attach1_type" in object["updates"][index][7]:
                        w.set_text(object["updates"][index][7]["attach1_type"])

                    if "OUTBOX" in self.get_flags(object["updates"][index][2]):
                        w.setUnreadCount(0)

                    else:
                        w.setUnreadCount(w.getUnreadCount() + 1)
                    item: QtWidgets.QListWidgetItem = self.listview.item(i)
                    self.listview.takeItem(i)
                    self.listview.insertItem(0, item)
                    self.updateElement(w, item)
                    break

    def longPoll_start(self):
        LPApi = tools.longPollQT()
        LPApi.getLongPollServer()
        LPApi.setMode(10)
        LPApi.signalNewMessage.connect(self.slot_new_message)
        LPApi.signalDialogIsread.connect(self.slot_dialog_is_read)
        while True:
            while self.loading:
                time.sleep(0.2)
            LPApi.update()

    def slot_dialog_is_read(self, index, object: dict):
        if not self.loading:

            for i in range(0, self.listview.count()):
                w: DialogListWidgetPanel = self.listview.itemWidget(
                    self.listview.item(i))

                if object["updates"][index][1] == w.get_id():
                    w.setUnreadCount(0)
                    w.update()
                    break

    def Vscrolled(self, i):
        if self.Vscroll.maximum() == i:
            if self.newoffset != self.count:
                if not self.loading:
                    t = threading.Thread(target=self.load_dialogs, args=(100, self.newoffset))
                    t.start()

    def thread_load_images(self, panel: DialogListWidgetPanel, url):
        imgh=tools.ImageHandler()
        panel.set_image(imgh.get_image_from_url(url), True)
        print("url= "+url)
    def slot_data_loaded(self, id, unreadcount, title, text, imageUrl):
        item = QtWidgets.QListWidgetItem()

        w = DialogListWidgetPanel(self)
        self.WlistWidgets.append(w)
        w.set_id(id)
        w.set_text(text)
        w.set_title_text(title)
        print("загрузка диалога: "+title)

        w.set_image(self.standartImage, True)

        w.setUnreadCount(unreadcount)
        item.setSizeHint(QtCore.QSize(w.width(), 60))
        self.listview.addItem(item)
        self.listview.setItemWidget(item, w)
        if len(imageUrl) > 0:
            t = threading.Thread(target=self.thread_load_images, args=(w, imageUrl)).start()

    def check(self):
        k: bool = False
        if self.loadingsImage == True:
            for i in range(0, len(self.Conversations["response"]["items"])):
                w: DialogListWidgetPanel = self.listview.itemWidget(
                    self.listview.item(self.oldoffset + i))
                if w is None:
                    k = True
                    break

            if not k:
                threading.Thread(target=self.load_images()).start()
                self.loadingsImage = False

    def load_images(self):
        print("start loading iMAGE")
        for i in range(0, len(self.Conversations["response"]["items"])):
            try:
                if str(self.Conversations["response"]["items"][i]["conversation"]["peer"]["type"]) == "chat":

                    tz = threading.Thread(target=self.load_chat_image,
                                          args=(i,))
                    tz.start()

                elif str(self.Conversations["response"]["items"][i]["conversation"]["peer"]["type"]) == "user":
                    tz = threading.Thread(target=self.load_user_image, args=(i,))
                    tz.start()

                else:
                    tz = threading.Thread(target=self.load_group_image, args=(i,))
                    tz.start()

            except Exception as ex:
                print(str(ex))

        self.oldoffset = self.oldoffset + len(self.Conversations["response"]["items"])
        self.loading = False

    def load_dialogs(self, count, offset):
        self.loading = True

        self.Conversations = self.MApi.get(count, offset, 1)
        self.count = self.Conversations["response"]["count"]

        for i in range(0, len(self.Conversations["response"]["items"])):
            time.sleep(0.03)

            if str(self.Conversations["response"]["items"][i]["conversation"]["peer"]["type"]) == "chat":

                self.load_chat_dialog(i)
            elif str(self.Conversations["response"]["items"][i]["conversation"]["peer"]["type"]) == "user":

                self.load_user_dialog(i)
            else:

                self.load_group_dialog(i)

        self.newoffset = self.newoffset + len(self.Conversations["response"]["items"])
        self.loading=False

    def load_group_image(self, index):

        conversation = self.Conversations["response"]["items"][index]["conversation"]
        for i in range(0, len(self.Conversations["response"]["groups"])):
            group = self.Conversations["response"]["groups"][i]
            if (int(conversation["peer"]["id"]) * -1 == group["id"]):
                if "photo_50" in group:
                    w: DialogListWidgetPanel = self.listview.itemWidget(
                        self.listview.item(self.oldoffset + index))

                    w.set_image(self.imagehandler.get_image_from_url(group["photo_50"]), True)

                    break

    def load_user_image(self, index):

        conversation = self.Conversations["response"]["items"][index]["conversation"]
        for i in range(0, len(self.Conversations["response"]["profiles"])):
            profile = self.Conversations["response"]["profiles"][i]
            if (conversation["peer"]["id"] == profile["id"]):
                w: DialogListWidgetPanel = self.listview.itemWidget(
                    self.listview.item(self.oldoffset + index))

                w.set_image(self.imagehandler.get_image_from_url(profile["photo_50"]), True)

                break

    def load_chat_image(self, index):

        conversation = self.Conversations["response"]["items"][index]["conversation"]
        if ("photo" in conversation["chat_settings"]):
            w: DialogListWidgetPanel = self.listview.itemWidget(
                self.listview.item(self.oldoffset + index))

            w.set_image(self.imagehandler.get_image_from_url(conversation["chat_settings"]["photo"]["photo_50"]), True)

    def load_group_dialog(self, index: int):
        if (len(self.Conversations["response"]["items"][index]["last_message"]["fwd_messages"]) > 0):
            textMessage = "[Пересланные сообщения]"
        elif (len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) > 0):
            if (len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) == 1):
                textMessage = "Вложение"
            else:
                textMessage = "[Вложения]"
        else:
            textMessage = self.Conversations["response"]["items"][index]["last_message"]["text"]
        conversation = self.Conversations["response"]["items"][index]["conversation"]

        for i in range(0, len(self.Conversations["response"]["groups"])):
            group = self.Conversations["response"]["groups"][i]
            if (conversation["peer"]["id"] * -1 == group["id"]):

                title = group["name"] + "[Группа]"

                if "unread_count" in conversation:
                    self.trigger.emit(group["id"], conversation["unread_count"], title, textMessage, group["photo_50"])
                else:
                    self.trigger.emit(group["id"], 0, title, textMessage, group["photo_50"])

                break

    def load_user_dialog(self, index: int):
        if (len(self.Conversations["response"]["items"][index]["last_message"]["fwd_messages"]) > 0):
            textMessage = "[Пересланные сообщения]"

        elif (len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) > 0):
            if (len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) == 1):
                textMessage = "[Вложение]"
            else:
                textMessage = "[Вложения]"

        else:
            textMessage = self.Conversations["response"]["items"][index]["last_message"]["text"]
        conversation = self.Conversations["response"]["items"][index]["conversation"]

        for i in range(0, len(self.Conversations["response"]["profiles"])):
            profile = self.Conversations["response"]["profiles"][i]
            if (conversation["peer"]["id"] == profile["id"]):

                title = profile["first_name"] + " " + \
                        profile["last_name"] + "[Пользователь]"

                if ("unread_count" in conversation):
                    self.trigger.emit(profile["id"], conversation["unread_count"], title, textMessage,
                                      profile["photo_50"])

                else:
                    self.trigger.emit(profile["id"], 0, title, textMessage, profile["photo_50"])

                break

    def load_chat_dialog(self, index: int):

        conversation = self.Conversations["response"]["items"][index]

        if (len(self.Conversations["response"]["items"][index]["last_message"]["fwd_messages"]) > 0):
            textMessage = "[Пересланные сообщения]"
        elif (len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) > 0):
            if (len(self.Conversations["response"]["items"][index]["last_message"]["attachments"]) == 1):
                textMessage = "Вложение"
            else:
                textMessage = "[Вложения]"

        else:
            textMessage = self.Conversations["response"]["items"][index]["last_message"]["text"]

        text = conversation["last_message"]["text"]
        title = conversation["conversation"]["chat_settings"]["title"] + "[Беседа]"
        if ("photo" in conversation["conversation"]["chat_settings"]):
            Ucount = 0
            if "unread_count" in conversation["conversation"]:
                Ucount = int(conversation["conversation"]["unread_count"])

            self.trigger.emit(conversation["conversation"]["peer"]["id"],
                              Ucount, title, textMessage,
                              conversation["conversation"]["chat_settings"]["photo"]["photo_50"])

        else:
            Ucount = 0
            if "unread_count" in conversation["conversation"]:
                Ucount = int(conversation["conversation"]["unread_count"])

            self.trigger.emit(conversation["conversation"]["peer"]["id"],
                              Ucount, title, textMessage,
                              None)
