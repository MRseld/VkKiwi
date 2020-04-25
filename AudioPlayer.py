from PySide2 import QtMultimedia

playing:bool=False;
activeDuration=0
currectDuration=0
loaded=False
player =  QtMultimedia.QMediaPlayer()
def play():
    global playing
    if playing ==True:
        stop()
        playing=False;
    player.play();
    playing=True

def Isloaded():
    return loaded;
def pause():
    player.pause()

def stop():
    player.stop()

def setAudio(url):
    m=QtMultimedia.QMediaContent(url)
    player.setMedia(m);
    global loaded
    loaded=True

def setVolume(value):
    player.setVolume(value)


def getDuration():
    return activeDuration;

def getPosition():
    
    return player.position()

def setPosition(position):
     player.setPosition(position)







    
