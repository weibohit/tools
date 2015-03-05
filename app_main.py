from flask import Flask
from flask import g
from flask import render_template
from flask import request
import optparse
import os
import sys
import time
from driver.serial_impl import SerialImpl
from utility.log import InitLogging
from utility.log import VLOG
from utility.server_info import ServerInfo
from utility.status import *

app = Flask(__name__)

@app.before_request
def server_info_init():
  g.server_info = ServerInfo.Create()

@app.route('/')
def home_page():
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

# WebGL demos entrance
@app.route('/spin-cube.html')
def spin_cube_page():
  return render_template('spin-cube.html')

# for debugging layout template
@app.route('/layout.html')
def layout_page():
  return render_template('layout.html')

''' main entrance of application '''
def main(argv):
  opt_version = 'version ' + '0.0.9'
  opt_debug = True
  opt_port = '5000'

  parser = optparse.OptionParser()
  parser.add_option('--version', action='store_false', dest='version', help='info current version')
  parser.add_option('--debug', action='store', dest='opt_debug', help='enable debug mode of application')
  parser.add_option('--port', action='store', dest='opt_port', type='int', help='enable debug mode of application')
  parser.add_option('--log-path', action='store', dest="opt_log_path", help='write server log to file instead of stderr, increase log level to INFO')
  parser.add_option('--verbose', action='store_false', dest="verbose", help='log verbosely')
  parser.add_option('--silent', action='store_false', dest="silent", help='log nothing')
  parser.add_option('--unittest', action='store_false', dest="silent", help='run unit test cases during launching')

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
    # sys.exit(-1)

  status = Status(kOk)

  if '--unittest' in argv:
    app_serial.ForTest()
    app_serial.Defaut()
    app_serial.LoopBackTest()

  # start flask app server
  try:
    VLOG(1, "Start application on port: http://127.0.0.1:" + opt_port)
    app.run(debug=opt_debug)
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
