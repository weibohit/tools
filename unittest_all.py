import os
from utility import file_helper

if __name__ == "__main__":
  file_path = "./static/frequency_scanning.csv"
  status = file_helper.LoadDataFromStaticDir(file_path)
  if status.IsError():
    print status.Message()

  for rootdir, subdir, files in os.walk("./"):
    for item in files:
      if item.endswith(".pyc"):
        try:
          os.remove(rootdir + "/" + item)
        except:
          pass
