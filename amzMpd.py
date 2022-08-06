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
        print("FindAdd Playlist  ERROR")
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
def GetUpdateMpd():
    try:
        client = MPDClient()
        client.timeout = 10
        client.idletimeout = None
        client.connect("localhost", 6600)
        client.clearerror()
        #print("GetUpdate")
        status = client.idle()
        #print(status)
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return status #int(volume)

    except :
        print(" Get Idle ERROR")
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
        listAlbum = GetListMpd2("album")
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
#list('Title', 'Artist', artist)
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
def GetListOutputs():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        outputs = client.outputs()
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return outputs #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"
def SetOutputs2(id):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        outputs = client.outputs()
        listId = []
        for item in outputs:
             if "outputid" in item:
                 listId.append(int(item["outputid"]))
        print(listId)
        for item in listId:
             client.disableoutput(item)
        client.enableoutput(id)
        #print(GetListOutputs())
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return outputs #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"
def SetOutputs(id,en):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        #outputs = client.outputs()
        #listId = []
        #for item in outputs:
        #     if "outputid" in item:
        #         listId.append(int(item["outputid"]))
        #print(listId)
        #for item in listId:
        #     client.disableoutput(item)
        if en ==1:
             client.enableoutput(id)
        else:
             client.disableoutput(id)
        #print(GetListOutputs())
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return "Send Output OK" #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"

def GetListMpd2(cmd):
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
def GetListFiles(url):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        listFiles = client.listfiles(url)
        files = []
        for dictionary in listFiles:
             if "directory" in dictionary:
                  files.append(dictionary["directory"])
             if "file" in dictionary:
                  files.append(dictionary["file"])

        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return files #int(volume)

    except :
        print("Get list file ERROR")
        return "list file ERROR"
def GetListDir(url):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        listFiles = client.listfiles(url)
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        files = []
        for dictionary in listFiles:
             if "directory" in dictionary:
                  files.append(dictionary["directory"])

        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return files #int(volume)

        #return list #int(volume)

    except :
        print("Get list file ERROR")
        return "list file ERROR"
def GetListFiles2(url):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        listFiles = client.listall(url)
        #print(listFiles)
        files = []
        for dictionary in listFiles:
             if "file" in dictionary:
                  if not ".cue/" in dictionary["file"]:
                     # print(dictionary["file"])
                      files.append(dictionary["file"])
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return files #int(volume)

    except :
        print("Get list file ERROR")
        return "list file ERROR"

def GetListMpd(cmd,cmd2,cmd3):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        list = client.list(cmd,cmd2,cmd3)
        #print(client.status()['volume'])
        #s1 = json.dumps(status)
        #volume = json.loads(s1)["volume"]
        #print(volume)
        return list #int(volume)

    except :
        print("Get Status ERROR")
        return "ERROR"
def GetTitlesAlbum(indexAlbums):
    listMpd = GetListMpd2("album")
    #print(listMpd)
    try:
        albums = []
        for dictionary in listMpd:
             if "album" in dictionary:
                  albums.append(dictionary["album"])
        titles = GetListMpd("title","album",albums[indexAlbums])
        #print(titles)
        Titles = []
        for dictionary in titles:
             if "title" in dictionary:
                  Titles.append(dictionary["title"])
        return Titles 
    except:
        print("Can not read album")
def GetFilesAlbum(indexAlbums):
    listMpd = GetListMpd2("album")
    #print(listMpd)
    try:
        albums = []
        for dictionary in listMpd:
             if "album" in dictionary:
                  albums.append(dictionary["album"])
        files = GetListMpd("file","album",albums[indexAlbums])
        #print(files)
        Files = []
        for dictionary in files:
             if "file" in dictionary:
                  Files.append(dictionary["file"])
        return Files
    except:
        print("Can not read album")

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
def PlayAddMpd(title,album):
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.findadd("title",title,"album",album)
        client.play()
    except :
        return False

def UpdateMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.clearerror()
        client.update()
    except :
        return False


def ClearPlaylistMpd():
    try:
        client = MPDClient()
        client.connect("localhost", 6600)
        client.clear()
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


