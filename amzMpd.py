from mpd import (MPDClient, CommandError, FailureResponseCode)
import json
def CheckPlayMpd(FileName: str) -> bool:
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        status = client.status()
        s1 = json.dumps(status)
        state = json.loads(s1)["state"]
        #print("trang thai mpd {}".format(state))
        if state.find("play") != -1:
            song_info = client.currentsong()
            s1 = json.dumps(song_info)
            filename = json.loads(s1)["file"]
            if filename.find(FileName) != -1:
                #print("Playing with Song info : {}".format(filename))
                return True
            else:
                #print("Mpd not play with {}".format(FileName))
                return False
        
    except :
        return False
def SetVolume(volume):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.setvol(volume)
        print("Volume set is {}".format(volume))
    except :
        print("Set Volume ERROR")
        return False
def FindAddPlaylist(key,name):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.findadd(key,name)
        #print("Volume set is {}".format(volume))
    except :
        print("FindAdd Playlist  Volume ERROR")
        return False

def GetVolume():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        
        status = client.status()
        print(client.status()['volume'])
        s1 = json.dumps(status)
        volume = json.loads(s1)["volume"]
        #print(volume)
        return int(volume)
        
    except :
        print("Get Volume ERROR")
        return 50
def GetStatusMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)

        status = client.status()
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return status #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"
def GetPlaylistMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)

        list = client.playlistinfo()
        titles = []
        for dictionary in list:
             if "title" in dictionary:
                  titles.append(dictionary["title"])
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return titles #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"
def GetListAlbumMpd():
    try:
        listAlbum = GetListMpd("album")
        albums = []
        for dictionary in listAlbum:
             if "album" in dictionary:
                  albums.append(dictionary["album"])
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return albums #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"

def GetSongMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        song_info = client.currentsong()
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return song_info #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"

def GetListMpd(cmd):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        list = client.list(cmd)
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return list #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"


def PlayMpdRadio(Url: str):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.clearerror()
        client.stop()
        client.clear()
        client.add(Url)
        client.play(0)
    except :
        return False
def StopMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.stop()
    except :
        return False
def PauseMpd(state):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.pause(state)
    except :
        return False
def NextMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.next()
    except :
        return False
def UpdateMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.update()
    except :
        return False

def PreviousMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.previous()
    except :
        return False
def PlayMpd(songId):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.play(songId)
    except :
        return False


