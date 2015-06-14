__all__ = ["ServerInfo"]

import psutil
import time
from execute_async import ExecuteAsync

class ServerInfo(object):
  
  @staticmethod
  def Create():
    server_info = {}
    command = ExecuteAsync("uname -m")
    command.Run()
    (status, output) = command.GetResponse() 
    if status.IsOk():
      server_info["architecture"] = output[:-1]
    command = ExecuteAsync("pwd")
    command.Run()
    (status, output) = command.GetResponse() 
    if status.IsOk():
      server_info["work_dir"] = output[:-1]
    command = ExecuteAsync("uname -v")
    command.Run()
    (status, output) = command.GetResponse() 
    if status.IsOk():
      server_info["distribution"] = output[:-1]
    command = ExecuteAsync("uname -sr")
    command.Run()
    (status, output) = command.GetResponse() 
    if status.IsOk():
      server_info["kernel"] = output[:-1]
    server_info["disk_usage"] = ServerInfo.disk_usage()
    server_info["virtual_memory"] = ServerInfo.virtual_memory()
    server_info["access_time"] = time.asctime()
    return server_info
  
  @staticmethod
  def virtual_memory():
    total = psutil.virtual_memory().total >> 20
    percent = psutil.virtual_memory().percent
    used = psutil.virtual_memory().used >> 20
    free = psutil.virtual_memory().free >> 20
    virtual_memory = "total=%dMB, used=%dMB, free=%dMB, percent=%s" % (\
        total, used, free, str(percent) + '%')
    return virtual_memory

  @staticmethod
  def disk_usage():
    total = psutil.disk_usage('/').total >> 30
    percent = psutil.disk_usage('/').percent
    free = psutil.disk_usage('/').free >> 30
    used = psutil.disk_usage('/').used >> 30
    disk_usage = "total=%dGB, used=%dGB, free=%dGB, percent=%s" % (\
        total, used, free, str(percent) + '%')
    return disk_usage

if __name__ == "__main__":
  for item in ServerInfo.Create().iteritems():
    print item
