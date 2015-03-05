from utility.log import VLOG
from utility.status import *
import serial
import time

class SerialImpl(object):

  def __init__(self):
    # Serial Port RS232 basic configure parameters
    self.ser_ = serial.Serial('/dev/ttyUSB0')
    self.ser_.setBaudrate(9600)
    self.ser_.setStopbits(serial.STOPBITS_ONE)
    self.ser_.setByteSize(serial.EIGHTBITS)
    self.ser_.setParity(serial.PARITY_NONE)
    self.ser_.setTimeout(3)
    self.ser_.setWriteTimeout(3)
    self.ser_.flushInput()
    self.ser_.flushOutput()
    self.ShowParameters()

  def Defaut(self):
    # Serial Port RS232 basic configure parameters
    self.ser_.setBaudrate(9600)
    self.ser_.setStopbits(serial.STOPBITS_ONE)
    self.ser_.setByteSize(serial.EIGHTBITS)
    self.ser_.setParity(serial.PARITY_NONE)
    self.ser_.setTimeout(3)
    self.ser_.setWriteTimeout(3)
    self.ser_.flushInput()
    self.ser_.flushOutput()
    return self.ShowParameters()

  def IsOpen(self):
    return self.ser_.isOpen()

  def Close(self):
    if self.IsOpen():
      self.ser_.close()

  def SetReadTimeout(self, timeout):
    try:
      self.ser_.setTimeout(timeout)
    except serial.SerialException, e:
      VLOG(3, e)
      return Status(kUnknownError, e)
    VLOG(0, "set read timeout %d" % self.ser_.timeout)
    return Status(kOk)

  def readtimeout(self):
    return self.ser_.timeout

  def SetWriteTimeout(self, timeout):
    try:
      self.ser_.setWriteTimeout(timeout)
    except serial.SerialException, e:
      VLOG(3, e)
      return Status(kUnknownError, e)
    VLOG(0, "set write timeout %d" % self.ser_.writeTimeout)
    return Status(kOk)

  def writetimeout(self):
    return self.ser_.writeTimeout

  def SetBaudRate(self, baudrate):
    try:
      self.ser_.setBaudrate(baudrate)
    except serial.SerialException, e:
      VLOG(3, e)
      return Status(kUnknownError, e)
    VLOG(0, "set baudrate %d" % self.ser_.stopbits)
    return Status(kOk)

  def baudrate(self):
    return self.ser_.baudrate

  def SetStopBits(self, stopbits):
    try:
      self.ser_.setStopbits(stopbits)
    except serial.SerialException, e:
      VLOG(3, e)
      return Status(kUnknownError, e)
    VLOG(0, "set stopbit %d" % self.ser_.stopbits)
    return Status(kOk)

  def stopbits(self):
    return self.ser_.stopbits

  def SetByteSize(self, bytesize):
    try:
      self.ser_.setByteSize(bytesize)
    except serial.SerialException, e:
      VLOG(3, e)
      return Status(kUnknownError, e)
    VLOG(0, "set bytesize %d" % self.ser_.bytesize)
    return Status(kOk)

  def bytesize(self):
    return self.ser_.bytesize

  def SetParity(self, parity):
    try:
      self.ser_.setParity(parity)
    except serial.SerialException, e:
      VLOG(3, e)
      return Status(kUnknownError, e)
    VLOG(0, "set parity %s" % self.ser_.parity)
    return Status(kOk)

  def parity(self):
    return self.ser_.parity

  def ShowParameters(self):
    declaim = "\
    -----------------------------------------\n\
    |       Basic Parameters of RS232       |\n\
    -----------------------------------------\n\
    | fileno: " + str(self.ser_.fileno()) + "\n\
    | port: " + self.ser_.getPort() + "\n\
    | baudrate: " + str(self.ser_.baudrate) + "\n\
    | bytesize: " + str(self.ser_.bytesize) + "\n\
    | stopbits: " + str(self.ser_.stopbits) + "\n\
    | parity: " + self.ser_.parity + "\n\
    | read-timeout: " + str(self.ser_.timeout) + "\n\
    | write-timeout: " + str(self.ser_.writeTimeout) + "\n\
    -----------------------------------------"
    print declaim
    return Status(kOk)

  def ForTest(self):
    VLOG(0, "Should move this blocks when RS232 passed.")
    status = self.SetBaudRate(115200)
    if status.IsError():
      return status

    self.SetStopBits(serial.STOPBITS_TWO)
    if status.IsError():
      return status

    self.SetByteSize(serial.SEVENBITS)
    if status.IsError():
      return status

    self.SetParity(serial.PARITY_EVEN)
    if status.IsError():
      return status

    self.SetReadTimeout(1)
    if status.IsError():
      return status

    self.SetWriteTimeout(1)
    if status.IsError():
      return status

    return self.ShowParameters()

  def LoopBackTest(self):
    VLOG(1, "connect TX and Rx pin in 5 second.")
    time.sleep(5)
    tx_data = "\
    -----------------------------------------\n\
    |          Loop Back Test RS232          |\n\
    -----------------------------------------\n\
    | fileno: " + str(self.ser_.fileno()) + "\n\
    | port: " + self.ser_.getPort() + "\n\
    | baudrate: " + str(self.ser_.baudrate) + "\n\
    | bytesize: " + str(self.ser_.bytesize) + "\n\
    | stopbits: " + str(self.ser_.stopbits) + "\n\
    | parity: " + self.ser_.parity + "\n\
    | read-timeout: " + str(self.ser_.timeout) + "\n\
    | write-timeout: " + str(self.ser_.writeTimeout) + "\n\
    -----------------------------------------"
    self.Write(tx_data)
    rx_data = self.Read()
    if rx_data != tx_data:
      error = "failed loopback test RS232."
      VLOG(3, error)
      return Status(kUnknownError, error)
    VLOG(0, "success loopback test RS232:\n %s" % rx_data)
    return Status(kOk)

  # return void whatever
  def Write(self, data):
    try:
      self.ser_.write(data)
    except serial.SerialTimeoutException, e:
      VLOG(3, e)

  # return receive data
  def Read(self):
    return self.ser_.read(size=1024)

