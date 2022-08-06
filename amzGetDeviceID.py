import random

n = random.randint(0,999999999999999)
def getDeviceID():
  # Extract serial from cpuinfo file
  seri  = int(n)
  cpuserial = str(seri)
  cpuserial = cpuserial.rjust(15,'0')
  try:
    f = open('/sys/block/mmcblk0/device/cid','r')
    #for line in f:
    #  if line[0:6]=='Serial':
    seri  = f.readline()
    cpuserial = int(seri,16)
    id = str(cpuserial)
    lenght = len(id)
    cpuseria  = id[-15:]
    #print("Get ID full  ID {}".format(id))
    #cpuseria = cpuseria.rjust(15,'0')
        #cpuserial = "111100064567895"   
    #print("Get ID full  ID {}".format(cpuseria))
    cpuserial = cpuseria
    f.close()
  except:
      print("Get default not found ")
  return str(cpuserial)
