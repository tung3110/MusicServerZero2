
#!/usr/bin/python
#from sense_hat
#import SenseHat
import socket
import re
from threading import Timer,Thread,Event
from datetime import datetime
from time import strftime
import urllib
import requests
import time
time.sleep(0)
import os
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import subprocess
import serial
from amzGetDeviceID import getDeviceID
from amzCheckStream import CheckStream
#from amzGetHostBroker import checkOutput
#from amzStream import StreamStart
from amzMQTT import ConectMQTT
#from amzGetMpdSong import get_song_info
from amzMpd import (UpdateMpd,GetListAlbumMpd,GetPlaylistMpd,FindAddPlaylist,GetListMpd,PauseMpd,NextMpd,PreviousMpd,GetSongMpd,CheckPlayMpd,PlayMpd,StopMpd,SetVolume,GetVolume,GetStatusMpd)
from amzGetHostName import getHostIP
from amzCheckDAC import CheckDac
#from amzConnectWifi import ConnectWifi
#connectWifi = ConnectWifi("Tan Phong","66668888")
#connectWifi.ConnectWifi("Tungnh","1234512345")
#interface = 'wlan0'
#name = "Tan Phong"
#password = "66668888"
#os.system('iwconfig ' + interface + ' essid ' + name + ' key ' + password)
checkDac = CheckDac()
checkDacOld = checkDac
if(checkDac):
   os.system("sudo systemctl restart shairport-sync.service")
   os.system("sudo systemctl restart raspotify.service")    
   print("Restart AirPlay")
MQTT_BROKER_URL=  "smart.radiotech.vn"
MQTT_USER =  "village-speaker"
MQTT_PASS =  "vs.bytech@2019"
MQTT_PORT = 1883
HostRadioTech = "http://smart.radiotech.vn:3000/"
#time.sleep(0)
MQTT_Flag = 0
MQTT_Timeout = 20
MQTT_Timeout_Online = 30
#hostname = socket.gethostname()
#local_ip = socket.gethostbyname(hostname)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
except:
    local_ip = "172.24.1.1"
#Broker = "192.168.1.237"
Broker_Local = local_ip
#Broker_Local = getHostIP()
if Broker_Local.find("Not Found") != -1:
    Broker_Local = "localhost"
HostLocalStream = "http://{}:8000/".format(Broker_Local)

print("HostLocalStream : {}".format(HostLocalStream))

#Broker_Local = "192.168.1.230"

#if(CheckStream(HostLocalStream,"mpd")):
#    print("Local Streaming")
#check = CheckStream(HostRadioTech,"860262050120653")
pub_topic = "vs/sub/amzMaster"
MountPoint = getDeviceID()
print("Device ID: {}".format(MountPoint))
#get_song_info("mpd")
MASTER1 = "795844609835509"
MASTER2 = "601563437304150"
MASTER3 = "000001111199999"
sub_topic = "vs/sub/{}".format(MountPoint)
LocalMaster = "amzMaster"
#PlayMpd("{}{}".format(HostRadioTech,MASTER2))
#state = CheckPlayMpd(MASTER1)
#StreamStart("localhost","amz","amz",8000,"/{}".format(MountPoint),"/media/pi/MUSIC/MP3")
STREAM_STATE = False
STREAM_RUNNING_TIMEOUT = 0
STATE_ONLINE = 1
VOLUME = GetVolume()
print("Volume is {}".format(str(VOLUME)))
PageModeLcd = 0
#output = checkOutput("avahi-browse -r _mqtt._tcp")
def CheckFirstRun():
    with open('hostname.txt') as f:
       if 'amz123' in f.read():
         print("First Run Set Hostname")
         try:
            hostname = "Amz"+MountPoint[-4:]
            print("Hostname is: ",hostname)
            output_file = open('/etc/hostname','w')
            output_file.write(hostname)
            output_file.close()
            output_file = open('hostname.txt','w')
            output_file.write(hostname)
            output_file.close()
            time.sleep(20)
            os.system("sudo reboot")
            print("Set Hostname : {} OK".format(hostname))
        #lines = [line.rstrip() for line in lines]
         except:
            print("Can not set Hostname")
       
#print(output)
CheckFirstRun()
def ReadConfig():
  global MASTER1,MASTER2,MASTER3 
  try:
     with open("amzConfig.txt") as file:
        lines = file.readlines()
        #file.close()
     #print(lines)
     newlines = lines[0].split(',')
     m1  = newlines[1].split('(')
     MASTER1 = m1[1]
     MASTER1 = MASTER1[:-1]
     m2 = newlines[2].split('(')
     MASTER2 = m2[1]
     MASTER2 = MASTER2[:-1]
     m3 = newlines[3].split('(')
     MASTER3 = m3[1]
     MASTER3 = MASTER3[:-1]
     print("Read Config : Master 1,2,3 : {},{},{}".format(MASTER1,MASTER2,MASTER3))
        #lines = [line.rstrip() for line in lines]
  except:
    print("Read Config file not fount")
def ReadConfigState():
    global STATE_ONLINE 
    try:
     with open("amzConfigState.txt") as file:
        lines = file.readlines()
        #file.close()
     #print(lines)
     newlines = lines[0].split(',')
     m1  = newlines[1].split('(')
     m2 = m1[1]
     m2 = m2[:-2]
     STATE_ONLINE = int(m2)
     print("Read Config State: MODE : {}".format(m2))
        #lines = [line.rstrip() for line in lines]
    except:
        print("Read Config State file not fount")
def ReadConfigVolume():
  global VOLUME
  try:
     with open("amzConfigVolume.txt") as file:
        lines = file.readlines()
        #file.close()
     #print(lines)
     newlines = lines[0].split(',')
     m1  = newlines[1].split('(')
     m2 = m1[1]
     m2 = m2[:-2]
     VOLUME = int(m2)
     SetVolume(VOLUME)
     print("Read Volume: {}".format(m2))
        #lines = [line.rstrip() for line in lines]
  except:
    print("Read Config Volume file not fount")
ReadConfig()
ReadConfigState()
#ReadConfigVolume()
MASTER_STREAM = MASTER1
#print(MASTER1)
#print(MASTER2)
#print(MASTER3)
MQTT_Flag_Local = 0
def playAudioLocal(links):
    media = vlc.MediaPlayer(links)
    media.play()
def playAudio(links):
       global STREAM_STATE
       if STATE_ONLINE != 4:
           STREAM_STATE = True
           PlayMpd(links)
           print("Playing with links {}".format(links))
def on_connect_local(client2, userdata, flags, rc):
   global MountPoint,MQTT_Flag_Local
   print("Connected Host Local  with result code " + str(rc))
   MQTT_Flag = 1
   MQTT_Flag_Local = 1
   Sub_RadioTech = "vs/sub/"+MountPoint
   client2.subscribe(Sub_RadioTech)
   client2.subscribe("vs/pub/{}".format("amzMaster"))
   client2.subscribe("vs/pub/{}".format(MASTER1))
   client2.subscribe("vs/pub/{}".format(MASTER2))
   client2.subscribe("vs/pub/{}".format(MASTER3))
   #print(Sub_RadioTech)
# when receiving a mqtt message do this;
def on_connect_online(client, userdata, flags, rc):
   global MountPoint
   print("Connected Radio Tech  with result code " + str(rc))
   MQTT_Flag = 1
   MQTT_Timeout_Online = 30
   Sub_RadioTech = "vs/sub/"+MountPoint
   client.subscribe(Sub_RadioTech)
   client.subscribe("vs/pub/{}".format(MASTER1))
   client.subscribe("vs/pub/{}".format(MASTER2))
   client.subscribe("vs/pub/{}".format(MASTER3))
   #client.subscribe("vs/pub/{}".format("860262050123210"))
   print(Sub_RadioTech)
# when receiving a mqtt message do this;
def on_message_local(client2, userdata, msg):
   global PlayVlc,MQTT_Timeout,MQTT_Flag,MountPoint,LocalMaster
   MQTT_Timeout = 40
   MQTT_Flag = 1
   message = str(msg.payload)
   print("MQTT Local " + msg.topic + " " + message)
   #links ="mpc add http://{0}:8000/{1}.ogg".format(MASTER1,MASTER3)
   #/usr/share/alsa/alsa.conf
   if message.find("SET,HOSTNAME")!=-1:
      try:
         newlines = message.split(',')
         hostname = newlines[2]
         ssid = newlines[3]
         password = newlines[4]
         #cmd = "nmcli d wifi connect "%s"  password %s  ifname wlan0" % (ssid,password)
         cmd = "sudo nmcli device wifi connect '{}' password '{}' ifname wlan0".format(ssid,password)
         #connectWifi = ConnectWifi(ssid,password)
         os.system('nmcli d wifi connect "%s"  password %s  ifname wlan0' % (ssid,password))
         print(cmd)
         publish_mqtt_local("vs/sub/amzMaster",message)
         time.sleep(1)
         publish_mqtt_local("vs/sub/amzMaster",message)
         time.sleep(1)
         output_file = open('/etc/hostname','w')
         output_file.write(hostname)
         output_file.close()
         output_file = open('hostname.txt','w')
         output_file.write(hostname)
         output_file.close()
         output_file = open('amzAudioConfig.txt','w')
         output_file.write(message)
         output_file.close()
         print("Set Hostname : {} OK".format(hostname))
         publish_mqtt_local("vs/sub/amzMaster","RESET")
         time.sleep(1)
         os.system("sudo reboot")
         #print("Set Hostname : {} OK".format(hostname))
        #lines = [line.rstrip() for line in lines]
      except:
        print("Can not set Hostname")
   if message.find("GET,HOSTNAME")!=-1:
       try:
          with open("amzAudioConfig.txt") as file:
             lines = file.readlines()
             #file.close()
             #print(lines)
          newlines = lines[0]
          publish_mqtt_local("vs/sub/amzMaster",newlines)
       except:
          print("Can not amzAudioConfig")

   if message.find("SET,MASTER1")!=-1:
       try:
           output_file = open('amzConfig.txt','w')
           output_file.write(message)
           output_file.close()
       except:
           print("File not open")
       ReadConfig()
   if msg.topic.find("/pub/amzMaster") != -1:#RUNNING()
        if message.find("RUNNING(") != -1:
            links = message.split('(')[1]
            links = links[:-2]
            print("links : {}".format(links))
            LocalMaster = links.split('/')[3]
            STREAM_RUNNING_TIMEOUT = 15
            STREAM_STATE_STR = "RUNNING"
            MASTER_STREAM = "LocalMaster:{}".format(LocalMaster)
            links ="{0}{1}".format(HostLocalStream,LocalMaster)
            if not CheckPlayMpd("8000/{}".format(LocalMaster)):
                print("Check stream")
                playAudio(links)
def on_message_online(client, userdata, msg):
   global HostRadioTech,MASTER2,MQTT_Timeout_Online,MQTT_Flag
   MQTT_Timeout_Online = 40
   MQTT_Flag = 1
   message = str(msg.payload)
   print("MQTT Online " + msg.topic + " " + message)
   if message.find("SET,MASTER1")!=-1:
       try:
           output_file = open('amzConfig.txt','w')
           output_file.write(message)
           output_file.close()
       except:
           print("File amzConfig.txt not open ")
       ReadConfig()
   if message.find("GET,IP")!=-1:
       try:
           conectMQTT.publish_mqtt("IP({})".format(local_ip))
       except:
           print("File amzConfig.txt not open ")

   if message.find("SET,MODE")!=-1:
       try:
           print("Receiver Mode: {}".format(message))
           output_file = open('amzConfigState.txt','w')
           output_file.write(message)
           output_file.close()
       except:
           print("File amzConfigState not open ")
       ReadConfigState()
       if STATE_ONLINE == 4:
           StopMpd()
           print("STOP MPD")
   if message.find("SET,VOLUME")!=-1:
       try:
           print("Receiver Volume: {}".format(message))
           output_file = open('amzConfigVolume.txt','w')
           output_file.write(message)
           output_file.close()
       except:
           print("File amzConfigVolume not open ")
       ReadConfigVolume()
       
   if msg.topic.find(MASTER1) != -1:
       if message.find("RUNNING") != -1:
           if not CheckPlayMpd("8000/{}".format(LocalMaster)):
               if not CheckPlayMpd("8000/mpd"):
                   if not CheckPlayMpd(MASTER1):
                       links ="{0}{1}".format(HostRadioTech,MASTER1)
                       playAudio(links)
       elif message.find("STOP") != -1:
           StopMpd()
   if msg.topic.find(MASTER2) != -1:
        #print("Nhan lenh Running tu {}".format(MASTER2))
        if message.find("RUNNING") != -1:
            if not CheckPlayMpd("8000/{}".format(LocalMaster)):
                if not CheckPlayMpd("8000/mpd"):
                   if not CheckPlayMpd(MASTER1):
                       if not CheckPlayMpd(MASTER2):
                           links ="{0}{1}".format(HostRadioTech,MASTER2)
                           playAudio(links)
        elif message.find("STOP") != -1:
           StopMpd()
   if msg.topic.find(MASTER3) != -1:
       print("Nhan lenh Running tu {}".format(MASTER3))
       if message.find("RUNNING") != -1:
           if not CheckPlayMpd("8000/{}".format(LocalMaster)):
               if not CheckPlayMpd("8000/mpd"):
                   if not CheckPlayMpd(MASTER1):
                       if not CheckPlayMpd(MASTER2):
                           if not CheckPlayMpd(MASTER3):
                               links ="{0}{1}".format(HostRadioTech,MASTER2)
                               playAudio(links)
       elif message.find("STOP") != -1:
           StopMpd() 
def publish_mqtt_local2(sensor_data):
   global MountPoint
   try:
       mqttc = mqtt.Client("python_pub")
       mqttc.connect(Broker_Local, 1883)
       mqttc.publish("vs/pub/"+MountPoint, sensor_data)
   except:
       print("Can not connect local")
   #mqttc.loop(2) //timeout = 2s
def publish_mqtt_local(topic,sensor_data):
   global MountPoint
   try:
       mqttc = mqtt.Client("python_pub")
       mqttc.connect(Broker_Local, 1883)
       mqttc.publish(topic, sensor_data)
       print("publish topic: {}, msg: {}".format(topic,sensor_data))
   except:
       print("Can not connect local")
   #mqttc.loop(2) //timeout = 2s
def on_publish_local(mosq, obj, mid):
   print("mid: " + str(mid))
def ConectMQTT_Local():
        
        try:
                print("Ket noi local {}".format(Broker_Local))
                global MQTT_Timeout
                MQTT_Timeout = 30
                client2 = mqtt.Client()
                client2.on_connect = on_connect_local
                client2.on_message = on_message_local
                client2.connect(Broker_Local, 1883, 60)
                client2.loop_start()
        except:
                MQTT_Flag = 0
                print("Khong the ket noi local")
t=0
class ConectMQTT_RadioTech:
    #global MQTT_Timeout,MQTT_Flag
     def __init__(self, broker,user,pwd):
        self.broker = broker
        self.user = user
        self.pwd = pwd
     def publish_mqtt(self,sensor_data):
        global MountPoint
        print(sensor_data)
        try:
            mqttc = mqtt.Client("python_pub")
            mqttc.username_pw_set(username=self.user, password=self.pwd)
            mqttc.connect(self.broker, 1883)
            Pub_RadioTech = "vs/pub/"+MountPoint
            mqttc.publish(Pub_RadioTech, sensor_data)
        except:
            print("Can not connect MQTT online")
        #mqttc.loop(2) //timeout = 2s

     def on_publish(mosq, obj, mid):
        print("mid: " + str(mid))
     def ConectMQTT(self):
        
        try:
                global MQTT_Timeout
                
               
                client = mqtt.Client()
#client = mqtt.Client(client_id= "" ,clean_session=True, userdata=None, protoco$
                client.on_connect = on_connect_online
                client.on_message = on_message_online
                #client.tls_set()  # <--- even without arguments
                client.username_pw_set(username=self.user, password=self.pwd)            
                client.connect(self.broker, MQTT_PORT)
                client.loop_start()
        except:
                MQTT_Flag = 0
                print("Can not connect MQTT Online") 
#
ConectMQTT_Local()
conectMQTT  = ConectMQTT_RadioTech(MQTT_BROKER_URL,MQTT_USER,MQTT_PASS)
conectMQTT.ConectMQTT()

def SendSerial(serial,Msg):
     res = bytes(Msg, 'utf-8')
     res2 = bytes([255,255,255])
     res1 = res + res2
     serial.write(res1)
     #serial.write(255)
     #serial.write(255)
     #serial.write(255)
ser = serial.Serial(
          port = '/dev/{}'.format("ttyS5"),
          baudrate = 9600,
          parity = serial.PARITY_NONE,
          stopbits = serial.STOPBITS_ONE,
          bytesize = serial.EIGHTBITS,
          timeout = 1)
#SendSerial(ser,"AMZ START")
#SendSerial(ser,"t6.txt={}".format(MountPoint))
#SendSerial(ser,"t6.txt=\"%s\"" % (MountPoint))
#SendSerial(ser,"t1.txt=\"%s\"" % (local_ip))
SendSerial(ser,"t0.txt=\"%s\"" % ("AMZ START"))
time.sleep(1)
#SendSerial(ser,"t0.txt=\"%s\"" % ("AMZ AUDIO HIFI"))
#SendSerial(ser,"t6.txt=\"Imei:{}\"".format(MountPoint))
#SendSerial(ser,"t1.txt=\"%s\"" % (local_ip))
#listMpd = GetListMpd("album")
#print(listMpd)
def SendAlbumLcd():
    listMpd = GetListMpd("album")
    #print(listMpd)
    try:
        s1 = json.dumps(listMpd[1])
        album = json.loads(s1)["album"]
        FindAddPlaylist("album",album)
        SendSerial(ser,"t0.txt=\"%s\"" % (album))
        print("album is %s" % (album))
    except:
        print("Can not read album")
def SendTimeLcd():
     global ser
     timeNow = strftime("%H:%M:%S")
     SendSerial(ser,"t37.txt=\"%s\"" % (timeNow))
     #print("t7.txt=\"%s\"%c%c%c" % (timeNow,255,255,255))
#SendAlbumLcd();
UpdateMpd()
playlist = GetPlaylistMpd()
print(playlist)
albums = GetListAlbumMpd()
print(albums)
StatePlayOld = "stop"
SongId = 0
PlayListLength = 0
def insert_newlines(string, every):
    return '\\r'.join(string[i:i+every] for i in range(0, len(string), every))
SongName = ""
def SendStatusMpdLcd():
    global SongName,StatePlayOld,SongId,PlayListLength,PageModeLcd
    status = GetStatusMpd()
    #print(status)
    try:
        s1 = json.dumps(status)
        state = json.loads(s1)["state"]
        PlayListLength = json.loads(s1)["playlistlength"]
        StatePlayOld = state
        Volume = json.loads(s1)["volume"]
        #Volume = GetVolume()
        #print(status)
        if(PageModeLcd==3):
           playlist = GetPlaylistMpd()
           if len(playlist) == 0:
               clk = 2
               while clk <16:
                    SendSerial(ser,"t%d.txt=\"%s\"" % (clk,""))
                    clk = clk + 1
           else:
               x = 14
               playlists = [playlist[i:i+x] for i in range(0, len(playlist), x)]
               indexPlaylist = int(SongId/14)
               Playlist = playlists[indexPlaylist]
               print(playlists)
               print("Index %d, %s" % (indexPlaylist,Playlist))
               id = 1
               addEmpty = len(Playlist)
               while(addEmpty< 14):
                    Playlist.append("")
                    addEmpty = addEmpty+1
               for item in Playlist:
                   SendSerial(ser,"t%d.txt=\"%s\"" % (id+1,item))
                   SendSerial(ser,"t%d.pco=65535" % (id+1))
                   songId = SongId % 14
                   if (id == (songId+1)):
                        SendSerial(ser,"t%d.pco=65504" % (id+1))
                   id = id + 1
        if state.find("play") != -1:
           SongId = int(json.loads(s1)["song"])
           audioBit = json.loads(s1)["audio"]
           SendSerial(ser,"t32.txt=\"%s\"" % (audioBit))
           timeNow = json.loads(s1)["time"]
           timeNow1 = timeNow.split(":")
           #timeNowStart = timeNow1[0]
           #timeNowStop = timeNow1[1]
           timeProgressBar = (int(timeNow1[0])/int(timeNow1[1]))*100
           SendSerial(ser,"j0.val=%d" % (timeProgressBar))
           timeNowStart = datetime.fromtimestamp(int(timeNow1[0])).strftime('%M:%S')
           timeNowStop = datetime.fromtimestamp(int(timeNow1[1])).strftime('%M:%S')
           #timeNow2 = "t5.txt=\"%s/%s\"" % (timeNowStart,timeNowStop)
           SendSerial(ser, "t35.txt=\"%s/%s\"" % (timeNowStart,timeNowStop))

           song_info = GetSongMpd()
           #print(song_info)
           s1 = json.dumps(song_info)
           songName  = json.loads(s1)["title"]
           if len(songName)>30:
               SongName = insert_newlines(songName,30)
           else:
                SongName = songName
           SendSerial(ser,"t36.txt=\"%s\"" % (SongName))
           album  = json.loads(s1)["album"]
#           if len(album)>30:
#                Album = insert_newlines(album,30)
#           else:
           Album = album
           #Album = re.sub("(.{30})", "\\1\n", album, 0, re.DOTALL)
           SendSerial(ser,"g0.txt=\"Album: %s\"" % (Album))
           Artist = json.loads(s1)["artist"]
           SendSerial(ser,"t30.txt=\"Ar: %s\"" % (Artist))
           SendSerial(ser,"p1.pic=1")
           SendSerial(ser,"j1.val=%s" % (Volume))
           SendSerial(ser,"t34.txt=\"%s\"" % (Volume))
           #StatePlayOld = True 
        elif state.find("stop") != -1:
           SendSerial(ser,"j1.val=%s" % (Volume))
           SendSerial(ser,"t34.txt=\"%s\"" % (Volume))
           SendSerial(ser,"j0.val=%d" % (0))
           SendSerial(ser, "t35.txt=\"00:00/00:00\"")
           SendSerial(ser,"p1.pic=0")
           #StatePLayOld = False
        elif state.find("pause") != -1:
           SendSerial(ser,"j1.val=%s" % (Volume))
           SendSerial(ser,"t34.txt=\"%s\"" % (Volume))
           SendSerial(ser,"p1.pic=0")
    except:
        print("Can not Send Status Mpd")
def SendSongMpdLcd():
    global StatePlayOld
    song_info = GetSongMpd()
    print(song_info)
    try:
        SongName  = json.loads(s1)["file"]
        SendSerial(ser,"t36.txt=\"%s\"" % (SongName))
        
    except:
        print("Can not Send Mpd")
class MyThread(Thread):
    global MQTT_Flag_Local,PageModeLcd,MQTT_Timeout,MQTT_Flag,ConectMQTT2,STREAM_RUNNING_TIMEOUT,ser
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        global PageModeLcd,ser,checkDacOld,checkDac, MQTT_Timeout,MQTT_Flag,STREAM_RUNNING_TIMEOUT,MQTT_Timeout_Online
        while not self.stopped.wait(1): #timeout 1s
            if ((PageModeLcd ==1) or (PageModeLcd ==3) or (PageModeLcd ==4)):
                SendStatusMpdLcd()
                #SendSongMpdLcd()
                #SendSerial(ser,"t1.txt={}".format(local_ip))
                #SendSerial(ser,"t1.txt=\"%s\"" % (local_ip))
                SendTimeLcd()
            elif PageModeLcd ==2:
                SendSerial(ser,"t6.txt=\"IP:{}\"".format (local_ip))
                SendSerial(ser,"t5.txt=\"Imei:{}\"".format(MountPoint))
            elif PageModeLcd ==0:
                SendSerial(ser,"t0.txt=\"%s\"" % ("AMZ START"))
            checkDac = CheckDac()
            if not checkDacOld:
                 if checkDac:
                     os.system("sudo systemctl restart shairport-sync.service")
                     os.system("sudo systemctl restart raspotify.service")                     
                     print("Restart AirPlay")
            checkDacOld = checkDac
            if STREAM_RUNNING_TIMEOUT > 0:
                STREAM_RUNNING_TIMEOUT = STREAM_RUNNING_TIMEOUT -1
                if STREAM_RUNNING_TIMEOUT ==0:
                    StopMpd()
            if(MQTT_Flag_Local==0):
                ConectMQTT_Local()
            if(MQTT_Timeout>0):
                MQTT_Timeout = MQTT_Timeout -1 
                if(MQTT_Timeout==0):
                        MQTT_Flag = 1
                        print("MQTT Local  Not Receiver","ERROR")
                        #ConectMQTT_Local()
            if(MQTT_Timeout_Online>0):
                MQTT_Timeout_Online = MQTT_Timeout_Online -1 
                if(MQTT_Timeout_Online==0):
                        MQTT_Flag = 1
                        print("MQTT Online  Not Receiver","ERROR")
                        conectMQTT.ConectMQTT()
                

stopFlag = Event()
thread = MyThread(stopFlag)
thread.start()

#conectMQTT = ConectMQTT(MQTT_BROKER_URL,MQTT_USER,MQTT_PASS,MQTT_PORT,on_connect_online,on_message_online)
#conectMQTT.ConectMQTT()
STREAM_STATE_STR = "IDE"
def RadioProcessStick():
   
   sensor_data = t # [read_temp(), read_humidity(), read_pressure()]
  # publish.single("vs/sub/amzMaster1", str(sensor_data), hostname = Broker)
   #publish_mqtt(sensor_data)
   #INF,860262050123210,SL1.8,RUNNING,4G,4085,16951296,601563437304150,0,63,MIC,ON,ON,9,0,0,0.0000,0.0000,CSQ:18,VIETTEL,"FDD LTE","LTE BAND 1",300'
   if STATE_ONLINE==4:
       STREAM_STATE_STR = "STOP"
   msg = "INF,"+MountPoint+",SL0.1,"+STREAM_STATE_STR +",WIFI,0,0,"+local_ip+",0,"+str(VOLUME)+",MIC,ON,ON,9,0,0,0.0000,0.0000,,,,,300"
   #conectMQTT.publish_mqtt("vs/pub/{}".format(MountPoint),msg)
   conectMQTT.publish_mqtt(msg)
   publish_mqtt_local("vs/sub/amzMaster",msg)
   publish_mqtt_local("vs/pub/{}".format(MountPoint),msg)
   time.sleep(10)
   t=t+1
   if(CheckStream(HostLocalStream,LocalMaster)):
        STREAM_RUNNING_TIMEOUT = 15
        STREAM_STATE_STR = "RUNNING"
        MASTER_STREAM = "LocalMaster:{}".format(LocalMaster)
        links ="{0}{1}".format(HostLocalStream,LocalMaster)
        if not CheckPlayMpd("8000/{}".format(LocalMaster)):
            print("Play audio form local: {}".format(LocalMaster))
            playAudio(links)
   
   elif(CheckStream(HostRadioTech,MASTER1)):
      STREAM_RUNNING_TIMEOUT = 15
      STREAM_STATE_STR = "RUNNING"
      MASTER_STREAM = MASTER1
      links ="{0}{1}".format(HostRadioTech,MASTER1)
      #print(links)
      if not CheckPlayMpd(MASTER1):
          STREAM_STATE_STR = "RUNNING"
          MASTER_STREAM = MASTER1
          links ="{0}{1}".format(HostRadioTech,MASTER1)
          print("Check stream")
          playAudio(links)
   elif (CheckStream(HostRadioTech,MASTER2)):
         STREAM_RUNNING_TIMEOUT = 15
         STREAM_STATE_STR = "RUNNING"
         MASTER_STREAM = MASTER2
         if not CheckPlayMpd(MASTER2):
            links ="{0}{1}".format(HostRadioTech,MASTER2)
            print("Check stream")
            playAudio(links)
   elif (CheckStream(HostRadioTech,MASTER3)):
         STREAM_RUNNING_TIMEOUT = 15
         STREAM_STATE_STR = "RUNNING"
         MASTER_STREAM = MASTER3
         if not CheckPlayMpd(MASTER3):
            links ="{0}{1}".format(HostRadioTech,MASTER3)
            print("Check stream")
            playAudio(links)
   else:
         STREAM_STATE_STR = "IDLE"
         STREAM_STATE = False
         #StopMpd()
def SerialProcess(data):
     global VOLUME,StatePlayOld,SongId,PageModeLcd
     #print(data)
     if data.find('Volume+') != -1:
          VOLUME = VOLUME + 5
          SetVolume(VOLUME)
          SendSerial(ser,"j1.val=%d" % (VOLUME))
          SendSerial(ser,"t34.txt=\"%d\"" % (VOLUME))
     if data.find('Volume-') != -1:
          if VOLUME >5:
              VOLUME = VOLUME - 5
          SetVolume(VOLUME)
          SendSerial(ser,"j1.val=%d" % (VOLUME))
          SendSerial(ser,"t34.txt=\"%d\"" % (VOLUME))
     if data.find('page') != -1:
          try:
              PageModeLcd = int(data[4:])
              print("Page %d" % (PageModeLcd))
          except:
               print("Error get data")
               print(data[4:])
     if data.find('Play') != -1:
            try:
                SongId = int(data[4:])
                PlayMpd(SongId)
            except:
                print("Play error")
     if StatePlayOld.find('stop') != -1:
        if data.find('play') != -1:
           PlayMpd(SongId)
           print("Play Id = %d" %(SongId))
     elif  StatePlayOld.find('play')  != -1:
           if data.find('play') != -1:
               PauseMpd(1) 
               print("Pause Start")
     elif  StatePlayOld.find('pause') != -1:
           if data.find('play') != -1:
               PauseMpd(0)
               print("Pause Stop")
     if data.find('next') != -1:
           NextMpd()
           print("Next")
     if data.find('previous') != -1:
           PreviousMpd()
           print("Previous")
     if data.find('stop') != -1:
           StopMpd()
           print("Stop")
while True:
        try:
            received_data = ser.read() #read serial port except AttributeError: 
            time.sleep(0.03) 
            data_left = ser.inWaiting() #check for remaining byte 
            received_data += ser.read(data_left)
            #print (received_data)
            if len(received_data)>0: 
                dataRev = received_data.decode('utf-8', errors='replace') 
                SerialProcess(dataRev)
        except AttributeError:
          pass
