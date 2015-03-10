import os
import math
import sys
from status import *

def LoadDataFromStaticDir(path):
  if not os.path.isfile(path):
    return Status(kUnknownError, path + " doesn't exist.")

  try:
    fd = open(path, 'r')
  except IOError, e:
    return Status(kUnknownError, e)

  try:
    fd_output = open('static/output.csv', 'w+')
  except IOError, e:
    fd.close()
    return Status(kUnknownError, e)

  print len(fd.readlines())
  fd.seek(0)

  # header for output csv data
  fd_output.write("x,y,z,\n")

  for line in fd.readlines():
    vector = line[:-1].split(',')
    angle = float(vector[0]) / 180.0 * math.pi
    data = float(vector[1])
    x = round(math.cos(angle) * data, 9)
    y = round(math.sin(angle) * data, 9)
    # convert to string
    x_str = "{:.9f}".format(x)
    y_str = "{:.9f}".format(y)
    z_str = "{:.9f}".format(0.0)
    fd_output.write(x_str + "," + y_str + "," + z_str + ",\n")

  fd.close()
  fd_output.close()
  return Status(kOk)

def LoadDataFromCST():
  try:
    fd_output = open('static/microstrip.csv', 'w+')
  except IOError, e:
    fd.close()
    return Status(kUnknownError, e)

  # header for output csv data
  fd_output.write("x,y,z,\n")

  # format xoy
  try:
    fd = open('static/xoy.csv', 'r')
  except IOError, e:
    return Status(kUnknownError, e)

  for line in fd.readlines():
    vector = line[:-1].split(',')
    angle = float(vector[0]) / 180.0 * math.pi
    data = float(vector[1])
    x = round(math.cos(angle) * data, 9)
    y = round(math.sin(angle) * data, 9)
    # convert to string
    x_str = "{:.9f}".format(x)
    y_str = "{:.9f}".format(y)
    z_str = "{:.9f}".format(0.0)
    fd_output.write(x_str + "," + y_str + "," + z_str + ",\n")

  fd.close()

  # format xoz
  try:
    fd = open('static/xoz.csv', 'r')
  except IOError, e:
    return Status(kUnknownError, e)

  for line in fd.readlines():
    vector = line[:-1].split(',')
    angle = float(vector[0]) / 180.0 * math.pi
    data = float(vector[1])
    z = round(math.cos(angle) * data, 9)
    x = round(math.sin(angle) * data, 9)
    # convert to string
    x_str = "{:.9f}".format(x)
    z_str = "{:.9f}".format(z)
    y_str = "{:.9f}".format(0.0)
    fd_output.write(x_str + "," + y_str + "," + z_str + ",\n")

  fd.close()

  # format yoz
  try:
    fd = open('static/yoz.csv', 'r')
  except IOError, e:
    return Status(kUnknownError, e)

  for line in fd.readlines():
    vector = line[:-1].split(',')
    angle = float(vector[0]) / 180.0 * math.pi
    data = float(vector[1])
    z = round(math.cos(angle) * data, 9)
    y = round(math.sin(angle) * data, 9)
    # convert to string
    y_str = "{:.9f}".format(y)
    z_str = "{:.9f}".format(z)
    x_str = "{:.9f}".format(0.0)
    fd_output.write(x_str + "," + y_str + "," + z_str + ",\n")

  fd.close()
  fd_output.close()
  return Status(kOk)
