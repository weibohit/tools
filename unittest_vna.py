import socket
import time

class SCPI(object):

  def __init__(self, host_ip):
    self.host_ip = host_ip
    self.port = 1024
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((host_ip, self.port))

  def Close(self):
    self.client.close()

  def Wait(self):
    self.client.send("*WAI\n")

  def RST(self):
    self.client.send("*RST\n")

  def CLS(self):
    self.client.send("*CLS\n")

  # select trace n in window1
  def ActivateTrace(self, n):
    self.client.send("DISPlay:WINDow1:TRACe" + n + ":SElect\n")

  # delete trace n in window1
  def ClearTrace(self, n):
    self.client.send("DISPlay:WINDow1:TRACe" + n + ":DElete\n")

  def CreateMeasureVar(self, method, n):
    # e.g S11 ---> MeasureS11
    prefix_var = "Measure" + method;
    self.client.send("CALCulate" + n + ":PARameter:DEFine '" + prefix_var + "'," + method + "\n")

  def CreateTraceAssotiateWithVar(self, method, n):
    prefix_var = "Measure" + method;
    self.client.send("DISPlay:WINDow1:TRACe" + n + ":FEED '" + prefix_var + "'\n")

  def SetRange(self, start, stop, n):
    # set frequency range
    self.client.send("SENSe" + n + ":FREQuency:START " + start + "\n")
    self.client.send("SENSe" + n + ":FREQuency:STOP " + stop + "\n")

  def CreateMark(self, n):
    self.client.send("CALC" + n + ":MARK" + n + ":STAT ON\n")

  def SetMarkFreq(self, n, Freq):
    # set start frequency
    self.client.send("CALC" + n + ":MARK" + n + ":X " + Freq + "\n")

  def MarkerFormat(self, n):
    #self.client.send("CALC" + n + ":MARK" + n + ":FORMat DEFault\n")
    self.client.send("CALC" + n + ":MARK" + n + ":FORMat MLOG\n")

  def GetMarkerX(self, n):
    self.client.send("CALC" + n + ":MARK" + n + ":X?\n")
    return self.client.recv(1024)

  def GetMarkerY(self, n):
    self.client.send("CALC" + n + ":MARK" + n + ":Y?\n")
    return self.client.recv(1024)

if __name__ == "__main__":

  vna =  SCPI("192.168.1.11")
#  vna.RST()
#  vna.CLS()
  vna.ClearTrace('1')
  vna.CreateMeasureVar('S11', '1')
  vna.CreateTraceAssotiateWithVar('S11', '1')
  vna.SetRange('1GHz', '3GHz', '1')
  vna.CreateMark('1')
  vna.MarkerFormat('1')
  vna.SetMarkFreq('1', '2.4GHz')
  vna.Wait()

  freq = vna.GetMarkerX('1')
  print freq
  vna.Wait()
  db = vna.GetMarkerY('1')
  print db

