__all__ = ["SCPI"]

import socket
import time
from utility.log import VLOG
from utility.status import *

class SCPI(object):

  def __init__(self, host_ip):
    self.host_ip = host_ip
    self.port = 1024
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((host_ip, self.port))

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
    self.client.send("CALCulate" + n + ":PARameter:DEFine '" + \
        prefix_var + "'," + method + "\n")

  def CreateTraceAssotiateWithVar(self, method, n):
    prefix_var = "Measure" + method;
    self.client.send("DISPlay:WINDow1:TRACe" + n + ":FEED '" + \
        prefix_var + "'\n")

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
    #self.client.send("CALC" + n + ":MARK" + n + ":FORMat LOGPhase\n")
    self.client.send("CALC" + n + ":MARK" + n + ":FORMat MLOG\n")
    #self.client.send("CALC" + n + ":MARK" + n + ":FORMat \n")
    pass

  def GetMarkerX(self, n):
    self.client.send("CALC" + n + ":MARK" + n + ":X?\n")
    return self.client.recv(100)

  def GetMarkerY(self, n):
    self.client.send("CALC" + n + ":MARK" + n + ":Y?\n")
    return self.client.recv(100)

  def Close(self):
    self.client.close()
