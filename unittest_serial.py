from driver.serial_impl import SerialImpl
from utility.log import InitLogging
from utility.log import VLOG
import optparse
import time
import sys

def Init():
  ser = SerialImpl()
  ser.LoopBackTest()
  ser.Close()

def ContinueSend3(ser, seconds):
  timeout = time.time() + seconds
  while time.time() < timeout:
    time.sleep(0.04)
    ser.Write('3')

def Start(ser):
  ser.Write("{CUR20;MCS16;SPD5000;ENA;};")

def Abort(ser):
  ser.Write("OFF;")

if __name__ == "__main__":
  parser = optparse.OptionParser()
  parser.add_option('--version', action='store_false', dest='version', help='info current version')
  parser.add_option('--debug', action='store', dest='opt_debug', help='enable debug mode of application')
  parser.add_option('--port', action='store', dest='opt_port', type='int', help='enable debug mode of application')
  parser.add_option('--log-path', action='store', dest="opt_log_path", help='write server log to file instead of stderr, increase log level to INFO')
  parser.add_option('--verbose', action='store_false', dest="verbose", help='log verbosely')
  parser.add_option('--silent', action='store_false', dest="silent", help='log nothing')
  parser.add_option('--unittest', action='store_false', dest="silent", help='run unit test cases during launching')
  (opts, _) = parser.parse_args()
  # log system
  InitLogging(opts)
  # init serial
  ser = SerialImpl()
  # ContinueSend3(ser, 10)
  st = time.time()
  ast = time.asctime()
  Start(ser)
  quit = False
  while not quit:
    try:
      pass
    except KeyboardInterrupt:
      Abort(ser)
      quit = True
      et = time.time()
      aet = time.asctime()
  ser.Close()
