from utility.log import VLOG
from utility.status import *

class SerialImpl(object):

  def __init__(self):
    # Serial Port RS232 basic configure parameters
    self.baud_rate_ = 9600
    self.stop_bit_ = 1
    self.bit_ = 8
    self.check_ = "none"

  def SetBaudRate(self, baud_rate):
    if type(baud_rate) != int:
      status = Status(kUnknownError, "Baud rate must be integer.")
      VLOG(3, status.Message())
      return status
    self.baud_rate_ = baud_rate
    VLOG(0, "Set baud rate at %d" % self.baud_rate_)
    return Status(kOk)

  def baud_rate(self):
    return self.baud_rate

  def SetStopBit(self, stop_bit):
    if type(stop_bit) == int and stop_bit >= 0 and stop_bit <= 2:
      self.stop_bit_ = stop_bit
      VLOG(0, "Set stop bit %d" % self.stop_bit_)
      return Status(kOk)
    status = Status(kUnknownError, "Invalid stop bit.")
    VLOG(3, status.Message())
    return status

  def stop_bit(self):
    return self.stop_bit

  def SetBit(self, bit):
    if type(bit) == int:
      self.bit_ = bit
      VLOG(0, "Set bit %d" % self.bit_)
      return Status(kOk)
    status = Status(kUnknownError, "Invalid bit counts.")
    VLOG(3, status.Message())
    return status

  def bit(self):
    return self.bit_

  def SetCheck(self, check):
    if type(check) != str:
      status = Status(kUnknownError, "Invalid check type")
      VLOG(3, status.Message())
      return status
    elif check.lower() == "none":
      self.check_ = "none"
      VLOG(0, "Set check type %s" % self.check_)
      return Status(kOk)
    elif check.lower() == "odd":
      self.check_ = "odd"
      VLOG(0, "Set check type %s" % self.check_)
      return Status(kOk)
    elif check.lower() == "even":
      self.check_ = "even"
      VLOG(0, "Set check type %s" % self.check_)
      return Status(kOk)
    else:
      status = Status(kUnknownError, "Invalid check type")
      VLOG(3, status.Message())
      return status

  def check(self):
    return self.check_

