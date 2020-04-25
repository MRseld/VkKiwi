from PySide2 import QtMultimedia

playing:bool=False;
activeDuration=0

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

def setDuration(value):
    activeDuration=value;

def getDuration():
    return activeDuration;

def getPosition():
    
    return player.position()

def setPosition(position):
    return player.setPosition(position)







    
