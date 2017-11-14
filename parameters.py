# -*- coding: utf-8 -*-

# parameters    for SmartTerminal   May be russ's big monster


# History/status  ( !! = to do ** = done)
#    !! db names and connect names still need some clean up
#

import logging
import serial
import sys
import os


# local
from app_global import AppGlobal

class Parameters( object ):
    """
    manages parameter values for all of Smart Terminal app and its various data logging
    and monitoring applications
    generally available to most of the application through the Controllers instance variable
    """
    def __init__(self,  ):
        """
        """
        self.controller         = AppGlobal.controller
        AppGlobal.parameters    = self

        # next is mandatory
        self.default_terminal_mode()               # this is not really a mode that is intended to be used or modified
                                                   # but a default state, call before the "real" mode
                                                   # do not modify unless your really understand
                                                   # but you can run the termial in this mode

        self.os_tweaks( )                          # adjustments for different operating systems

        self.computer_name_tweaks(  )              # adjustments for computers by name
        
        
        # --------- add your mods as desired starting here ---------
        
        # self.port               = "COM5"           #
        # self.baudrate           = 19200            # Standard baud rates include 110, 300, 600, 1200, 2400, 
                                                   #    4800, 9600, 14400, 19200, 38400, 57600, 115200, 128000 and 256000

        
        

# ---------->> call modes here; I comment out ones I am not using.  Makes it really easy to switch modes

        # these are modes I use, pretty much one for each microcontroller
        # project that I do.  You can look at them as examples or delte the subroutines
        # pick one by uncommenting it.

        #self.tutorial_example_mode()
        #self.accel_demo_mode()
        #self.controlino_mode()
        #self.ddclock_17_test_mode()
        #self.ddclock_17_auto_mode()
        #self.ddclock_mode()
        #self.infra_red_mode()
        #self.green_house_mode()
        #self.motor_driver_mode()
        #self.stepper_tester_mode()
        #self.serial_cmd_test()
        #self.terminal_mode()
        self.two_axis_mode()
        #self.well_monitor_mode()

        return

    # -------
    def os_tweaks( self ):
        """
        this is an sufroutine to tweak the default settings of "default_terminal_mode"
        for particular operating systems
        you may need to mess with this based on your os setup 
        """
        if  self.os_win:
            self.icon              = r"./green_house.ico"    #  greenhouse this has issues on rasPi
            #self.icon              = None                   #  default gui icon

        else:
            pass

    # -------
    def computer_name_tweaks( self ):
        """
        this is an sufroutine to tweak the default settings of "default_terminal_mode"
        for particular computers.  Put in settings for you computer if you wish
        these are for my computers, add what you want ( or nothing ) for your computes
        """

        if self.computername == "smithers":
            self.port               = "COM5"   #
            #self.port              = "COM3"   #
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

        elif self.computername == "millhouse":
            pass
            self.port               = "COM3"   #
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
            #self.win_geometry   = '1300x600+20+20'          # width x height position
            self.pylogging_fn       = "millhouse_smart_terminal.py_log"   # file name for the python logging


    # ------->> Subroutines:  one for each mode alpha order - except tutorial

    def tutorial_example_mode( self, ):
        """
        this mode does not do anything usefull except illustrate a simple "mode subroutine"
        """
        self.mode              = "TutorialExample"  # this name will appear in the title of the window
                                                    # to help keep track of which mode you are using

        self.baudrate          = 19200              # changes the baucrate from the default to 19200

        # the send_ctrls is a list of 3 valued tuples
        # for each item in the list you will have a "send button", a button that will send the contents of
        # the data entry field to the right of it to your comm port.
        # the first item of the tuple is a sting whose test will be on the button
        # the second is a string with the initial or default value for the data entry field
        # the third is a boolean, True make the data entry field editable, otherwise it is protected from edit
        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Send",                    "",              True ),
                ( "Send",                    "",              True ),
                ( "Different Title",         "default",       True ),
                ( "More Different",          "yes different", True ),
                ]
        # you may get extra buttons with default values to fill the space


        # you have an option for a pane below the title bar of some size and color, if the height is set
        # to zero you do not get this pane
        # useful if you have 2 instances of the program running and want an easy way to tell them apart
        self.id_height         = 5        # height of id pane, 0 for no pane
        self.id_color          = "red"    #  "blue"   "green"  and lots of other work

        # color for some of the background of the gui, not particurlarly useful imho
        self.bk_color          = "blue"   # color for the background, you can match the id color or use a neutral color like gray
        #self.bk_color          = "gray"

    # -------
    def accel_demo_mode( self, ):

        self.mode              = "AccelDemo"

        self.baudrate          = 19200  # 9600  19200 38400, 57600, 115200, 128000 and 256000 

        # 4 DOWN
        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of Arduino",      "v",     False ),
                ( "Help",                    "?",     False ),
                ( "What Where",              "w",     False ),
                ( "Send",                    "",      True  ),

                ( "Acc Set",                 "a500",     True  ),
                ( "Set Top or Max Speed",    "t5000",    True  ),
                ( "Acc Set",                 "a5000",    True  ),
                ( "Set Top or Max Speed",    "t50000",   True  ),
                
                
                ( "moveToNow nn",            "m100",  True  ),
                ( "moveToNow nn",            "m0",    True  ),
                ( "moveToNow nn",            "m-100", True  ),
                ( "Zero current pos",        "z",     False ),
                
                ( "moveToNow nn",            "m500",  True  ),
                ( "moveToNow nn",            "m0",    True  ),
                ( "moveToNow nn",            "m-500", True  ),
                ( "Zero current pos",        "z",     False ),
                
                ( "Accel Ex 1-3",            "e1",    True  ),
                ( "moveToNow nn",            "m77",   True  ),
                ( "moveToNow nn",            "m -88",   True  ),

                ( "Run",                    "r",     False ),
                #( "Set Speed",              "s2000",   True  ),
                #( "Stop",                   "s",     False ),
             
                ( "What Where",              "w",    False  ),
                ( "Zero current pos",        "z",    False  ),

                ( "Help",                     "?",   False ),
                ( "Send",                     "",    True  ),
                ( "Send",                     "",    True  ),
                ( "ex long send message aaa bbbb", "",   True ),
                ]

        #self.gui_sends         = 15         # number of send frames in the gui beware if 0
        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long,

    # -------
    def controlino_mode( self ):
        self.mode              = "Controlino"
        pass

   # -------
    def ddclock_17_test_mode( self, ):

        self.mode              = "DDClock17"

        self.baudrate          = 19200  # 9600
        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of arduino",     "v",      False ),
                ( "Help",                   "?",      False ),
                ( "What Where",             "w",      False ),
                ( "Send",                   "",       True  ),

                ("set mode Hr",             "m1",     False ), # "mnn   setHrMinMode"
                ("set mode Min",            "m0",     False ), # "mnn   setHrMinMode"

                ("set top Speed nn",        "s100000", True ),  # case 's':   setMaxSpeedHr   setMaxSpeedMin
                ("set Acc nn",              "a5000",    True ),  # case 'a'    setAccHr        setAccMin

                 
                ("go to Time nn",           "t12",     True ), # case 't'    goToHr     goToMin
                ("go to Time nn",           "t3",     True ), # case 't'    goToHr     goToMin
                ("go to Time nn",           "t6",     True ), # case 't'    goToHr     goToMin
                ("go to Time nn",           "t9",     True ), # case 't'    goToHr     goToMin

                ("nudge nn",                "n8",     True ), # case 't'    
                ("nudge nn",                "n-4",    True ), # case 't'    
                ("zero pos",                "z",      True ), # case 'z'   
                
                
                ("do Dance nn",             "d0",     True ), # case 'd'    doHrDance  doDanceMin

                ("Send",                    "",       True ),


                #("Report",                  "r",       False ),

               # ("Move", "mnn", True ),

                #("milli sec", "tn", True ),("micro sec", "un", True ),
                #("Perm N", "p0", True ),("Next Perm", "n", False ),
                #("Go Steps", "g200", True ),("Send", "", True ),
#                ("Send", "", True ),
#                ("AccSet nn", "a20", True ),
                ("Send", "", True ),
                ("Send", "", True ),
                ("Send", "", True ),
                ("Send", "", True ),
                ]

        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long,

    # -------
    def ddclock_17_auto_mode( self, ):

        self.mode                       = "DDClock17Auto"

        self.ext_processing_module      = "ddc_processingy"
        self.ext_processing_class       = "DDCProcessing"

        self.arduino_connect_delay      = 10     # may not be implemented yet
        self.get_arduino_version        = "v"
        self.arduino_version            = "DDClock17"

        self.baudrate                   = 19200  # 9600
        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of arduino",     "v",      False ),
                ( "Help",                   "?",      False ),
                ( "What Where",             "w",      False ),
                ( "Send",                   "",       True  ),

                ("set mode Hr",             "m1",     False ), # "mnn   setHrMinMode"
                ("set mode Min",            "m0",     False ), # "mnn   setHrMinMode"

                ("set top Speed nn",        "s10000", True  ),  # case 's':   setMaxSpeedHr   setMaxSpeedMin
                ("set Acc nn",              "a50",    True  ),  # case 'a'    setAccHr        setAccMin

                ("Nudge nn",                "n-3",    True  ),  # case 'n':   adjHr      adjMin
                ("go to Time nn",           "t3",     True  ),  # case 't'    goToHr     goToMin

                ("do Dance nn",             "d0",     True  ), # case 'd'    doHrDance  doDanceMin

                ("Send",                    "",       True  ),

                ("Send", "", True ),
                ("Send", "", True ),
                ("Send", "", True ),
                ("Send", "", True ),
                ]

        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long,

    # -------
    def infra_red_mode( self ):
        self.mode                       = "InfraRed"

        self.ext_processing_module      = "ir_processing"
        self.ext_processing_class       = "IRProcessing"

    # -------
    def green_house_mode( self ):
        self.mode                       = "GreenHouse"

        self.ext_processing_module      = "gh_processing"
        self.ext_processing_class       = "GHProcessing"

        if self.our_os == "win32":
                 self.dbLPi()
#                self.connect      = "SmithersToSmithers"  # meta name used later
#                self.connect      = "none"           # do not even try to connect
#                self.connect      = "Pi176"         # local to pi 176 same for pi178
#                self.connect      = "RtoPi178"      # remote to  pi178
#                self.connect      = "LSmithers"     # LSmithers
        else:
                 self.dbLPi()
#                self.connect      = "LPi"

        self.send_ctrls = [
                ("Version", "v", False ),
                ("Report", "r", False ),
                ("Help", "w", False ),
                ("Aquire", "a", False ),
                ("Temp.", "t", False ),
                ("Humid.", "h", False ),("Send", "", True ),("Send", "u10", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),
                ("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),
                ("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),
                ]
        # number of send frames in the gui

        self.gui_sends         = 15         # number of send frames in the gui beware if 0
        self.gui_sends         = len( self.send_ctrls )          # number of send frames in the gui beware if 0
        self.max_send_rows     = 3         # the send areas are added in columns this many rows long, then a new

        self.arduino_connect_delay  = 10     # may not be implemented yet
        self.get_arduino_version    = "v"
        self.arduino_version        = "GreenHouse Monitor"


    # -------
    def serial_cmd_test( self ):
        """
        this is a stub fill it out
        """
        self.mode              = "serial_cmd_test"
        self.baudrate          = 38400  # 9600 38400 19200
        self.send_ctrls = [
                # button title          send_what     can_edit
                ("Version",             "v",            False ),
                ("Help",                "h",            False ),
                ("Print Alphabet",      "a",            False ),
                ("Blink nn times",       "b33",          True ),
                ("Convert (not in lib)","c22",          True  ),
                ("Echo nn (in lib)",       "e123456",          True  ),
                ("Echo  nn (in lib)",       "e 654321",         True  ),
                ("set Mili Sec nn",     "m 65",         True  ),
                ("Pulse N Times",       "p99",          True  ),
                ("Get Args qn n",       "q5 6 7",       True  ),
                ("Report All",          "r",            False ),
                ("set Micro Se nn",       "u22",          True  ),

                ("XBlink nn",           "x2",           True  ),

                ("Send",                "", True ),
                ("Send",                "", True ),
                ("Send",                "", True ),
                ]

    # -------
    def stepper_tester_mode( self ):

        self.mode              = "StepperTester"
        self.baudrate          = 57600  # 9600  19200 38400, 57600, 115200, 128000 and 256000 
        self.send_ctrls        = [
                ("Version", "v", False ), ("Report", "r", False ), ("Where?", "w", False ), ("Send", "", True ),
                #("1", "", True ),("2", "", True ),("3", "", True ),
                ("Rotate +", "d+", False ),("Rotate -", "d-", False ),
                ("milli sec", "tn", True ),("micro sec", "un", True ),
                ("Perm N", "p0", True ),("Next Perm", "n", False ),
                ("Go Steps", "g200", True ),("Send", "", True ),
                ("Send", "", True ), ("AccTst nn", "a20", True ), ("Exp N", "x0", True ),
                ("Help", "?", False ),
                ("Send", "", True ), ("Send", "", True ),
                ("Send", "", True ),
                ]

        #self.gui_sends         = 15         # number of send frames in the gui beware if 0
        self.gui_sends         = len( self.send_ctrls )          # number of send frames in the gui beware if 0
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long, then a new

    # -------
    def two_axis_mode( self, ):

        self.mode              = "TwoAxis"

        self.baudrate          = 19200  # 9600  19200 38400, 57600, 115200, 128000 and 256000 

        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of Arduino",      "v",     False ),
                ( "Help",                    "?",     False ),
                ( "What Where",              "w",     False ),
                ( "Send",                    "",      True  ),

                
                ( "Motor 1=x",            "m1",   True  ),
                ( "Motor 2=y",            "m2",   True  ),
                ( "Acc Set",                 "a500",     True  ),
                ( "Set Top or Max Speed",    "s5000",    True  ),
            
                ( "Target nn ",                 "t2",     True  ),
                ( "Target nn ",                 "t4",     True  ),
                ( "Save target -nn",            "t-2",    True  ),                
                ( "Save target -nn",            "t-4",    True  ),    
                
                
#                ( "moveToNow nn",            "m100",  True  ),
#                ( "moveToNow nn",            "m0",    True  ),
#                ( "moveToNow nn",            "m-100", True  ),
                #( "Zero current pos",        "z",     False ),
                

                
                #( "Accel Ex 1-3",            "e1",    True  ),
                # ( "Motor x",            "m1",   True  ),
                # ( "Motor y",            "m2",   True  ),
                
                 #( "Accel Ex 1-3",            "e1",    True  ),
                ( "Nudge current motor",            "n80",    True  ),
                ( "Nudge current motor",            "n-80",    True  ),
                ( "Nudge current motor",            "n4",      True  ),
                ( "Nudge current motor",            "n-4",   True  ),
                #( "Motor y",            "m2",   True  ),               
                
                ( "Zero current pos",        "z",    False  ),
                # ( "Run",                    "r",     False ),
                #( "Set Speed",              "s2000",   True  ),
                #( "Stop",                   "s",     False ),
             
                ( "What Where",              "w",    False  ),
          
                ( "Dance current xy",                     "d2",    True  ),
                ( "Send",                     "",    True  ),
                ( "Send",                    "",      True  ),
               # ( "ex long send message aaa bbbb", "",   True ),
                ]

        #self.gui_sends         = 15         # number of send frames in the gui beware if 0
        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long,


    # -------
    def well_monitor_mode( self ):
        self.mode              = "WellMonitor"
        pass

    # -------
    def ddclock_mode( self ):
        self.mode              = "DDClock"
        self.gui_sends         = 5         # number of send frames in the gui beware if 0  may be updated below
        self.max_send_rows     = 3         # the send areas are added in columns this many rows long, then a new
        self.send_ctrls        = [ ( "GetVersion", "v",   True ),     ( "SetSpeed",     "s1000", True ),  ( "SetAcc", "a100",  True ),
                                   ( "SetPower On",  "p1",  False ),  ( "SetPower Off", "p0", False ),
                                   ( "MoveTo", "m200", True ),        ( "Stop Motor", "o", False ),       ( "Report", "r", False ),
                                   ( "Help", "?", False ),                                 ]
        self.gui_sends         = len( self.send_ctrls ) +  5

    # -------
    def terminal_mode( self ):
        self.mode                       = "Terminal"

    # -------
    def motor_driver_mode( self ):
        self.mode                       = "MotorDriver"
        self.ext_processing_module      = "motor_processing"
        self.ext_processing_class       = "MotorProcessing"

        self.send_ctrls = [
                                  "v", "z",   "g200", "n",
                                  ( "Forward", "d+",  False ),
                                  ( "Back",    "d-",  False ),
                                     "l",   "r",  "h",
                                     "p0",  "n",  "g40",
                                     "m5",  "u5", "w50", "w150",
                                     "r"
                                     ]

        self.gui_sends         = len( self.send_ctrls )


    #   ------------------------------------
    def default_terminal_mode(self, ):
        """
        this sets defaults that are needed to make the system run, many have an advanced
        purpose and will not be documented ( comments here should not be trusted )
        here, other example parameter files document
        them, unless they are obsolete or unimplemented.  Setting unused parameters
        just wastes small amounts of memory, impact is minimal
        some mandatory, some pretty much automatic, and generally should not be
        messed with
        """
        self.mode                       = "Default Terminal"

         # -----  os platform...  set automatically, do not change -------------
        self.our_os = sys.platform       #testing if self.our_os == "linux" or self.our_os == "linux2"  "darwin"  "win32"
        #print( "self.our_os is ", self.our_os )

        if self.our_os == "win32":
            self.os_win = True     # right now windows and everything like it
        else:
            self.os_win = False

        self.platform       = self.our_os    # sometimes it matters which os

        self.computername   = ( str( os.getenv( "COMPUTERNAME" ) ) ).lower()

        self.ext_processing_module      = None
        self.ext_processing_class       = None

        # ----- Begin database setup we do not want one  -----------------------
        # this is the name of a database connection
        self.connect     = "none"        # default = "none"- any connection shoudl change this to a connection name

        # ----- logging ------------------
        # id used by the python logger  -- appears inside the logging file
        self.logger_id         = "smart_terminal"

        # file name for the python logging
        self.pylogging_fn      = "smart_terminal.py_log"   # file name for the python logging

        # python logging level of severity for message to be logged
        self.logging_level     = logging.DEBUG           #   CRITICAL   50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0
        #self.logging_level     = logging.INFO           #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        self.print_to_log      = False
        # ----- send/recieve/recieve area and presets  -----------

        #---------------- end meta parameters --------------------
        self.queue_length         = 20
        self.queue_sleep          = .1

        # automatically start the task list
        #self.task_list_on         = False   no longer exists

        # ----- send/recieve/recieve area and presets  -----------
        self.kivy                 = False
        self.max_lines            = 1000     # max number of lines in the recieve area
        # number of lines in the recieve area before older lines are truncated
        # limits memory used  0 for unlimited

        # determine if the receive auto scrolls or not -- also a check box in the gui
        self.default_scroll    = 1        # 1 auto scroll the recieve area, else 0

        #import  gh_processing
        # ----------  self.start_helper_function    = gh_processing.GHProcessing.find_and_monitor_arduino
        self.start_helper_function    = "find_and_monitor_arduino"    # now using eval, may need to do same with args,
        self.start_helper_args        = ( )     # () empty   ( "x", ) one element
        self.start_helper_delay       = 0      # in seconds  must be > 0 to start

        # open comm port on startup
        self.auto_open         = False       # true to open port on start up  #  !! *todo

        # number of send frames in the gui
        self.gui_sends         = 5         # number of send frames in the gui beware if 0
        self.max_send_rows     = 1         # the send areas are added in columns this many rows long, then a new

        self.show_helper_frame = False      # helper frame not used in basic terminal

        # ------ pre-sets for send areas

        #   could be just string or tuples, this will try tuple   (  label, data_to_send, enable_fg )  ( "Send", "send_me", true )  or mixed, test type on each
        #  "\n"    for a 2 line label on the button

        self.send_ctrls        = [ ( "Send", "send_me", True ), ( "Send it", "send_me", True ) , ( "Send it3", "send_medata ", True ) ]

        # these control how data is displayed in the receive area ( which also shows data send and other information )
        self.prefix_send       = "# >>> "    # prefix for data sent
        self.prefix_rec        = "# <<< "    # prefix for data received
        self.prefix_info       = "# !!! "    # prefix for informational messages

        self.echoSend          = True        # locally echo the sent characters

        # this is put on the end of the sent material
        self.serialAppend      = "\r\n"        # "\r\n" is car. return line feed.
        self.serialAppend      = ""
        self.serialAppend      = "\r"

        # This is how often in ms to poll the comm port, faster makes it more responsive, uses
        # more resources
        self.gt_delta_t        = 50               # in ms --   lowest I have tried is 10 ms, could not see cpu load

        self.ht_delta_t        = 100/1000.        # TIME FOR helper thread polling this uses time so in seconds, sorry for confusion

        self.send_array_mod    = 5                # see task, send array

        # ?? not implemented should it be?
        self.block_port_closed = False            # block sending if port is closed   # *todo  -- or some warning

        # ----- appearance: size, color, icon.... ------------------------
        # sets the initial overall window size - it is an oddly formatted string

        self.win_geometry   = '1300x600+20+20'      # width x height position

        # sets a color that you like or so that differently configured
        # smart terminals are easily distinguished
        self.id_color          = "red"    #  "blue"   "green"  and lots of other work
        self.id_height         = 0       # height of id pane, 0 for no pane
        self.bk_color          = "blue"   # color for the background, you can match the id color or use a neutral color like gray
        self.bk_color          = "gray"

        # specify an icon for the application window
        #  this may be an issue for linux, have some code to skip icon there, need to find out more
        self.icon              = r"D:\Temp\ico_from_windows\terminal_red.ico"    #  blue red green yellow
        self.icon              = r".smaller.ico"    #  this format is ng
        self.icon              = r"D:\Russ\0000\SpyderP\SmartTerminal\smaller.ico"    #  greenhouse will rename
        self.icon              = r"smaller.ico"    #  greenhouse will rename  == this has issues on rasPi
        self.icon              = r"./smaller.ico"    #  greenhouse will rename  == this has issues on rasPi
        self.icon              = None


        self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

        #### self.ex_editor          =  r"%windir%\system32\notepad.exe"      # does not work
        #self.ex_editor          =  r"C:\Windows\System32\notepad.exe"

        # ------->> Communications
        # -----  parameters that are relavant for rs232 parms for arduino

        # 9600 is ok as are many others try this for most reliable? comm
        # The default is 8 data bits, no parity, one stop bit.
        # http://arduino.cc/en/Serial/begin
        # ----- ports and  serial settings -------------------------
        # wrappers for PySerial, leave alone unless more drivers are implemented
        self.comm_mod           = "rs232driver2"
        self.comm_class         = "RS232Driver"

        self.port               = "COM5"   #
        self.port               = "COM3"   #

        self.baudrate           = 9600                 # baudrate – Baud rate such as 9600,19200,38400 or 115200 etc.
        #self.baudrate           = 38400

        self.bytesize           = serial.EIGHTBITS     # Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
        self.parity             = serial.PARITY_NONE
        self.stopbits           = serial.STOPBITS_ONE
        self.recTimeout         = .05           # serial.timeout in units of x seconds (float allowed)  then what happens exception ?

        # used to probe around for ports

        self.port_list  =  [ "COM1",  "COM2",  "COM3",  "COM4",  "COM5",  "COM6",  "COM7",  "COM8",  "COM9",  "COM10", ]

        self.port_last_probe   = None   # use in port probe for last port that worked

        # parameters not managed
            #timeout – Set a read timeout value.
            #xonxoff – Enable software flow control.
            #rtscts – Enable hardware (RTS/CTS) flow control.
            #dsrdtr – Enable hardware (DSR/DTR) flow control.
            #writeTimeout – Set a write timeout value.
            #interCharTimeout – Inter-character timeout, None to disable (default).
        # ----- Processing Monitor application Values use may depend on mode  ===============

        self.ex_max              = 5   # max no of exceptions for some reason
        # ----- data valid and db update rules -------------------
        # this should be someone else

        self.db_max_delta_time   = 15.         # max time between postings
        self.db_max_delta_time   = 100.         # max time between postings
        self.db_min_delta_time   = 50.          # min time between postings

        self.db_delat_temp       = 2.          # max temperature change between postings
        self.db_delat_temp       = 0.5          # max temperature change between postings

        self.db_temp_len         = 20           # number of value to average -- is this working ??
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

        # ----- Processing Monitor application Values use may depend on mode  ===============

        self.ex_max              = 20   # max no of exceptions for some reason

        # next are caused by too many or wrong kinds of exceptions.
        self.after_helper_fail     = "do something"
        self.after_polling_fail    = "do something and more parameters "


    # ------->> Subroutines:  db set connection parameter
    #  these will probably not apply to your setup
    #
    # ----- db remote generic, still needs host from a caller
    def dbRemote( self, ):
        """
        standard parameters for remote connection, but
        will not set host which needs to be set in caller
        return: set of instance variables
        """
        self.db_host             = '192.168.0.0'   # no pi of mine
        self.db_host             = 'host not set'  # no pi of mine
        self.db_port             = 3306

        self.db_db               = 'env_data_1'

        self.db_user             = 'env_user'
        self.db_passwd           = 'pi_not_tau'

    # ----- db on standard local name, move towards workin on all my pi's
    def dbLocal( self, ):

        self.db_host             = '127.0.0.1'
        self.db_port             = 3306

        self.db_db               = 'env_data_1'

        self.db_user             = 'env_user'
        self.db_passwd           = 'pi_not_tau'

    # ----- db local on Smithers, smithers is a bit non standard
    def dbLSmithers( self, ):  #for local, name of machine, when dbLocal will not do
        """
        db from smithers to smithers  local db
        """
        self.connect             = "LSmithers"
        self.db_host             = '127.0.0.1'
        self.db_port             = 3306

        self.db_db               = 'well_monitor_1'

        self.db_user             = 'root'
        self.db_passwd           = 'FreeData99'

    # ----- db on .....  for local, name of machine, when dbLocal will not do
    def dbLPi( self, ):
        self.connect             = "LPi"
        self.db_host             = '127.0.0.1'
        self.db_port             = 3306

        self.db_db               = 'env_data_1'

        self.db_user             = 'env_user'
        self.db_passwd           = 'pi_not_tau'

    # ----- db remote to a Pi
    def dbRtoPi176( self, ):
        self.dbRemote( )
        self.connect             = "RtoPi176"
        self.db_host             = '192.168.0.176'

    # ----- db remote to a Pi
    def dbRtoPi178( self, ):

        self.dbRemote( )
        self.connect             = "RtoPi178"
        self.db_host             = '192.168.0.178'    # 178 even ethernet, 179 odd wifi



# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
#    x
    print( "" )
    print( " ========== starting SmartTerminal from parameters.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )

# =================== eof ==============================










