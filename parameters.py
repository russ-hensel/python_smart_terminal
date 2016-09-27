# -*- coding: utf-8 -*-

# parameters    for SmartTerminal

# lots of values commeted out for future/past use

import logging
import serial
import sys

class Parameters( object ):
    """
    manages parameter values for all of Smart Terminal app and its various data logging
    and monitoring applications
    should be generally available to much of the application through the Controllers instance variable
    """
    def __init__(self,  controller  ):

#          #print "parameters.py in WellMonitorTerminal"
#          #sys.stdout.flush()

          self.controller        = controller    # save a link to the controller

# ----------- meta parms, set other parms ===========
# these parameters are used to set other parameters as a convience, if this is not convienuent for you just
# set your parmeters at the end of the init or us a second parameter file.

# ----------- mode, os.... ---------------
          # mode might be called application it changes the function of the
          # app, mostly in the "auto" mode, it primarly effects the auto task list
          # and perhaps the database connection

          # for now just case statements inc in this
          self.mode              = "GreenHouse"  # add sensor processing and monitoring for greenhouse sensors
          self.mode              = "Terminal"    # no special processing, just a terminal
                                                 # later implement WellMonitor...... RootCellar

          # mode is important so check !! change to dict
          if   self.mode == "Terminal":
                print "parameter says Terminal"

          elif self.mode == "GreenHouse":
                print "parameter says GreenHouse"

          elif self.mode == "RootCellar":
                print "parameter says RootCellar"
                print "now using greenhouse mode"
          else:
                print "error ?? parameter says " + self.mode

          # ---------  os platform... ----------------

          our_os = sys.platform
          print "our_os is ", our_os

          #if our_os == "linux" or our_os == "linux2"  "darwin":

          if our_os == "win32":
               self.os_win = True     # right now windows and everything else
          else:
               self.os_win = False

          self.platform   = our_os    # sometimes it matters which os

          #  example use as if self.controller.parameters.os_win:

          # ------------------------------------

          #self.connect     = "SmithersToSmithers"
          #self.connect     = "SmithersToPi"
          #self.connect     = "PiToPi"
          #self.connect     = "manual"
          #self.connect     = "no"

          # feel free to add more, except for self.connect = no, only used in parameter files.
          if self.mode != "Terminal":
              if our_os == "win32":
                  self.connect      = "SmithersToSmithers"  # meta name used later
                  #self.connect     = "SmithersToPi"
              else:
                   self.connect     = "PiToPi"

              self.platform   = our_os
          else:
               self.connect   = "no"  # do not use a database  "manual" is another legal meta value

          # --------- end os platform... ----------------

#---------------- end meta parameters --------------------

          # this is the name of a program: its excutable with path inof.
          # to be used in opening an exteranl editor
          self.ex_editor   =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10

          # thought I could find a way to start the db engine
          # not easy on windows with mySql
          # self.start_db    =  !!

          # -----------------------------------

          # this is only partly implemented, leave both to true for now
          # function of this not relly clear, keep True
          self.have_terminal     = True      # an idea that is not well thought out

          # test frame is the frame where the start auto stop auto .... buttons appear
          # set to false to delete from GUI
          self.have_test_frame   = True      # new phase in test frame at top of window
          self.have_test_fg      = True      # old phase out test frame at top of window

          # obsolete keep False so the unexpected does not happen
          self.have_iar          = False       # ?? todo or remove

          # automatically start the task list
          self.task_list_on      = False        # automatically start the task list

# --------------------- logging ------------------
          # id used by the python logger
          self.logger_id         = "smart_terminal"

          # file name for the python logging
          self.pylogging_fn      = "smart_terminal.py_log"   # file name for the python logging

          # python logging level of severity for message to be logged
          self.logging_level     = logging.DEBUG           #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0
          #self.logging_level     = logging.INFO            #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0

# ----------- graph ignore, all soon moved to another app -----------

          self.graph_min         = 0.
          self.graph_max         = 100.

# ------------------send/recieve ---------------------
# ----------- recieve area -----------

          self.max_lines         = 1000     # max number of lines in the recieve area
                                            # befor older lines are truncated
                                            # limits memory used  0 for unlimited
          self.default_scroll    = 1        # 1 auto scroll the recieve area, else 0

          # open comm port on startup
          self.auto_open         = True       # true to open port on start up  #  !! *todo

          # number of send frames in the gui
          self.gui_sends         = 15          # number of send frames in the gui beware if 0
          self.max_send_rows     = 5           # the send areas are added in columns this many rows long, then a new
                                               # column is started

          # these are strings inserted into the send frames, one in each frame
          self.send_strs         = [ "v", "z5", "t", "p", "a1 2 3 44 55 666 777", "x"    ]
          self.send_strs         = [ "v", "a", "t", "h", "l", "x", "", "", "", "", "", "", "", ""    ]
          self.send_strs         = [ "r", "p0", "n", "g400", "d-", "d+", "t2", "t8", "t16", "", "a5", "a10", "a20", ""    ]

          # wrapers for PySerial, leave alone unless more drivers are implemented
          self.comm_mod     = "rs232driver2"
          self.comm_class   = "RS232Driver"

          # locally echo the sent characters to the recieve area
          self.echoSend          = True          # locally echo the sent characters

          # this is put on the end of the sent material
          self.serialAppend      = "\r\n"        # "\r\n" is car. return line feed.
          self.serialAppend      = ""
          self.serialAppend      = "\r"

          # probably being phased out or not but do not use
          self.loop_period       = 100              # multiples of self.poll_delta_t
          self.loop_text         = "looping TEXT"   # do not make so long as to jam the transmitter sent every poll_delta_t

          # This is how often in ms to poll the comm port, faster makes it more responsive, uses
          # more resources
          self.poll_delta_t      = 100              # in ms --   lowest I have tried is 10 ms, could not see cpu load

          self.send_array_mod    = 5                # see task, send array

          # ?? not implemented should it be?
          self.block_port_closed = False            # block sending if port is closed   # *todo  -- or some warning

          # used in a "version" task to help identify the arduino
          # the arduino is susposed to respond to a version request with a string
          # containing this, they are part of the name of an Arduino applicatin
          self.arduino_string    = "WellMonitor"   # see       task_version_rec( self, rec_data )
          self.arduino_string    = "PiRemote"
          self.arduino_string    = "GreenHouse Monitor"
          self.arduino_string    = "RootCellar"
          self.arduino_string    = "GreenHouse"
         #self.arduino_string    = "DeerAnti"
          # ------------------------------------------

# -------------------- appearance ------------------------
          # sets the initial overall window size - it is an oddly formatted string
          # self.win.geometry('1500x800+40+80')
          self.win_geometry      = '1500x800+20+20'    # width x height position

          # sets a color that you like or so that differently configured
          # smart terminal are easily distinguished
          self.id_color          = "red"    #
          #self.id_color          = "blue"

          #  this may be an issue for linux, have some code to skip icon there, need to find out more
          self.icon              = r"D:\Temp\ico_from_windows\terminal_red.ico"    #  blue red green yellow
          self.icon              = r".smaller.ico"    #  this format is ng
          self.icon              = r"D:\Russ\0000\SpyderP\SmartTerminal\smaller.ico"    #  greenhouse will rename
          self.icon              = r"smaller.ico"    #  greenhouse will rename  == this has issues on rasPi
          self.icon              = r"./smaller.ico"    #  greenhouse will rename  == this has issues on rasPi

# ----------- db .... ---------------

          # for now just case statements inc in this
          #self.use_db              = "No" # "No" "Yes" or "name of connection"  !! not really implemented

             # ----------------------- db from smithers to smithers  local ----------------------

          if      self.connect     == "SmithersToSmithers":
                            self.dbFromSmithersToSmithers( )
                            print "dbFromSmithersToSmithers( )"
          elif    self.connect     == "SmithersToPi":
                            self.dbFromSmithersToPi()
                            print "dbFromSmithersToPi()"
          elif    self.connect     == "PiToPi":
                            self.dbFromPiToPi()
          elif    self.connect     == "manual":
                # put parms here
                print "manual connect parms"
                pass

          elif    self.connect     == "no":
                # do not use a db
                pass
          else:
              print "we have a connect config error in parmameters"

# ------------------------- Monitor application Values ===============
# ------------------------- data valid and db update rules -------------------

          self.db_max_delta_time   = 15.         # max time between postings
          self.db_max_delta_time   = 600.         # max time between postings
          self.db_min_delta_time   = 50.          # min time between postings

          self.db_delat_temp       = 2.          # max temperature change between postings
          self.db_delat_temp       = 0.5          # max temperature change between postings

          self.db_temp_len         = 20           # in seconds ??
          # !! more

          self.db_humid_delta      = 2.
          self.db_humid_len        = 16

          self.db_light_len        = 16
          self.db_light_delta      = 2.

          # for door not clear what meaning these might have look at processing
          self.db_door_len        = 1
          self.db_door_delta      = 1.

          # for pressure will be replaced

          self.run_ave_len         = 6          # length of the pressure running average
          self.db_delat_pressure   = 2.          # max pressure change between postings

# ------------------- ports -------------------------

          if self.os_win:
                self.port              = "COM6"   #
                self.port              = "COM15"   # /dev/ttyUSB0 on GNU/Linux or COM3 on Windows. Device name or port number number or None.
                self.port              = "COM4"   #
          else:
                # not sure for ras pi
                self.port              = "/dev/ttyUSB0"
                #self.port              = "/dev/ttyUSB1"
                self.port              = "/dev/ttyACM2"     # reported by arduino app
                self.port              = "/dev/ttyACM0"     # reported by arduino app  0 or o    0 is what works dummy


          #self.baudrate          = 9600                 # baudrate – Baud rate such as 9600 or 115200 etc.
          self.baudrate          = 19200
          #self.baudrate          = 38400

          self.bytesize          = serial.EIGHTBITS     # Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
          self.parity            = serial.PARITY_NONE
          self.stopbits          = serial.STOPBITS_ONE
          self.recTimeout        = .05           # serial.timeout in units of x seconds (float allowed)

          self.portList          =  [ "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", ]

          # parameters I am not managing
          #timeout – Set a read timeout value.
          #xonxoff – Enable software flow control.
          #rtscts – Enable hardware (RTS/CTS) flow control.
          #dsrdtr – Enable hardware (DSR/DTR) flow control.
          #writeTimeout – Set a write timeout value.
          #interCharTimeout – Inter-character timeout, None to disable (default).

          # ----------  parameters that are relavant for rs232 parms for arduino


          # 9600 is ok as are many others try this for most reliable? comm
          #The default is 8 data bits, no parity, one stop bit.
          #http://arduino.cc/en/Serial/begin

# ------  utility values, use in utility functions below

          self.parityToStrs      = {  serial.PARITY_EVEN : "Parity Even",
                                      serial.PARITY_NONE : "Parity None",
                                      serial.PARITY_ODD  : "Parity Odd",
                                      serial.PARITY_MARK : "Parity Mark",
                                      serial.PARITY_SPACE: "Parity Space"
                                      }
          # ------

          self.stopbitsToStrs    = { serial.STOPBITS_ONE            : "1",
                                     serial.STOPBITS_ONE_POINT_FIVE : "1.5",
                                     serial.STOPBITS_TWO            : "2",
                                     }

          # ------

          #print "Parameters initialized"

          # too soon to use logger, not configured yet
          # self.controller.logger.info( "parameters.Parameters initialized" )
          return

# -----------------db connection parameter subroutines
    #these will surely not apply to your setup
    #!! fix names ----------------------------------

    def dbFromSmithersToSmithers( self, ):
          """
          db from smithers to smithers  local db
          """

          self.db_host             = '127.0.0.1'
          self.db_port             = 3306
          self.db_db               = 'well_monitor_1'
          self.db_user             = 'root'
          self.db_passwd           = 'FreeData99'


    # ----------------------- db on pi remote ----------------------
    def dbFromSmithersToPi( self, ):

    # not working sept 10 2016
          self.db_host             = '192.168.0.175'
          self.db_port             = 3306

          self.db_db               = 'well_db_2'
          self.db_db               = 'well_db'
          self.db_db               = 'WELL_DB'

          self.db_user             = 'wm_user'
          self.db_passwd           = 'wm_secret_pass_99'


    # ----------------------- db on pi from pi  ----------------------
    def dbFromPiToPi( self, ):


          self.db_host             = '127.0.0.1'
          self.db_port             = 3306

          self.db_db               = 'WELL_DB'

          self.db_user             = 'wm_user'
          self.db_passwd           = 'wm_secret_pass_99'

# -------- utility functions, mostly get parameters as strings

    def getCommTypeAsStr( self, ):   # should get from driver and branch to right kind of parms

           return "RS232"

    # ---------------------
    def getParityAsStr( self, ):

           return self.parityToStrs[ self.parity ]

    # ---------------------
    def getBaudrateAsStr( self, ):

           return str( self.baudrate )

    # ---------------------
    def getPortAsStr( self, ):

           return self.port

    def getStopbitsAsStr( self, ):

           return self.stopbitsToStrs[ self.stopbits ]

    # -----------------------------
    # probably should just get the variable, more pythonic?

    def getBaud( self, ):
          return self.baudrate

# ==============================================
if __name__ == '__main__':
        """
        run the app associated with the parameters
        """

        import smart_terminal
        a_app = smart_terminal.SmartTerminal(  )

# =================== eof ==============================

