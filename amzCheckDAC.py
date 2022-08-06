import subprocess
def ReadAudioOutput():
    command = ['aplay -l', '-l']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True,shell=True)
    text = p.stdout.read()
    retcode = p.wait()
    #print(text)
    return text
def CheckDac():
    audioOutput = ReadAudioOutput()
    if audioOutput.find("card 3:")!=-1:
      return True
    return False
