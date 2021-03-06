# Copy from https://github.com/egrcc/zhihu-python/blob/master/auth.py
import termcolor

class Logging:
  flag = True

  @staticmethod
  def error(msg):
    if Logging.flag == True:
      print "".join(  [ termcolor.colored("ERROR", "red"), ": ", termcolor.colored(msg, "white") ] )
  @staticmethod
  def warn(msg):
    if Logging.flag == True:
      print "".join(  [ termcolor.colored("WARN", "yellow"), ": ", termcolor.colored(msg, "white") ] )
  @staticmethod
  def info(msg):
    # attrs=['reverse', 'blink']
    if Logging.flag == True:
      print "".join(  [ termcolor.colored("INFO", "magenta"), ": ", termcolor.colored(msg, "white") ] )
  @staticmethod
  def debug(msg):
    if Logging.flag == True:
      print "".join(  [ termcolor.colored("DEBUG", "magenta"), ": ", termcolor.colored(msg, "white") ] )
  @staticmethod
  def success(msg):
    if Logging.flag == True:
      print "".join(  [ termcolor.colored("SUCCESS", "green"), ": ", termcolor.colored(msg, "white") ] )