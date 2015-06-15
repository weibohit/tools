import sys
import os
from utility.plot_manager import PlotManager

if __name__ == "__main__":

  if len(sys.argv) <= 1:
    print "usage: python answer.py `file1` `file`"
    sys.exit(-1)

  if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]) \
      and sys.argv[1].endswith('csv'):
    PlotManager.Scatter(sys.argv[1])
    PlotManager.Polar(sys.argv[1])
    PlotManager.Bar(sys.argv[1])
    PlotManager.Show()
    sys.exit(0)

  if len(sys.argv) > 2 and len(sys.argv) <=5:
    file_list = []
    for item in sys.argv[1:]:
      if os.path.isfile(item) and item.endswith('csv'):
        file_list.append(item)
    PlotManager.MultiScatter(file_list)
    PlotManager.ShareScatter(file_list)
    PlotManager.MultiPolar(file_list)
    PlotManager.SharePolar(file_list)
    PlotManager.ShareBar(file_list)
    PlotManager.Show()
    sys.exit(0)

  if len(sys.argv) > 5:
    print "current version only support 4 file"
    sys.exit(-1)
