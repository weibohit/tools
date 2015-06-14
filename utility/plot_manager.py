__all__ = ["PlotManager"]

import os
import math
import matplotlib.pyplot as plt
from utility.log import VLOG
#import Tkinter

""" This class helps local controller machine process
the data renderring routines besides the WebGL renderring
which is implemented by JavaScript. This helper mainly use
the matplotlib as its low level data process """

class PlotManager(object):
  minor_threshold = -100.0

  @staticmethod
  def Show():
    plt.show()

  @staticmethod
  def Scatter(path):
    x = []
    y = []
    try:
      fd = open(path)
    except:
      VLOG(3, "Failed to find valid data file from: %s" % path)
    for lines in fd:
      token = lines[:-1].split(',')
      try:
        int(token[0])
      except:
        continue
      if float(token[1]) > PlotManager.minor_threshold:
        x.append(int(token[0]))
        y.append(float(token[1]))
    fd.close()
    plt.figure(figsize=(10, 10))
    plt.plot(x[1:], y[1:], linewidth=2.0, color='b')
    plt.xlabel('Current Theta Angle')
    plt.ylabel('S21 Gain in Decibel')
    plt.title('Antenna S21 2D Plot')
    plt.axis([min(x), max(x) + 10, min(y), max(y) + 3])
    plt.grid(b=True, which='major', color='r', linestyle='-', alpha=0.5)
    plt.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
    plt.minorticks_on()
    # should not block multiple figure draw
    plt.draw()

  @staticmethod
  def MultiScatter(path_list):
    color_pool = ['b', 'r', 'g', 'y', 'k']
    color_index = 0
    plt.figure(figsize=(10, 10))
    plt.xlabel('Current Theta Angle')
    plt.ylabel('S21 Gain in Decibel')
    plt.title('Antenna S21 2D Plot')
    plt.grid(b=True, which='major', color='r', linestyle='-', alpha=0.5)
    plt.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
    plt.minorticks_on()
    for path in path_list:
      x = []
      y = []
      try:
        fd = open(path)
      except:
        VLOG(3, "Failed to find valid data file from: %s" % path)
      for lines in fd:
        token = lines[:-1].split(',')
        try:
          int(token[0])
        except:
          continue
        if float(token[1]) > PlotManager.minor_threshold:
          x.append(int(token[0]))
          y.append(float(token[1]))
      fd.close()
      plt.plot(x, y, linewidth=2.0, color=color_pool[color_index])
      color_index += 1
      # should not block multiple figure draw
      plt.draw()

  @staticmethod
  def ShareScatter(path_list):
    color_pool = ['b', 'r', 'g', 'y', 'k']
    color_index = 0
    spot_label = [221, 222, 223, 224]
    plt.figure(figsize=(10, 10))
    for path in path_list:
      plt.subplot(spot_label[color_index])
      plt.xlabel('Current Theta Angle', fontsize=10)
      plt.ylabel('S21 Gain in Decibel', fontsize=10)
      plt.title('Antenna S21 2D Plot', fontsize=10)
      plt.grid(b=True, which='major', color='r', linestyle='-', alpha=0.5)
      plt.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
      plt.minorticks_on()
      x = []
      y = []
      try:
        fd = open(path)
      except:
        VLOG(3, "Failed to find valid data file from: %s" % path)
      for lines in fd:
        token = lines[:-1].split(',')
        try:
          int(token[0])
        except:
          continue
        if float(token[1]) > PlotManager.minor_threshold:
          x.append(int(token[0]))
          y.append(float(token[1]))
      fd.close()
      plt.plot(x, y, linewidth=2.0, color=color_pool[color_index])
      color_index += 1
      # should not block multiple figure draw
      plt.draw()

  @staticmethod
  def Polar(path):
    plt.figure(figsize=(10, 10))
    plt.axes(polar=True)
    x = []
    y = []
    try:
      fd = open(path)
    except:
      VLOG(3, "Failed to find valid data file from: %s" % path)
    for lines in fd:
      token = lines[:-1].split(',')
      try:
        int(token[0])
      except:
        continue
      if float(token[1]) > PlotManager.minor_threshold:
        x.append(int(token[0]))
        y.append(float(token[1]))
    fd.close()
    # rebase the minor value to be zero
    for i in range(len(x)):
      y[i] = y[i] - min(y)
      x[i] = float(x[i]) * math.pi / 180.0
    plt.plot(x, y, linewidth=2.0, color='b')
    plt.title('Antenna S21 Polar Plot')
    plt.grid(b=True, which='major', color='r', linestyle='-', alpha=0.5)
    plt.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
    plt.minorticks_on()
    # should not block multiple figure draw
    plt.draw()

  @staticmethod
  def MultiPolar(path_list):
    color_pool = ['b', 'r', 'g', 'y', 'k']
    color_index = 0
    plt.figure(figsize=(10, 10))
    plt.axes(polar=True)
    for path in path_list:
      x = []
      y = []
      try:
        fd = open(path)
      except:
        VLOG(3, "Failed to find valid data file from: %s" % path)
      for lines in fd:
        token = lines[:-1].split(',')
        try:
          int(token[0])
        except:
          continue
        if float(token[1]) > PlotManager.minor_threshold:
          x.append(int(token[0]))
          y.append(float(token[1]))
      fd.close()
      # rebase the minor value to be zero
      for i in range(len(x)):
        y[i] = y[i] - min(y)
        x[i] = float(x[i]) * math.pi / 180.0
      plt.plot(x, y, linewidth=2.0, color=color_pool[color_index])
      color_index += 1
      plt.title('Antenna S21 Polar Plot')
      plt.grid(b=True, which='major', color='r', linestyle='-', alpha=0.5)
      plt.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
      plt.minorticks_on()
      # should not block multiple figure draw

  @staticmethod
  def SharePolar(path_list):
    color_pool = ['b', 'r', 'g', 'y', 'k']
    color_index = 0
    spot_label = [221, 222, 223, 224]
    plt.figure(figsize=(10, 10))
    for path in path_list:
      #plt.axes(polar=True)
      plt.subplot(spot_label[color_index], polar=True)
      plt.title('Antenna S21 2D Plot', fontsize=10)
      plt.grid(b=True, which='major', color='r', linestyle='-', alpha=0.5)
      plt.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
      plt.minorticks_on()
      x = []
      y = []
      try:
        fd = open(path)
      except:
        VLOG(3, "Failed to find valid data file from: %s" % path)
      for lines in fd:
        token = lines[:-1].split(',')
        try:
          int(token[0])
        except:
          continue
        if float(token[1]) > PlotManager.minor_threshold:
          x.append(int(token[0]))
          y.append(float(token[1]))
      fd.close()
      # rebase the minor value to be zero
      for i in range(len(x)):
        y[i] = y[i] - min(y)
        x[i] = float(x[i]) * math.pi / 180.0
      plt.plot(x, y, linewidth=2.0, color=color_pool[color_index])
      color_index += 1
      # should not block multiple figure draw
      plt.draw()

  @staticmethod
  def Bar(path):
    x = []
    y = []
    try:
      fd = open(path)
    except:
      VLOG(3, "Failed to find valid data file from: %s" % path)
    for lines in fd:
      token = lines[:-1].split(',')
      try:
        int(token[0])
      except:
        continue
      if float(token[1]) > PlotManager.minor_threshold:
        x.append(int(token[0]))
        y.append(float(token[1]))
    fd.close()
    plt.figure(figsize=(10, 10))
    plt.gca().set_axis_bgcolor('red')
    plt.bar(x, y, alpha=1, width=1.8, align='center', color='w')
    plt.xlabel('Current Theta Angle')
    plt.ylabel('S21 Gain in Decibel')
    plt.axis([min(x), max(x), min(y), max(y) + 3])
    plt.title('Antenna S21 2D Plot')
    plt.grid(False)
    # should not block multiple figure draw
    plt.draw()

  @staticmethod
  def ShareBar(path_list):
    fig = plt.figure(figsize=(10, 10))
    color_pool = ['blue', 'red', 'green', 'yellow']
    color_index = 0
    spot_label = [221, 222, 223, 224]
    for path in path_list:
      ax = fig.add_subplot(spot_label[color_index])
      ax.patch.set_facecolor(color_pool[color_index])
      color_index += 1
      x = []
      y = []
      try:
        fd = open(path)
      except:
        VLOG(3, "Failed to find valid data file from: %s" % path)
      for lines in fd:
        token = lines[:-1].split(',')
        try:
          int(token[0])
        except:
          continue
        if float(token[1]) > PlotManager.minor_threshold:
          x.append(int(token[0]))
          y.append(float(token[1]))
      fd.close()
      plt.bar(x, y, alpha=1, width=1.8, align='center', color='w')
      plt.xlabel('Current Theta Angle', fontsize=10)
      plt.ylabel('S21 Gain in Decibel', fontsize=10)
      plt.axis([min(x), max(x), min(y), max(y) + 3])
      plt.title('Antenna S21 2D Plot', fontsize=10)
      plt.grid(False)
      # should not block multiple figure draw
      plt.draw()
