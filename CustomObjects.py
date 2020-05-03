from PySide2 import QtWidgets, QtCore, QtGui
from enum import Enum
class DataScrollBar(QtWidgets.QScrollBar):
    resized=QtCore.Signal(QtGui.QResizeEvent)
    def __init__(self,parent):
        super().__init__(parent)
    def resizeEvent(self,size):
        self.resized.emit(size) 


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


class AudioSlider(QtWidgets.QSlider):
    clicked = QtCore.Signal(int)

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

    def enterEvent(self, enterEvent):
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
            self.clicked.emit(val)

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

    def leaveEvent(self, leaveEvent):
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


class СlickableLabel(QtWidgets.QLabel):
    clicked = QtCore.Signal(QtGui.QMouseEvent)

    def mousePressEvent(self, ev):
        self.clicked.emit(ev)


class AttachmentType():
    video="video"
    audio="audio"
    photo="photo"

class userType():
    user = "user"
    chat = "chat"
    group = "group"
