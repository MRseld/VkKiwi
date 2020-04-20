from PySide2 import QtMultimedia

playing:bool=False;


player =  QtMultimedia.QMediaPlayer()
def play():
    global playing
    if playing ==True:
        stop()
        playing=False;
    player.play();
    playing=True

def stop():
    player.stop()

def setAudio(url):
    m=QtMultimedia.QMediaContent(url)
    player.setMedia(m);

def setVolume(value):
    player.setVolume(value)





    
