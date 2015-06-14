__all__ = ["ExecuteAsync"]

import re
import subprocess
import threading
from status import *

""" since python' subprocess module does not support manual
timeout setting. This class binds the wanted commands and post
the task to another thread which can be under control in timeout
setting calling thread.join(timeout) """

class ExecuteAsync(object):

  def __init__(self, cmd="", timeout=3):
    self.cmd = cmd
    self.timeout = timeout
    self.process = None
    self.stdout = ""
    self.stderr = ""
    self.is_timeout = False
    self.Run()

  def Task(self):
    self.process = subprocess.Popen(\
        self.cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (self.stdout, self.stderr) = self.process.communicate()
    return

  def Run(self):
    thread = threading.Thread(target=self.Task)
    thread.start()
    thread.join(self.timeout)
    if thread.is_alive():
      self.is_timeout = True
      self.process.terminate()
      thread.join()
    return

  # return status and response<string> 
  def GetResponse(self):
    # handle timeout error
    if self.is_timeout:
      msg = "%s command timed out after %s seconds" \
          % (self.cmd, str(self.timeout))
      return (Status(kTimeout, msg), "")
    # handle command execute shell-like error,
    # etc. command unregconize or spelled error
    if self.stderr:
      return (Status(kUnknownError, "Failed to run %s command" % self.cmd), "")
    # handle adb execute error
    matchObj = re.search(r'error', self.stdout, re.I)
    if matchObj:
      return (Status(kUnknownError, \
          "Failed to run %s command, detailed message: %s" \
          % (self.cmd, self.stdout)), "")
    return (Status(kOk), self.stdout)
    
