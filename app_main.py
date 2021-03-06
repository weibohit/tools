from flask import Flask
from flask import g
from flask import render_template
from flask import request
import optparse
import os
import math
import sys
import time
from driver.serial_impl import SerialImpl
from driver.scpi import SCPI
from utility.log import InitLogging
from utility.log import VLOG
from utility.server_info import ServerInfo
from utility.status import *

# global var
app = Flask(__name__)
app_serial = None
app_scpi = None
reverse = False

@app.before_request
def server_info_init():
  g.server_info = ServerInfo.Create()

@app.route('/multiples')
def multiples():
  return render_template('multiple_done.html')

@app.route('/multiple.html')
def multiple():
  return render_template('multiple.html')

@app.route('/pre_start_emf.html')
def pre_start_emf():
  return render_template('pre_start_emf.html')

# multiple data process, current support 6 points
# data will be saved as "multi-2.5G.csv" like
@app.route('/points/<f1>/<f2>/<f3>/<f4>/<f5>/<f6>')
def multiple_points_emf(f1, f2, f3, f4, f5, f6):
  # check the validation of fn
  plist = []
  try:
    if 0.04 < float(f1) and float(f1) < 20:
      plist.append(float(f1))
  except:
    VLOG(0, "invalid interested frequency points" + f1)
  try:
    if 0.04 < float(f2) and float(f2) < 20:
      plist.append(float(f2))
  except:
    VLOG(0, "invalid interested frequency points" + f2)
  try:
    if 0.04 < float(f3) and float(f3) < 20:
      plist.append(float(f3))
  except:
    VLOG(0, "invalid interested frequency points" + f3)
  try:
    if 0.04 < float(f4) and float(f4) < 20:
      plist.append(float(f4))
  except:
    VLOG(0, "invalid interested frequency points" + f4)
  try:
    if 0.04 < float(f5) and float(f5) < 20:
      plist.append(float(f5))
  except:
    VLOG(0, "invalid interested frequency points" + f5)
  try:
    if 0.04 < float(f6) and float(f6) < 20:
      plist.append(float(f6))
  except:
    VLOG(0, "invalid interested frequency points" + f6)
  VLOG(0, "current valid interested frequency points" + str(plist))
  # loop for the items of plist
  for item in plist:
    # file for store
    time_tag = time.strftime("%Y%m%d-%H:%M%p", time.localtime())
    file_name = "static/multi-" + time_tag + '-' + str(item) + "G.csv"
    fd_output = open(file_name, 'w+')
    fd_output.write("Freq=" + str(item) + "G,dB\n")

    # init Motor
    app_serial = SerialImpl()
    # init VNA
    app_scpi = SCPI("192.168.0.11")
    app_scpi.RST()
    app_scpi.CLS()
    app_scpi.ClearTrace('1')
    app_scpi.CreateMeasureVar('S21', '1')
    app_scpi.CreateTraceAssotiateWithVar('S21', '1')
    app_scpi.SetRange('0.045GHz', '19.95GHz', '1')
    app_scpi.CreateMark('1')
    app_scpi.MarkerFormat('1')
    app_scpi.SetMarkFreq('1', str(item) + 'GHz')
    app_scpi.GetMarkerY('1')
    # power on Motor
    for i in range(180):
      src = app_scpi.GetMarkerY('1')
      dB_str = src.split(",")[0]
      print dB_str
      beishu = dB_str.split("e")[0]
      zhishu = dB_str.split("e")[1]
      dB = float(beishu) * float(10 ** float(zhishu))
      print ">>>>>>>> ....." + str(dB)
      dB_str = "{:.9f}".format(dB)
      fd_output.write(str(i*2) + "," + dB_str + "\n")
      if reverse:
        app_serial.Write("{CUR20;MCS16;SPD5000;STP4280;ENA;};")
      else:
        app_serial.Write("{CUR20;MCS16;SPD5000;STP-4280;ENA;};")
      time.sleep(1)
    # shutdown
    fd_output.close()
    app_serial.Write("OFF;")
    app_scpi.Close()
    global reverse
    reverse = not reverse
  return render_template('multiple_done.html')

# data saved in file "real_s21.csv"
# display in Chart format
# request "real_s21" in url to get landed
@app.route('/start_emf_chart/<center>/<start>/<stop>')
def start_emf_chart(center, start, stop):
  center_freq = center + 'GHz'
  start_freq = start + 'GHz'
  stop_freq = stop + 'GHz'
  # file for store
  fd_output = open('static/real_s21.csv', 'w+')
  fd_output.write("Freq,dB\n")

  # init Motor
  app_serial = SerialImpl()
  # init VNA
  app_scpi = SCPI("192.168.0.11")
  app_scpi.RST()
  app_scpi.CLS()
  app_scpi.ClearTrace('1')
  app_scpi.CreateMeasureVar('S21', '1')
  app_scpi.CreateTraceAssotiateWithVar('S21', '1')
  app_scpi.SetRange(start_freq, stop_freq, '1')
  app_scpi.CreateMark('1')
  app_scpi.MarkerFormat('1')
  app_scpi.SetMarkFreq('1', center_freq)
  # power on Motor
  app_scpi.GetMarkerY('1')
  for i in range(180):
    src = app_scpi.GetMarkerY('1')
    dB_str = src.split(",")[0]
    print dB_str
    beishu = dB_str.split("e")[0]
    zhishu = dB_str.split("e")[1]
    dB = float(beishu) * float(10 ** float(zhishu))
    print ">>>>>>>> ....." + str(dB)
    dB_str = "{:.9f}".format(dB)
    fd_output.write(str(i*2) + "," + dB_str + "\n")
    if reverse:
      app_serial.Write("{CUR20;MCS16;SPD5000;STP4280;ENA;};")
    else:
      app_serial.Write("{CUR20;MCS16;SPD5000;STP-4280;ENA;};")
    time.sleep(1)
  # shutdown
  fd_output.close()
  app_serial.Write("OFF;")
  app_scpi.Close()
  global reverse
  reverse = not reverse
  return render_template('real_s21.html')

# data saved in file "start_emf.csv"
# display in 3D format
# request "real_s21_3d" in url to get landed
@app.route('/start_emf/<center>/<start>/<stop>')
def start_emf(center, start, stop):
  center_freq = center + 'GHz'
  start_freq = start + 'GHz'
  stop_freq = stop + 'GHz'
  # file for store
  fd_output = open('static/start_emf.csv', 'w+')
  fd_output.write("x,y,z,\n")

  # init Motor
  app_serial = SerialImpl()
  # init VNA
  app_scpi = SCPI("192.168.0.11")
  app_scpi.RST()
  app_scpi.CLS()
  app_scpi.ClearTrace('1')
  app_scpi.CreateMeasureVar('S21', '1')
  app_scpi.CreateTraceAssotiateWithVar('S21', '1')
  app_scpi.SetRange(start_freq, stop_freq, '1')
  app_scpi.CreateMark('1')
  app_scpi.MarkerFormat('1')
  app_scpi.SetMarkFreq('1', center_freq)
  app_scpi.GetMarkerY('1')
  # power on Motor
  dB_list = []
  for i in range(180):
    src = app_scpi.GetMarkerY('1')
    dB_str = src.split(",")[0]
    beishu = dB_str.split("e")[0]
    zhishu = dB_str.split("e")[1]
    dB = float(beishu) * float(10 ** float(zhishu))
    # avoid the wrong data
    if dB > -100.0:
      dB_list.append(dB)
    #angle = float(2 * i / 180.0) * math.pi
    #x = round(math.cos(angle) * dB, 9)
    #y = round(math.sin(angle) * dB, 9)
    #x_str = "{:.9f}".format(x)
    #y_str = "{:.9f}".format(y)
    #z_str = "{:.9f}".format(0.0)
    #fd_output.write(x_str + "," + y_str + "," + z_str + ",\n")
    if reverse:
      app_serial.Write("{CUR20;MCS16;SPD5000;STP4280;ENA;};")
    else:
      app_serial.Write("{CUR20;MCS16;SPD5000;STP-4280;ENA;};")
    time.sleep(1)
  for i in range(len(dB_list)):
    angle = float(2 * i / 180.0) * math.pi
    x = round(math.cos(angle) * (dB_list[i] - 1.5 * min(dB_list)), 9)
    y = round(math.sin(angle) * (dB_list[i] - 1.5 * min(dB_list)), 9)
    x_str = "{:.9f}".format(x)
    y_str = "{:.9f}".format(y)
    z_str = "{:.9f}".format(0.0)
    fd_output.write(x_str + "," + y_str + "," + z_str + ",\n")
    
  # shutdown
  fd_output.close()
  app_serial.Write("OFF;")
  app_scpi.Close()
  global reverse
  reverse = not reverse
  return render_template('start_emf_3d.html')

@app.route('/real_s21')
def real_s21():
  return render_template('real_s21.html')

@app.route('/real_s21_3d')
def real_s21_3d():
  return render_template('start_emf_3d.html')

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about.html')
def about_page():
  return render_template('about.html')

@app.route('/contact_us.html')
def contact_us_page():
  return render_template('contact_us.html')

@app.route('/demo.html')
def demo_page():
  return render_template('demo.html')

@app.route('/faq.html')
def faq_page():
  return render_template('faq.html')

@app.route('/home.html')
def home_page():
  return render_template('home.html')

@app.route('/release.html')
def release_page():
  return render_template('release.html')

@app.route('/motor.html')
def motor_page():
  return render_template('motor.html')

# WebGL demos entrance
@app.route('/nvidia.html')
def nvidia_page():
  return render_template('nvidia.html')

@app.route('/san_angeles.html')
def san_angeles_page():
  return render_template('san_angeles.html')

@app.route('/juliaanim.html')
def juliananim_page():
  return render_template('juliaanim.html')

@app.route('/support_webgl.html')
def support_webgl_page():
  return render_template('support_webgl.html')

@app.route('/spin-cube.html')
def spin_cube_page():
  return render_template('spin-cube.html')

@app.route('/plot-3d.html')
def plot_3d_page():
  return render_template('plot-3d.html')

@app.route('/antenna.html')
def antenna_page():
  return render_template('antenna.html')

@app.route('/wifi_s21.html')
def wifi_page():
  return render_template('wifi_s21.html')

@app.route('/wifi_s21_3d.html')
def wifi_s21_3d_page():
  return render_template('wifi_s21_3d.html')

@app.route('/microstrip.html')
def microstrip_page():
  return render_template('microstrip.html')

@app.route('/microstrip_s11.html')
def microstrip_s11_page():
  return render_template('microstrip_s11.html')

@app.route('/microstrip2_s11.html')
def microstrip2_s11_page():
  return render_template('microstrip2_s11.html')

# for debugging layout template
@app.route('/layout.html')
def layout_page():
  return render_template('layout.html')

''' main entrance of application '''
def main(argv):
  host_ip = '0.0.0.0'
  opt_version = 'version ' + '1.0.0'
  opt_debug = True
  opt_port = 5000

  parser = optparse.OptionParser()
  parser.add_option('--version', action='store_false', dest='version', \
      help='info current version')
  parser.add_option('--debug', action='store', dest='opt_debug', \
      help='enable debug mode of application')
  parser.add_option('--port', action='store', dest='opt_port', type='int', \
      help='enable debug mode of application')
  parser.add_option('--log-path', action='store', dest="opt_log_path", \
      help='write server log to file instead of stderr, \
      increase log level to INFO')
  parser.add_option('--verbose', action='store_false', dest="verbose", \
      help='log verbosely')
  parser.add_option('--silent', action='store_false', dest="silent", \
      help='log nothing')
  parser.add_option('--unittest', action='store_false', dest="silent", \
      help='run unit test cases during launching')

  if 1 > len(argv):
    parser.print_help()

  (opts, _) = parser.parse_args()

  if False == InitLogging(opts):
    print "Unable to initialize logging. Exiting..."
    sys.exit(-1)

  if '--version' in argv:
    VLOG(0, opt_version)
    sys.exit(0)

  if opts.opt_debug:
    if opts.opt_debug.lower() == 'false':
      opt_debug = False
      VLOG(0, "Disable debug mode of application.")
    else:
      VLOG(0, "Enable debug mode of application.")

  if opts.opt_port:
    if opt_port < 65535 and opt_port > 0:
      opt_port = opts.opt_port
    else:
      VLOG(0, "Invalid port selection.")

  # initialize a serial object for application
  try:
    app_serial = SerialImpl()
  except:
    app_serial = None
    VLOG(3, "Failed to initialize serial port for application.")

  status = Status(kOk)

  if '--unittest' in argv:
    app_serial.ForTest()
    app_serial.Defaut()
    app_serial.LoopBackTest()

  # start flask app server
  try:
    VLOG(1, "Start application on port: %s:%d" % (host_ip, opt_port))
    app.run(host=host_ip, port=opt_port, debug=opt_debug)
  except KeyboardInterrupt:
    pass
  except:
    pass
  finally:
    # close serial file
    if app_serial and isinstance(app_serial, SerialImpl):
      app_serial.Close()
    # scan and make the directory tree clean every time 
    for rootdir, subdir, files in os.walk("./"):
      for item in files:
        if item.endswith(".pyc"):
          try:
            os.remove(rootdir + "/" + item)
          except:
            pass

  sys.exit(0)

if __name__ == '__main__':
  main(sys.argv)
