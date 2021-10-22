# -*- coding: utf-8 -*-


"""
parameters.py for SmartTerminal
this is the configuration file for the smart terminal  smart_terminal.py
one instance is created on system startup


"""

import logging
import serial
import sys
import os
import datetime

# ---------  local imports
from running_on import RunningOn
from app_global import AppGlobal

class Parameters( object ):
    """
    manages parameter values for all of Smart Terminal app and its various data logging
    and monitoring applications
    generally available all of the application through AppGlobal.parameters
    !! icons should usually be set at the beginning of each mode if you want the icon to id the mode
    """

    # -------
    def choose_mode( self,  ):
        """
        choose your mode, typically only one line is uncommented, or just pass to stay in default mode
        note addition at end for some testing, keep for that purpose
        use editor find or outline to go to the method
        """
        # ===========  add your  modes as desired starting here ========
        # ---------->> call modes here; I comment out ones I am not using.  Makes it really easy to switch modes
        # these are modes I use, pretty much one for each micro-controller
        # project that I do.  You can look at them as examples or delete the subroutines
        # pick one by un-commenting it.  These are typically synced up with an Arduino app


        pass                              # if everything else is commented out
        #self.quick_start_mode()
        #self.tutorial_example_mode()     # simple setup for documentation and basic terminal
        #self.accel_demo_mode()           #
        #self.controlino_mode()           #

        #self.ddclock_mode()
        #self.ddclock_david()
        #self.ddclock_test_mode()
        #self.ddclock_demo_1()
        #self.ddclock_demo_2()



        self.deer_me_dev()
        #self.deer_me_pi_deploy()

        #self.infra_red_mode()                # not working, requires special modules from irtools
        #self.green_house_mode()
        #self.motor_driver_mode()
        #self.root_cellar_mode()
        #self.stepper_tester_mode()
        #self.serial_cmd_test()               # for messing with master SerialCmd and SerialCmdMaster
        #self.terminal_mode()

        #self.two_axis_mode()
        #self.well_monitor_mode()


        # ---- additional stuff only for testing in addition to another mode
        #self.mode_plus_tests()                # used only for testing change freely

    # -------
    def __init__(self,  ):
        """
        what it says, placed second as the most common mod to parameters is to choose_mode
        """
        self.controller         = AppGlobal.controller
        AppGlobal.parameters    = self

        # next is "mandatory" or you need to make up for any/many missing parameters
        self.default_terminal_mode()               # this is not really a mode that is intended to be used or modified
                                                   # but a default state, call before the "real" mode
                                                   # do not modify unless your really understand
                                                   # but you can run the terminal in this mode

        self.running_on_tweaks()                   # adjustments for different run time environments

        self.choose_mode()

        self.sanity_check_parms(  )                # more of an idea than something of value

        # leave this as last -- do not modify, the global app makes some changes
        AppGlobal.parameter_tweaks()               # including restart
        # and we are done
        # for next move to prog info ??
        # msg   = ( f"{self}" )
        # AppGlobal.logger.log( 55, msg )
        #print( self )   # debug
        return

    # -------
    def running_on_tweaks(self,  ):
        """
        use running on tweaks as a more sophisticated  version of os_tweaks and computer name tweaks,
        """
        computer_id              =   self.running_on.computer_id

        self.os_tweaks()  # general for os, later for more specific

        if computer_id == "smithers":
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"
            self.db_file_name       =  "smithers_db.db"

        elif computer_id == "millhouse":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.win_geometry   = '1300x600+20+20'
            self.db_file_name       =  "millhouse_db.db"

        elif computer_id == "theprof":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            self.db_file_name       =  "the_prof_db.db"

        elif computer_id == "buster1":   # new pi, will become dearme ??
            self.ex_editor          =  r"mousepad"

        elif computer_id == "bulldog":    # may be gone
            self.ex_editor          =  r"gedit"            # ubuntu
            self.db_file_name       =  "bulldog_db.db"

        elif computer_id == "bulldog-mint-russ":
            self.ex_editor          =  r"xed"
            self.db_file_name       =  "bulldog_db.db"

        else:
            print( f"In parameters: no special settings for computer_id {computer_id}" )
            if self.running_on.os_is_win:
                self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            else:
                self.ex_editor          =  r"leafpad"    # linux raspberry pi maybe

    # -------
    def os_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_terminal_mode"
        for a particular operating systems
        you may need/want to mess with this based on your os setup
        """
        if  self.running_on.os_is_win:

            self.port             = "COM5"   #
            self.port_list        =  [ "COM1",  "COM2",  "COM3",  "COM4",  "COM5",  "COM6",  "COM7",  "COM8",  "COM9",  "COM10", ]

        else:  # linux
            print( "linux" )
            self.ex_editor        =  r"leafpad"    # linux editor, most common ones are already included, but this would be your first choice(s)
            self.port             = "/dev/ttyUSB0"
            self.port_list        =  [ "/dev/ttyUSB0",
                                       "/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2",
                                       "/dev/ttyAMC0", "/dev/ttyAMC1",
                                       "/dev/ttyUSB1",
                                       "/dev/AMA0"   ,
                                       ]
            self.icon             = None                 # default gui icon
            self.win_max          = True                 # maximize the window on opening
            self.pylogging_fn      = "smart_terminal_linux.py_log"
            self.bot_spacer_height = 10 # on linux tends to go off screen -- may not show if window not maximized

#    # -------
            # old replaced by running on tweaks
#    def computer_name_tweaks( self ):
#        """
#        this is an subroutine to tweak the default settings of "default_terminal_mode"
#        for particular computers.  Put in settings for you computer if you wish
#        these are for my computers, add what you want ( or nothing ) for your computers
#        """
#        if self.computername == "smithers":
#            self.port               = "COM5"   #
#            self.port               = "COM3"   #
#            self.win_geometry       = '1450x700+20+20'      # width x height + position + position --
#            self.win_max            =  True                 # maximize the window on opening
#            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers
#
#        elif self.computername == "millhouse":
#            self.port               = "COM4"   #
#            self.port               = "COM5"
#            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
#            #self.win_geometry   = '1300x600+20+20'          # width x height position
#            self.pylogging_fn       = "millhouse_smart_terminal.py_log"   # file name for the python logging
#
#        elif self.computername == "theprof":
#            self.port               = "COM4"   #
#            self.port               = "COM5"
#            self.port               = "COM3"
#            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
#            #self.win_geometry   = '1300x600+20+20'          # width x height position
#            self.pylogging_fn       = "theprof_smart_terminal.py_log"   # file name for the python logging

    # -------
    def mode_plus_tests( self ):
        """
        add change some parameters just for testing -- use after a normal mode method is called.
        """
        self.mode               += " + tests"
        self.logging_level      = logging.DEBUG     #INFO

        # self.ex_editor          =  "notepad"
        # self.ex_editor          =  [ "write", "notepad" ]
        # self.ex_editor          =  [ "joe", "notepad" ]

        # self.comm_logging_fn    = "test_comlog.log"

    # ------->> Subroutines:  one for each mode. alpha order - except quick_start_mode
    def quick_start_mode( self, ):
        """
        this mode does not do anything useful except illustrate a simple "mode subroutine"
        new users should probably start here
        the settings in it are the ones your are most likely to use/change from the defaults
        """
        self.mode              = "QuickStart"  # this name will appear in the title of the window
                                                    # to help keep track of which mode you are using

        self.baudrate          = 19200              # changes the baudrate from the default to 19200
        self.port              = "COM9"             # com port

        # the send_ctrls is a list of 3 valued tuples
        # for each item in the list you will have a "send button", a button that will send the contents of
        # the data entry field to the right of it to your comm port.
        # the first item of the tuple is a sting whose test will be on the button
        # the second is a string with the initial or default value for the data entry field
        # the third is a boolean, True make the data entry field editable, otherwise it is protected from edit
        self.send_ctrls = [
                # text                       cmd              can edit
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
        self.id_color          = "red"    # "blue"   "green"  and lots of other work

        # color for some of the background of the gui, not particularly useful imho
        self.bk_color          = "blue"   # color for the background, you can match the id color or use a neutral color like gray
        #self.bk_color          = "gray"


    # -------
    def accel_demo_mode( self, ):
        """
        used in conjunction with my arduino demo of the Accel stepper motor library
        """
        self.mode               = "AccelDemo"

        self.baudrate           = 19200  # 9600  19200 38400, 57600, 115200, 128000 and 256000

        # 4 DOWN
        self.send_ctrls = [
                # text                       cmd         can edit
                ( "Version of Arduino",      "v",        False ),
                ( "Help",                    "?",        False ),
                ( "What Where",              "w",        False ),
                ( "Send",                    "",         True  ),

                ( "Acc Set",                 "a60",      True  ),
                ( "Acc Set",                 "a600 ",    True  ),
                ( "Set Top or Max Speed",    "t5000",    True  ),
                ( "Set Top or Max Speed",    "t50000",   True  ),

                ( "move To Now nn",          "m100",     True  ),
                ( "move To Now nn",          "m0",       True  ),
                ( "move To Now nn",          "m-100",    True  ),
                ( "Zero current pos",        "z",        False ),

                ( "moveToNow nn",            "m500",     True  ),
                ( "moveToNow nn",            "m0",       True  ),
                ( "moveToNow nn",            "m-500",    True  ),
                ( "Zero current pos",        "z",        False ),

                ( "Accel Examples 1-3",      "e1",       True  ),
                ( "Accel Examples 1-3",      "e2",       True   ),
                ( "Accel Examples 1-3",      "e3",       True   ),

                ( "Send",                     "",    True  ),
                ( "Send",                     "",    True  ),
                ( "line1 line1 line2 line2 line3 line3 line4 line4 line5", "",   True ),
                ( "line1 line1 line2 line2 line3 line3", "",   True ),
                ]

        #self.gui_sends         = 15         # number of send frames in the gui beware if 0
        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long,

    # -------
    def controlino_mode( self ):
        """
        used in conjunction with my the controlino -- but really adds nothing to the application
        """
        self.mode              = "Controlino"
        # not really implemented just an idea
        pass

    # -------
    def ddclock_mode( self ):
        """
        used in conjunction with my arduino ddClock stepper motor clock application
        """
        self.mode                       = "ddclock_mode"
        self.baudrate                   = 19200  # 9600

        # ----- various auto start implementation questionable
        self.auto_start                 = None  # for auto-starting something in 2nd thread ?  !! think obsolete see below

        # testing this jan 2018 this function must exist in the helper    auto_run
        # at time of comment this will be run in the helper thread
        #to_eval  = "self.ext_processing." + self.parameters.start_helper_function
        self.start_helper_function    = "auto_run"    # now using eval, may need to do same with args,
        self.start_helper_args        = ( )    # () empty   ( "x", ) one element
        self.start_helper_delay       = 5      # in seconds  must be > 0 to start -- may not work for clock yet
        self.start_helper             = True   #

        # next may be replaced by above or vice versa sure needs clean up
        self.clock_start_mode         = "run"  # "set_hr" , "set_hr", "run", "run_demo",  also need auto connect !! not implemented yet

        self.clock_mode               = "run"     # run_demo   run
        # ---------------- send area:

        self.button_height     = 2        # for the send buttons    -- seem to be roughly the no of lines
        self.button_width      = 10       # for the send buttons    -- 10-20 seems reasonable starts
        self.send_width        = 15       # for the text to be sent -- 10-20 seems reasonable starts

        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of arduino",       "v",                  False ),
                ( "Help",                     "?",                  False ),
                ( "What Where",               "w",                  False ),

                ("nudgeMin",                   "n0 8",       True ), #
                ("nudgeMin",                   "n0 -8",       True ), #

                ("tweakMin",                   "t0 2",       True ), #
                ("tweakMin",                   "t0 -2",       True ), #

                ("chimeMin",                   "c2 0 5",        True ), # case 'q'   motor position speed acc
                ("chimeHr",                    "c1 0 2",       True ), #
#                ("chimeMin",                   "c2 0 30",       True ), #

                ("Send", "", True ),
                ("Send", "", True ),
                ]

        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 3         # the send areas are added in columns this many rows long,

        # ----- processing related:

        self.ext_processing_module      = "ext_process_ddc"
        self.ext_processing_class       = "DDCProcessing"

        # next for probing for a valid port with arduino.
        self.arduino_connect_delay      = 10               # may not be implemented yet
        self.get_arduino_version        = "v"              # # send to the port to get a response from the arduino.
        self.arduino_version            = "DDClock17"      # the response from the arduino should contain this as a substring if the comm port is valid.

        #self.begin_demo_dt              = None    # turns off demo mode -- not so sure
                                                #                            hr:vv  vv:minute     ..........
        self.begin_demo_dt              = datetime.datetime( 2008, 11,    10,   11, 1,     59 ) # should be set to something
        self.time_multiplier            = 10. # only used in demo mode
        #self.time_multiplier            = 100.
        #self.time_multiplier            = 1
        self.chime_type                 = "rotate"    # "random"   "assigned"

        # chime dicts only if assigned  self.chime_type if used you need to define all 12
        # testing 1  2  3 xxxx
        self.hour_chime_dict            = {  1:"2", 2:"3", 3:"2", 4:"2",  5:"2", 6:"3", 7:"2",  8:"3", 9:"2", 10:"3", 11:"2", 12:"2" }

        # testing xxx  4  x   6  7   8 xxx
        self.hour_chime_dict            = {  1:"4", 2:"6", 3:"7", 4:"8",  5:"4", 6:"6", 7:"7",  8:"8", 9:"4", 10:"6", 11:"7", 12:"8" }

        # not assigned default to 0
        self.minute_chime_dict          = {  10:"2", 15:"3", 20:"2", 30:"2",  40:"2", 45:"3", 50:"2",  60:"3", }     # if not assigned default to 0
                                            # above see arduino program to see which is which
        # self.effects_on                 = True    # for the chimes does it work use assigned and assign to 0 0

        self.hour_chime_rotate_amt      = 1
        self.hour_chime_rotate_list     = [ "1", "2", "3", "4", "5", "6", "7", "8" ]

        self.hour_off               = False   # for ddc_processing
        self.minute_off             = False   # for ddc_processing
        self.minute_chime_max       = 1   # !! implement me
        self.hour_chime_max         = 8   # !! implement me   see also _chime_dict

        # next based on 1.1 as ratio
        self.led_chime_values           =         {-20: 1, -19: 1.1, -18: 1.2100000000000002, -17: 1.3310000000000004,
                                                   -16: 1.4641000000000006, -15: 1.6105100000000008, -14: 1.771561000000001,
                                                   -13: 1.9487171000000014, -12: 2.1435888100000016, -11: 2.357947691000002,
                                                   -10: 2.5937424601000023, -9: 2.853116706110003, -8: 3.1384283767210035,
                                                   -7: 3.4522712143931042, -6: 3.797498335832415, -5: 4.177248169415656,
                                                   -4: 4.594972986357222, -3: 5.054470284992944, -2: 5.559917313492239,
                                                   -1: 6.115909044841463, 0: 6.72749994932561, 1: 6.115909044841463, 2: 5.559917313492239,
                                                   3: 5.054470284992944, 4: 4.594972986357222, 5: 4.177248169415656, 6: 3.7974983358324144,
                                                   7: 3.452271214393104, 8: 3.138428376721003, 9: 2.8531167061100025, 10: 2.593742460100002,
                                                   11: 2.3579476910000015, 12: 2.143588810000001, 13: 1.9487171000000008,
                                                   14: 1.7715610000000006, 15: 1.6105100000000003, 16: 1.4641000000000002,
                                                   17: 1.331, 18: 1.21, 19: 1.0999999999999999  }


        day_lb                           = 50
        eve_lb                           = 10
        self.led_background_values       = { 0: 0,       1: 0,       2: 0,       3: 0,       4: 0,        5: 0,
                                             6: day_lb,  7: day_lb,  8:day_lb,   9:day_lb,  10:day_lb,   11: day_lb,
                                             12:day_lb,  13:day_lb,  14:day_lb, 15:day_lb,  16: day_lb,  17: day_lb,
                                             18:eve_lb,  19:eve_lb,  20:eve_lb, 21:eve_lb,  22:eve_lb,   23:eve_lb,
                                             24:eve_lb  }

    # -------
    def ddclock_test_mode( self ):
        """
        debug mode for my arduino ddClock stepper motor clock application
        may not be maintained
        """
        self.mode                     = "ddclock_test_mode"
        self.icon                     = r"./clock_white.ico"

        self.baudrate                 = 19200  # 9600
        self.port                     = "COM4"             # com port

#       -------------------------- auto run on off ---------------------
        # testing this jan 2018 this function must exist in the helper    auto_run
#        self.start_helper_function    = "auto_run"    # now using eval, may need to do same with args,
#        self.start_helper_args        = ( )    # () empty   ( "x", ) one element
#        self.start_helper_delay       = 5      # in seconds  must be > 0 to start -- may not work for clock yet
#        self.start_helper             = True   #

        # next may be replaced by above or vice versa
#        self.clock_start_mode         = "run"  # "set_hr" , "set_hr", "run", "run_demo",  also need auto connect !! not implemented yet

        # ---------------- send area:

        self.button_height     = 3        # for the send buttons    -- seem to be roughly the no of lines
        self.button_width      = 15       # for the send buttons    -- 10-20 seems reasonable starts
        self.send_width        = 15       # for the text to be sent -- 10-20 seems reasonable starts
        # next at end of control list
        #self.max_send_rows     = 3         # the send areas are added in columns this many rows long, then a new
        #self.max_send_rows

        # see backup for some test button sets
        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of arduinoxx",       "v",                  False ),
                ( "Help",                     "?",                  False ),
                ( "What Where",               "w",                  False ),
                ( "Send",                     "",                   True  ),

#                ("nudgeHr n1 x",              "n1 20",     True ), #
#                ("nudgeHr n1 x",              "n1 -20",    True ), #
#                ("nudgeHr n1 x",              "n1 4",      True ), #
#                ("nudgeHr n1 x",              "n1 -4",     True ), #

#                ("quick",                   "q1 12 1000 500",       True ), # case 'q'   motor position speed acc
#                ("quick",                   "q1 3 1000 500",        True ), #
#                ("quick",                   "q1 9 1000 500",        True ), #
#                ("quick",                   "q1 50 1000 200",       True ), #


#                ("nudgeMin",                   "n0 8",       True ), #
                ("nudgeMin",                   "n0 -8",       True ), #

#                ("tweakMin",                   "t0 2",       True ), #
                ("tweakMin",                   "t0 -2",       True ), #

                ("danceMin",                   "d0 50 500 10",         True ), # case 'q'   motor position speed acc
                ("danceMin",                   "d0 1000 500 20",       True ), #

                ("chimeMin",                   "c2 0 5",        True ), # case 'q'   motor position speed acc

                ("danceHr",                   "d1 50 500 100",         True ), # case 'q'   motor position speed acc

                ("chimeHr",                   "c1 0 3",        True ), # case 'q'   motor position speed acc

#
                ("Send", "", True ),
                ("Send", "", True ),
                ]

        #self.send_ctrls        = send_ctrls_test_hr
        #self.send_ctrls        = send_ctrls_test_min

        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 2         # 4 seems good for the pi  the send areas are added in columns this many rows long,

        # ----- processing related:

        self.ext_processing_module      = "ext_process_ddc"
        self.ext_processing_class       = "DDCProcessing"

        self.arduino_connect_delay      = 10     # may not be implemented yet
        self.get_arduino_version        = "v"
        self.arduino_version            = "DDClock17"

        # --------- clock configuration    related
        self.clock_mode                 = "run"     # run_demo   run                                   #                            hr:vv  vv:minute     ..........
        self.begin_demo_dt              = datetime.datetime( 2008, 11,    10,   11, 1,     59 ) # should be set to something
        self.time_multiplier            = 10. # only used in demo mode
        #self.time_multiplier            = 100.
        #self.time_multiplier            = 1
        self.chime_type                 = "random"    # "random"   "assigned"  "rotate"

        # probably extend to 24 hours, or make auto doubler? -- try on 24 then back off to 12 ?
        # need 12                            0    1    3    4    5    6    7    8    9    10   11    12
        self.assigned_hour_chime        = [ "1", "2", "3", "4", "5", "6", "7", "8", "1", "1", "1", "1", "1", "1", ]  # make a dict for consistency ??

        self.hour_chime_dict            = {  1:"2", 2:"3", 3:"2", 4:"2",  5:"2", 6:"3", 7:"2",  8:"3", 9:"2", 10:"3", 11:"2", 12:"2" }    # not assigned default to 0

        self.hour_chime_rotate_amt      = 1
        self.hour_chime_rotate_list     = [ "1", "2", "3", "4", "5", "6", "7", "8" ]

        self.minute_chime_dict          = {  10:"2", 15:"3", 20:"2", 30:"2",  40:"2", 45:"3", 50:"2",  60:"3", }     # if not assigned default to 0

        # ----- led  make helper to give exponential growth, and past in here
        # next based on 1.1 as ratio
        self.led_chime_values           =         {-20: 1, -19: 1.1, -18: 1.2100000000000002, -17: 1.3310000000000004,
                                                   -16: 1.4641000000000006, -15: 1.6105100000000008, -14: 1.771561000000001,
                                                   -13: 1.9487171000000014, -12: 2.1435888100000016, -11: 2.357947691000002,
                                                   -10: 2.5937424601000023, -9: 2.853116706110003, -8: 3.1384283767210035,
                                                   -7: 3.4522712143931042, -6: 3.797498335832415, -5: 4.177248169415656,
                                                   -4: 4.594972986357222, -3: 5.054470284992944, -2: 5.559917313492239,
                                                   -1: 6.115909044841463, 0: 6.72749994932561, 1: 6.115909044841463, 2: 5.559917313492239,
                                                   3: 5.054470284992944, 4: 4.594972986357222, 5: 4.177248169415656, 6: 3.7974983358324144,
                                                   7: 3.452271214393104, 8: 3.138428376721003, 9: 2.8531167061100025, 10: 2.593742460100002,
                                                   11: 2.3579476910000015, 12: 2.143588810000001, 13: 1.9487171000000008,
                                                   14: 1.7715610000000006, 15: 1.6105100000000003, 16: 1.4641000000000002,
                                                   17: 1.331, 18: 1.21, 19: 1.0999999999999999  }

        day_lb                           = 50
        eve_lb                           = 10
        self.led_background_values       = { 0: 0,       1: 0,       2: 0,       3: 0,       4: 0,        5: 0,
                                             6: day_lb,  7: day_lb,  8:day_lb,   9:day_lb,  10:day_lb,   11: day_lb,
                                             12:day_lb,  13:day_lb,  14:day_lb, 15:day_lb,  16: day_lb,  17: day_lb,
                                             18:eve_lb,  19:eve_lb,  20:eve_lb, 21:eve_lb,  22:eve_lb,   23:eve_lb,
                                             24:eve_lb  }

        # self.effects_on                 = True    # for the chimes does it work use assigned and assign to 0 0

        self.hour_off                   = False
        self.minute_off                 = False

    # -------
    def ddclock_david( self ):
        """
        debug mode for my arduino ddClock stepper motor clock application
        may not be maintained
        """
        self.mode                     = "ddclock_david"
        self.icon                     = r"./clock_white.ico"

        self.baudrate                 = 19200  # 9600
        self.port                     = "COM4"             # com port

        self.logging_level            = logging.INFO       #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        self.comm_logging_fn           = None    # None for no logging else file name like "smart_terminal_comm.log"

#       -------------------------- auto run on off ---------------------
        # testing this jan 2018 this function must exist in the helper    auto_run
#        self.start_helper_function    = "auto_run"    # now using eval, may need to do same with args,
#        self.start_helper_args        = ( )    # () empty   ( "x", ) one element
#        self.start_helper_delay       = 5      # in seconds  must be > 0 to start -- may not work for clock yet
#        self.start_helper             = True   #

        # next may be replaced by above or vice versa
#        self.clock_start_mode         = "run"  # "set_hr" , "set_hr", "run", "run_demo",  also need auto connect !! not implemented yet
        self.start_helper_function    = "auto_run"    # now using eval, may need to do same with args,
        self.start_helper_args        = ( )    # () empty   ( "x", ) one element
        self.start_helper_delay       = 5      # in seconds  must be > 0 to start -- may not work for clock yet
        self.start_helper             = True   #
        # ---------------- send area:

        self.button_height     = 3        # for the send buttons    -- seem to be roughly the no of lines
        self.button_width      = 15       # for the send buttons    -- 10-20 seems reasonable starts
        self.send_width        = 15       # for the text to be sent -- 10-20 seems reasonable starts
        # next at end of control list
        #self.max_send_rows     = 3         # the send areas are added in columns this many rows long, then a new
        #self.max_send_rows

        # see backup for some test button sets
        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of arduino",       "v",                  False ),
                ( "Help",                     "?",                  False ),
                ( "What Where",               "w",                  False ),
                ( "Send",                     "",                   True  ),


                ("danceMin",                   "d0 50 500 10",         True ), # case 'q'   motor position speed acc
                ("danceMin",                   "d0 1000 500 20",       True ), #

                ("chimeMin",                   "c2 0 5",        True ), # case 'q'   motor position speed acc

                ("danceHr",                   "d1 50 500 100",         True ), # case 'q'   motor position speed acc

                ("chimeHr",                   "c1 0 3",        True ), # case 'q'   motor position speed acc

#
                ("Send", "", True ),
                ("Send", "", True ),
                ]


        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 2         # 4 seems good for the pi  the send areas are added in columns this many rows long,

        # ----- processing related:

        self.ext_processing_module      = "ext_process_ddc"
        self.ext_processing_class       = "DDCProcessing"

        self.arduino_connect_delay      = 10     # may not be implemented yet
        self.get_arduino_version        = "v"
        self.arduino_version            = "DDClock17"
        self.clock_start_mode           = "run"  # "set_hr" , "set_hr", "run", "run_demo",  also need auto connect !! not implemented yet

        # --------- clock configuration    related
        self.clock_mode                 = "run"     # run_demo   run                                   #                            hr:vv  vv:minute     ..........
        self.begin_demo_dt              = datetime.datetime( 2008, 11,    10,   11, 1,     59 ) # should be set to something
        self.time_multiplier            = 10. # only used in demo mode
        #self.time_multiplier            = 100.
        #self.time_multiplier            = 1
        self.chime_type                 = "rotate"     # "random"    # "random"   "assigned"  "rotate"

        # probably extend to 24 hours, or make auto doubler? -- try on 24 then back off to 12 ?
        # need 12                            0    1    3    4    5    6    7    8    9    10   11    12
        self.assigned_hour_chime        = [ "1", "2", "3", "4", "5", "6", "7", "8", "1", "1", "1", "1", "1", "1", ]  # make a dict for consistency ??

        self.hour_chime_dict            = {  1:"2", 2:"3", 3:"2", 4:"2",  5:"2", 6:"3", 7:"2",  8:"3", 9:"2", 10:"3", 11:"2", 12:"2" }    # not assigned default to 0

        self.hour_chime_rotate_amt      = 1
        self.hour_chime_rotate_list     = [ "1", "2", "3", "4", "5", "6", "7", "8" ]

        self.minute_chime_dict          = {  10:"2", 15:"3", 20:"2", 30:"2",  40:"2", 45:"3", 50:"2",  60:"3", }     # if not assigned default to 0

        # ----- led  make helper to give exponential growth, and past in here

        # next based on 1.1 as ratio
        self.led_chime_values           =         {-20: 1, -19: 1.1, -18: 1.2100000000000002, -17: 1.3310000000000004,
                                                   -16: 1.4641000000000006, -15: 1.6105100000000008, -14: 1.771561000000001,
                                                   -13: 1.9487171000000014, -12: 2.1435888100000016, -11: 2.357947691000002,
                                                   -10: 2.5937424601000023, -9: 2.853116706110003, -8: 3.1384283767210035,
                                                   -7: 3.4522712143931042, -6: 3.797498335832415, -5: 4.177248169415656,
                                                   -4: 4.594972986357222, -3: 5.054470284992944, -2: 5.559917313492239,
                                                   -1: 6.115909044841463, 0: 6.72749994932561, 1: 6.115909044841463, 2: 5.559917313492239,
                                                   3: 5.054470284992944, 4: 4.594972986357222, 5: 4.177248169415656, 6: 3.7974983358324144,
                                                   7: 3.452271214393104, 8: 3.138428376721003, 9: 2.8531167061100025, 10: 2.593742460100002,
                                                   11: 2.3579476910000015, 12: 2.143588810000001, 13: 1.9487171000000008,
                                                   14: 1.7715610000000006, 15: 1.6105100000000003, 16: 1.4641000000000002,
                                                   17: 1.331, 18: 1.21, 19: 1.0999999999999999  }

        day_lb                           = 50
        eve_lb                           = 10
        self.led_background_values       = { 0: 0,       1: 0,       2: 0,       3: 0,       4: 0,        5: 0,
                                             6: day_lb,  7: day_lb,  8:day_lb,   9:day_lb,  10:day_lb,   11: day_lb,
                                             12:day_lb,  13:day_lb,  14:day_lb, 15:day_lb,  16: day_lb,  17: day_lb,
                                             18:eve_lb,  19:eve_lb,  20:eve_lb, 21:eve_lb,  22:eve_lb,   23:eve_lb,
                                             24:eve_lb  }

        # self.effects_on                 = True    # for the chimes does it work use assigned and assign to 0 0

        self.hour_off                   = False
        self.minute_off                 = False

    # --------------------------
    def deer_me_dev( self ):
        """
        to scare away the deer
        this is for development probably on the professor
        """
        self.mode                     = "deer_me_dev"
        self.icon                     = r"./my_dear_icon_2.ico"

        # deer_me counts on this being .1 sec, or else major changes will be required
        self.ht_delta_t               = 100/1000.        # thought this was required timing for deer me but seems not so


        self.logging_level            = logging.DEBUG            #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        self.baudrate                 = 38400  # 9600  38400
        self.port                     = "COM5"             # com port

        self.logging_level            = logging.DEBUG       #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        self.comm_logging_fn           = None    # None for no logging else file name like "smart_terminal_comm.log"

#       -------------------------- auto run on off ---------------------
        self.start_helper_function    = "auto_run"    # now using eval, may need to do same with args,
        self.start_helper_args        = ( )    # () empty   ( "x", ) one element
        self.start_helper_delay       = -5      # in seconds  must be > 0 to start


        # ---------------- send area:
        self.button_height     = 3        # for the send buttons    -- seem to be roughly the no of lines
        self.button_width      = 15       # for the send buttons    -- 10-20 seems reasonable starts
        self.send_width        = 15       # for the text to be sent -- 10-20 seems reasonable starts
        # next at end of control list
        #self.max_send_rows     = 3         # the send areas are added in columns this many rows long, then a new
        #self.max_send_rows

        # see backup for some test button sets
# refresh this list form time to time
#define TIME_ON       0      // this is a time, delta time, for th light to be on
#define ACC_ON        1      // some sort of ( depending on method ) acceleration for the TIME_ON
#define TIME_OFF      2      // analogous to TIME_ON,  but for off
#define ACC_OFF       3      //
#define REPEATS       4      // number of time this cycle can repeat, this may not make sense
#define PIN           5      // pin used by this light
#define STATE         6      // current state
#define NEXT_TIME     7      // next time the state changes

        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of arduino",       "v",                  False ),
                ( "Help",                     "h",                  False ),
                ( "Set Light Index",          "i0",                 False ),
                ( "Set Light Index",          "i1",                 False  ),
                ( "Load Light I",             "l100 200 130 400",   True  ),
                ( "Load Light I",             "l105 200 130 400",   True  ),
                ( "Print Light I",            "p" ,     False  ),
                ( "Strobe",                   "s1" ,    False  ),
                ( "Strobe Not",                "s0" ,   False  ),
                ( "Stop",                     "!xx" ,   False  ),
                ( "Send", "", True ),
                ( "Send", "", True ),
                ]

        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 2         # 4 seems good for the pi  the send areas are added in columns this many rows long,

        # ----- processing related:
        self.ext_processing_module      = "ext_process_dm"
        self.ext_processing_class       = "DMProcessing"

        self.arduino_connect_delay      = 10     # may not be implemented yet
        self.get_arduino_version        = "v"
        self.arduino_version            = "DeerMe"

    # --------------------------
    def deer_me_pi_deploy( self ):
        """
        to scare away the deer
        this is for deployment on the raspberry pi deer_me
        """
        self.mode                     = "deer_me_pi_deploy"
        self.icon                     = r"./my_dear_icon_2.ico"

        # deer_me counts on this being .1 sec, or else major changes will be required
        self.ht_delta_t               = 100/1000.        # thought this was required timing for deer me but seems not so


        self.logging_level            = logging.DEBUG            #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        self.baudrate                 = 38400  # 9600  38400
        self.port                     = "COM5"             # com port

        self.logging_level            = logging.DEBUG       #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        self.comm_logging_fn           = None    # None for no logging else file name like "smart_terminal_comm.log"

#       -------------------------- auto run on off ---------------------
        self.start_helper_function    = "auto_run"    # now using eval, may need to do same with args,
        self.start_helper_args        = ( )    # () empty   ( "x", ) one element
        self.start_helper_delay       = -5      # in seconds  must be > 0 to start


        # ---------------- send area:
        self.button_height     = 3        # for the send buttons    -- seem to be roughly the no of lines
        self.button_width      = 15       # for the send buttons    -- 10-20 seems reasonable starts
        self.send_width        = 15       # for the text to be sent -- 10-20 seems reasonable starts
        # next at end of control list
        #self.max_send_rows     = 3         # the send areas are added in columns this many rows long, then a new
        #self.max_send_rows

        # see backup for some test button sets
# refresh this list form time to time
#define TIME_ON       0      // this is a time, delta time, for th light to be on
#define ACC_ON        1      // some sort of ( depending on method ) acceleration for the TIME_ON
#define TIME_OFF      2      // analogous to TIME_ON,  but for off
#define ACC_OFF       3      //
#define REPEATS       4      // number of time this cycle can repeat, this may not make sense
#define PIN           5      // pin used by this light
#define STATE         6      // current state
#define NEXT_TIME     7      // next time the state changes

        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of arduino",       "v",                  False ),
                ( "Help",                     "h",                  False ),
                ( "Set Light Index",          "i0",                 False ),
                ( "Set Light Index",          "i1",                 False  ),
                ( "Load Light I",             "l100 200 130 400",   True  ),
                ( "Load Light I",             "l105 200 130 400",   True  ),
                ( "Print Light I",            "p" ,     False  ),
                ( "Strobe",                   "s1" ,    False  ),
                ( "Strobe Not",                "s0" ,   False  ),
                ( "Stop",                     "!xx" ,   False  ),
                ( "Send", "", True ),
                ( "Send", "", True ),
                ]

        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 2         # 4 seems good for the pi  the send areas are added in columns this many rows long,

        # ----- processing related:
        self.ext_processing_module      = "ext_process_dm"
        self.ext_processing_class       = "DMProcessing"

        self.arduino_connect_delay      = 10     # may not be implemented yet
        self.get_arduino_version        = "v"
        self.arduino_version            = "DeerMe"


    # -------
    def infra_red_mode( self ):
        """
        not currently runnable, some details need fixing to get from 2.7 to 3.6
        support for my arduino infra red analysis application application
        """
        self.mode                       = "InfraRed"
        self.ext_processing_module      = "ext_process_ir"
        self.ext_processing_class       = "IRProcessing"

    # -------
    def green_house_mode( self ):
        """
        used in conjunction with my arduino green house monitor application
        """
        self.mode                       = "GreenHouse"
        self.icon                       = r"./green_house.ico"       #  greenhouse this has issues on rasPi

        self.baudrate                   = 38400            #
        self.ext_processing_module      = "ext_process_env_monitor"
        self.ext_processing_class       = "ProcessingForEnv"
        self.logging_level              = logging.ERROR           #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0


        if self.running_on.our_os == "win32":
                 self.dbRtoPi188()
                 #self.dbLPi()
        else:
                 self.dbLtoPi191()

        self.send_ctrls = [
                ("Version",          "v",       False ),
                #("Report",           "r", False ),
                ("Help",             "w",       False ),
                ("Aquire",           "a",       False ),
                ("Temp.",            "t",       False ),
                ("Humid.",           "h",       False ),
                ("Light",            "l",       False ),

                ("Send", "", True ),("Send", "", True ),("Send", "", True ),
                #("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),
                ]

        self.gui_sends              = 15                         # number of send frames in the gui beware if 0
        self.gui_sends              = len( self.send_ctrls )     # number of send frames in the gui beware if 0
        self.max_send_rows          = 3         # the send areas are added in columns this many rows long, then a new

        self.arduino_connect_delay  = 10     # may not be implemented yet
        self.get_arduino_version    = "v"
        self.arduino_version        = "GreenHouse"

        # ----- data valid and db update rules -------------------

        self.db_max_delta_time   = 15.         # max time between postings
        self.db_max_delta_time   = 100.        # max time between postings
        self.db_min_delta_time   = 50.         # min time between postings

        self.get_cpu_temp        = True

        self.db_delat_temp       = 2.          # max temperature change between postings
        self.db_delat_temp       = 0.5         # max temperature change between postings

        self.db_temp_len         = 20          # number of value to average -- is this working ??
        # !! more

        self.db_humid_delta      = 2.
        self.db_humid_len        = 16

        self.db_light_len        = 16
        self.db_light_delta      = 2.

        self.db_press_len        = 0              # no pressure measurements

        # for door not clear what meaning these might have look at processing
        self.db_door_len        = 1
        self.db_door_delta      = 1.

        # for pressure will be replaced

        self.run_ave_len         = 6          # length of the pressure running average name seems wrong
        self.db_press_delta      = 2.         # max pressure change between postings

        self.monitor_loop_delay  = 10

   # -------
    def motor_driver_mode( self ):
        """
        used in conjunction with my arduino multiphase motor application
        """
        self.mode                       = "MotorDriver"
        self.ext_processing_module      = "ext_process_motor"
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

    # -------
    def root_cellar_mode( self ):
        """
        used in conjunction with my arduino green house monitor application
        """
        self.green_house_mode( )             # default these then tweak

        self.mode                       = "RootCellar"
        self.ext_processing_module      = "ext_process_env_monitor"
        self.ext_processing_class       = "ProcessingForEnv"
        self.arduino_version            = "RootCellar"

        self.no_temps                   = 3
        self.no_humids                  = 1
        self.no_lights                  = 1
        self.no_doors                   = 4
        self.logging_level              = logging.DEBUG           #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        # copied from dd clock mar 2018 should work
        # at time of comment this will be run in the helper thread
        #to_eval  = "self.ext_processing." + self.parameters.start_helper_function
        self.start_helper_function    = "find_and_monitor_arduino"    # now using eval, may need to do same with args,
        self.start_helper_args        = ( )     # () empty   ( "x", ) one element
        self.start_helper_delay       = 5       # in seconds  must be > 0 to start -- may not work for clock yet
        self.start_helper             = False   # this may be obsolete

        if self.running_on.our_os == "win32":
                 self.dbRtoPi191()   # this probably will not work as system now stands

        else:
                 self.dbLtoPi191()

    # -------
    def serial_cmd_test( self ):
        """
        to test the arduino serial cmd interface
        used in conjunction with my arduino serial command application
        """
        self.mode              = "serial_cmd_test"
        # add icon here

        self.baudrate          = 115200  # 9600 38400 19200 115200
        self.send_ctrls = [
                # button title          send_what     can_edit
                ("Version",                 "v",            False ),
                ("Help",                    "h",            False ),
                ("Report All",              "r",            False ),
                ("Print Alphabet",          "a",            False ),

                ("Convert (not in lib)",    "c22",          True  ),
                ("Echo nn (in lib)",        "e123456",      True  ),
                ("Echo nn (in lib)",        "e    654321",  True  ),
                ("Echo nn (in lib)",        "e -654321",    True  ),


                ("Get Args qn n",           "q5 6   7",       True  ),
                ("Get Args qn n",           "q5 654321 7",    True  ),
                ("Get Args qn n",           "q5 -70 99 -3",   True  ),
                ("Get Args qn n",           "q5 6 7",         True  ),


                ("set Micro Sec nn",        "u22",          True  ),
                ("set Mili Sec nn",         "m 65",         True  ),
                ("Blink nn times",          "b33",          True ),
                ("Pulse N Times",           "p99",          True  ),

                ("XBlink nn",               "x2",           True  ),
                ("Spew",                    "s",            False ),   # self.gt_delta_t  may outrun terminal look at its polling speeds
                ("loop till stopped",       "l",            False ),
                ("Stop",                    "!999",         False ),
                ("Send",                    "",             True ),

                ("Send",                "", True ),
                ("Send",                "", True ),
                ("Send",                "", True ),
                ]
        self.gui_sends         = len( self.send_ctrls )          # number of send frames in the gui beware if 0
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long, then a new
        self.comm_logging_fn    = "serial_cmd_test.comm_log"    # None for no logging else file name like "smart_terminal_comm.log"

    # -------
    def stepper_tester_mode( self ):
        """
        used in conjunction with my arduino stepper motor test application
        """
        self.mode              = "StepperTester"
        self.port              = "COM3"   #
        if  self.os_win:
            pass
            #self.port                   = "COM4"
        else:
            self.port                   = "/dev/ttyUSB0"
            #self.port                   = "/dev/AMA0"     # WITH NOTHING CONNECTED, PROB WRONG
            #self.port              = "/dev/ttyUSB1"
            #self.port              = "/dev/ttyACM2"     # reported by arduino app
            #self.port              = "/dev/ttyACM0"

        # self.baudrate          = 57600  # 9600  19200 38400, 57600, 115200, 128000 and 256000
        self.send_ctrls        = [
                ("Version", "v", False ),
                ("Report", "r", False ),
                ("Where?", "w", False ),
                ("Send", "", True ),
                #("1", "", True ),
                ("2", "", True ),("3", "", True ),
                ("Rotate +",    "d+", False ),
                ("Rotate -",    "d-", False ),
                ("milli sec",   "t1",         True ),
                ("micro sec",   "u500",   True ),
                ("Perm N", "p0", True ),
                ("Next Perm", "n", False ),
                ("Go Steps", "g200", True ),(
                "Send", "", True ),
                ("Send", "", True ),
                ("AccTst nn", "a20", True ),
                ("Exp N", "x0", True ),
                ("Help", "?", False ),
                ("Send", "", True ), ("Send", "", True ),
                ("Send", "", True ),
                ]

        #self.gui_sends         = 15         # number of send frames in the gui beware if 0
        self.gui_sends         = len( self.send_ctrls )          # number of send frames in the gui beware if 0
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long, then a new

    # -------
    def terminal_mode( self ):
        """
        basic terminal mode -- pretty much the still the default
        """
        self.mode              = "Terminal"

        self.port              = "COM5"   #
        self.baudrate          = 19200  # 9600  19200 38400, 57600, 115200, 128000 and 256000

        self.send_ctrls = [
                # text                      cmd               can edit
                ( "Version",                    "v",              True ),
                ( "Help",                    "h",              True ),
                ( "TimeLoop",                "t",       True ),
                ( "More Different",          "yes different", True ),
                ]

    # -------
    def two_axis_mode( self, ):
        """
        for the two axis gimbals arduino application
        see:
            russ-hensel/TwoAxis: A TwoAxis stepper motor controller for the arduino
                https://github.com/russ-hensel/TwoAxis
        """
        self.mode              = "TwoAxis"

        self.baudrate          = 19200  # 9600  19200 38400, 57600, 115200, 128000 and 256000

        self.send_ctrls = [
                # text                      cmd       can edit
                ( "Version of Arduino",      "v",        False ),
                ( "Help",                    "?",        False ),
                ( "What Where",              "w",        False ),
                ( "Send",                    "",         True  ),

                ( "Motor 1=x",               "m1",       True  ),
                ( "Motor 2=y",               "m2",       True  ),
                ( "Acc Set",                 "a500",     True  ),
                ( "Set Top or Max Speed",    "s5000",    True  ),

                ( "Target nn ",                 "t2",    True  ),
                ( "Target nn ",                 "t4",    True  ),
                ( "Save target -nn",            "t-2",   True  ),
                ( "Save target -nn",            "t-4",   True  ),

                ( "Nudge current motor",        "n80",   True  ),
                ( "Nudge current motor",        "n-80",  True  ),
                ( "Nudge current motor",        "n4",    True  ),
                ( "Nudge current motor",        "n-4",   True  ),

                ( "Zero current pos",           "z",     False ),

                ( "What Where",                 "w",     False ),

                ( "Send",                       "",      True  ),
                ( "Send",                       "",      True  ),
               # ( "ex long send message aaa bbbb", "",   True ),
                ]

        self.gui_sends         = len( self.send_ctrls )
        self.max_send_rows     = 4         # the send areas are added in columns this many rows long,

    # -------
    def well_monitor_mode( self ):
        """
        for arduino well monitor, implementation in process
        """
        self.mode               = "WellMonitor"
        # for pressure
        self.no_press           = 1
        self.db_press_len       = 2
        self.db_press_delat     = 2.          # max pressure change between postings

        self.monitor_loop_delay = 10          # time in seconds for the monitoring loop, how often data is aquired

        self.baudrate                   = 38400            #
        self.ext_processing_module      = "ext_process_env_monitor"
        self.ext_processing_class       = "ProcessingForEnv"
        self.logging_level              = logging.ERROR           #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0
        self.logging_level              = logging.DEBUG           #   CRITICAL   50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        if self.running_on.our_os == "win32":
                 self.dbRtoPi188()      # from smithere ... to a remote
                 #self.dbLPi()
                 self.dbLSmithers()     # from smithers to smithers
        else:
                 self.dbLtoPi191()

        self.send_ctrls = [
                ("Version",          "v",       False ),
                #("Report",           "r", False ),
                ("Help",             "h",       False ),
                ("Aquire",           "a",       False ),
                ("Press.",            "p",       False ),
#                ("Humid.",           "h",       False ),
#                ("Light",            "l",       False ),

                ("Send", "", True ),("Send", "", True ),("Send", "", True ),
                #("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),("Send", "", True ),
                ]

        self.gui_sends              = 15                              # number of send frames in the gui beware if 0
        self.gui_sends              = len( self.send_ctrls )          # number of send frames in the gui beware if 0
        self.max_send_rows          = 3         # the send areas are added in columns this many rows long, then a new

       # next for probing for a valid port with arduino.
        self.arduino_connect_delay  = 10     # may not be implemented yet
        self.get_arduino_version    = "v"    # send to the port to get a response from the arduino.
        self.arduino_version        = "WellMonitor"   # the response from the arduino should contain this as a substring if the comm port is valid.

        # ----- data valid and db update rules -------------------

        self.db_max_delta_time   = 15.         # max time between postings
        self.db_max_delta_time   = 100.        # max time between postings
        self.db_min_delta_time   = 50.         # min time between postings

        self.no_press           = 1
        self.db_press_len       = 2
        self.db_press_delta     = 2.          # max pressure change between postings

    # ======================== this defaults settings for all the other modes, runs first =================
    # modify with care
    #   ------------------------------------
    def default_terminal_mode(self, ):
        """
        this sets defaults that are needed to make the system run, many have an advanced
        purpose and may not be documented ( comments here should not be trusted but are a guide )
        here, other example parameter files may document
        them, unless they are obsolete or unimplemented.  Setting unused parameters
        just wastes small amounts of memory, impact is minimal ).
        Some settings mandatory, some pretty much automatic, and generally this subroutine should not be
        messed with unless you think you understand the implications.  Make your changes in some overriding mode
        """
        self.mode              = "Default Terminal"
        self.running_on        = RunningOn   # RunningOn gathers information on the enviroment the application is running on
        self.running_on.gather_data()

        self.icon              = r"terminal_1.ico"    #  icon used by application

        #self.icon              = None                 # no icon at all -- that is os default

        # --------------- consider new ---------------------
        # catch_helper_exceptions       # true to catch helper exceptions, but make it harder to debug see smart_terminal_helper

        self.set_default_path_here      = True    # change the default dir to the one that main.py is in
        self.rethrow_helper_except      = True   # if true re throw log helper exceptions ( better for debugging i think )

        #---------------- begin meta parameters --------------------
        # -----  os platform...  set automatically, do not change -------------

        # self.our_os = sys.platform       #testing if self.our_os == "linux" or self.our_os == "linux2"  "darwin"  "win32"
#        print( "self.our_os is ", self.our_os )

        self.platform       = self.running_on.our_os    # sometimes it matters which os but phase out this name

        # help file for the application
        self.help_file       =  "http://www.opencircuits.com/SmartPlug_Help_File"   # can be url or a local file

        help_file  = r"D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver5\wiki_etc\Python Smart Terminal - OpenCircuits.pdf"
        help_file  = r"wiki_etc\Python Smart Terminal - OpenCircuits.pdf"

        self.help_file       =  help_file

        #---------------- end meta parameters --------------------
        #---------------- database related --------------------
        # extra modules for additional gui and programming of the terminal
        self.ext_processing_module      = None
        self.ext_processing_class       = None

        self.get_cpu_temp               = False   # some applications will fetch the cpu temperature most ignore this
        self.no_temps                   = 0       # temperature values
        self.no_humids                  = 0
        self.no_lights                  = 0
        self.no_doors                   = 0
        self.no_press                   = 0     # pressure values

        self.db_delat_temp              = 2.          # max temperature change between postings
        self.db_delat_temp              = 0.5         # max temperature change between postings

        self.db_temp_len         =       20          # number of value to average -- is this working ??
        # !! more

        self.db_humid_delta             = 2.
        self.db_humid_len               = 16

        self.db_light_len               = 16
        self.db_light_delta             = 2.

        # for door not clear what meaning these might have look at processing
        self.db_door_len                = 1
        self.db_door_delta              = 1.

        # for pressure
        self.db_press_len               = 2
        self.db_press_delta             = 2.          # max pressure change between postings
        #self.auto_start                 = None  # for auto-starting something in 2nd thread ?  no see start helper function
        self.monitor_loop_delay         = 10


        # ----- Begin database setup we do not want one  by default -----------------------
        # this is the name of a database connection
        self.connect           = "none"        # default = "none"- any connection should change this to a connection name

        # ----- logging ------------------
        # id used by the python logger  -- appears inside the logging file
        self.logger_id         = "smart_terminal"

        # file name for the python logging
        self.pylogging_fn      = "smart_terminal.py_log"        # file name for the python logging will be in the terminal directory
        self.comm_logging_fn   = "smart_terminal_comm.log"      # or the name of a file    None    "smart_terminal_comm.log"


        # python logging level of severity for message to be logged
        #self.logging_level     = logging.DEBUG           #   CRITICAL   50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0
        self.logging_level     = logging.INFO           #   CRITICAL  50   ERROR  40 WARNING  30  INFO    20 DEBUG    10 NOTSET   0

        self.print_to_log      = False     # not currently implemented

        # ----- end logging
        self.queue_length      = 30
        self.queue_sleep       = .1   # if queue is full we loop with this as delay in sec smart_terminal.py  post_to_queue is one place to look

        # automatically start the task list
        #self.task_list_on         = False   no longer exists

        # ----- send/receive area  -----------
        self.kivy                 = False    # ?? no support for this or any plans soon

        # number of lines in the receive area before older lines are truncated
        # limits memory used,  0 for unlimited
        self.max_lines            = 1000     # max number of lines in the receive area then lines turncacated

        # determine if the receive auto scrolls or not -- also a check box in the gui
        self.default_scroll       = 1        # 1 auto scroll the receive area, else 0

        # ----------  self.start_helper_function    = gh_processing.GHProcessing.find_and_monitor_arduino
        self.start_helper_function    = "find_and_monitor_arduino"    # now using eval, may need to do same with args,
        self.start_helper_args        = ( )      # () empty   ( "x", ) one element
        self.start_helper_delay       = -99      # in seconds  must be >= 0 to start
        #self.start_helper             = True      #  may drop and just have start_helper_delay

        # open comm port on startup
        self.auto_open         = False     # true to open port on start up  #  !! *todo

        # number of send frames in the gui
        self.gui_sends         = 5         # number of send frames in the gui beware if 0
        self.max_send_rows     = 1         # the send areas are added in columns this many rows long, then a new

        self.show_helper_frame = False     # helper frame not used in basic terminal

        # ------ pre-sets for send areas

        #   could be just string or tuples, this will try tuple   (  label, data_to_send, enable_fg )
        #    ( "Send", "send_me", true )  or mixed, test type on each
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
        self.gt_delta_t        = 50               # polling period in ms --   lowest I have tried is 10 ms, could not see cpu load  gt is gui thread

        self.ht_delta_t        = 100/1000.        # TIME FOR helper thread polling this uses time so in seconds, sorry for confusion

        self.send_array_mod    = 5                # see task, send array ?? very likely not implemented

        # ?? not implemented should it be?
        self.block_port_closed = False            # block sending if port is closed   # *todo  -- or some warning

        # ----- appearance: size, color, ... ------------------------
        # sets the initial overall window size - it is an oddly formatted string

        self.win_geometry      = '1300x600+20+20'      # width x height position
        self.win_max           =  False    # maximize the window on restart -- may only be approximated on linux
        # specify an icon for the application window -- this may be an issue for linux, have some code to skip icon

        # sets a color that you like or so that differently configured
        # smart terminals are easily distinguished
        self.id_color          = "red"    #  "blue"   "green"  and lots of other work
        self.id_height         = 0        # height of id pane, 0 for no pane
        self.bk_color          = "blue"   # color for the background, you can match the id color or use a neutral color like gray
        self.bk_color          = "gray"

        self.bot_spacer_height = 0        # height of spacer pane, 0 for no pane

        self.button_height     = 3        # for the send buttons    -- seem to be roughly the no of lines
        self.button_width      = 10       # for the send buttons    -- 10-20 seems reasonable starts
        self.send_width        = 20       # for the text to be sent -- 10-20 seems reasonable starts

        self.send_bg           = "white"  # white  blue  send text's background color

        self.ex_editor         =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

        #### self.ex_editor          =  r"%windir%\system32\notepad.exe"      # does not work
        #self.ex_editor          =  r"C:\Windows\System32\notepad.exe"

        # ------->> Communications
        # -----  parameters that are relevant for rs232 parameters for arduino

        # 9600 is ok as are many others try this for most reliable? comm
        # The default is 8 data bits, no parity, one stop bit.
        # http://arduino.cc/en/Serial/begin

        # ----- ports and  serial settings -------------------------
        # wrappers for PySerial, leave alone unless more drivers are implemented
        self.comm_mod           = "rs232driver2"
        self.comm_class         = "RS232Driver"

        self.port               = "COM5"   #
        self.port               = "COM3"   #

        #self.baudrate           = 9600                 # baud-rate – Baud rate such as 9600,19200,38400 or 115200 etc.
        #self.baudrate           = 38400
        self.baudrate           = 19200

        self.bytesize           = serial.EIGHTBITS     # Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
        self.parity             = serial.PARITY_NONE
        self.stopbits           = serial.STOPBITS_ONE
        self.recTimeout         = .05                  # serial.timeout in units of x seconds (float allowed)  then what happens exception ?

        # used to probe around for ports

        self.port_list  =  [ "COM1",  "COM2",  "COM3",  "COM4",  "COM5",  "COM6",  "COM7",  "COM8",  "COM9",  "COM10", ]

        self.port_last_probe   = None   # use in port probe for last port that worked

        # parameters of the port not managed by the application
            #timeout – Set a read timeout value.
            #xonxoff – Enable software flow control.
            #rtscts  – Enable hardware (RTS/CTS) flow control.
            #dsrdtr  – Enable hardware (DSR/DTR) flow control.
            #writeTimeout     – Set a write timeout value.
            #interCharTimeout – Inter-character timeout, None to disable (default).

        # ----- Processing Monitor application Values use may depend on mode  ===============

        self.ex_max                 = 20   # max no of exceptions for some reason

        # next are caused by too many or wrong kinds of exceptions.
        self.after_helper_fail      = "do something"
        self.after_polling_fail     = "do something and more parameters "

        # -------------- clock parameters
        self.clock_mode             = "run"     # run_demo   run
        self.hour_off               = False   # for ddc_processing
        self.minute_off             = False   # for ddc_processing
        self.minute_chime_max       = 1   # !! implement me
        self.hour_chime_max         = 8   # !! implement me

        self.time_mode              = "run_demo"    #   "run"  "run_demo"

    # ------->> Subroutines:  db set connection parameter
    #  only for applications using a database
    #
    # ----- db on standard local name, move towards working on all my pi's
    def dbLocal( self, ):
        """
        this is a partial setup for a local connection ( MySQL )
        call as first part of actual full setup where values
        may be modified
        """
        self.db_host             = '127.0.0.1'
        self.db_port             = 3306

        self.db_db               = 'env_data_1'

        self.db_user             = 'env_user'
        self.db_passwd           = 'pi_not_tau'

     # ----- db remote generic, still needs host from a caller
    def dbRemote( self, ):
        """
        remote = db not on currently running host
        for raspberry pi most connections are local
        this is a partial setup for a remote connection
        call as first part of actual full setup where values
        may be modified
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

    # ----- db remote to a Pi
    def dbRtoPi188( self, ):

        self.dbRemote( )
        self.connect             = "RtoPi188"
        self.db_host             = '192.168.0.188'    # 178 even ethernet, 179 odd wifi
        self.db_db               = 'pi_db'

        self.db_user             = 'pi_user'
        self.db_passwd           = 'taunot3point1fourpi'

    # ----- db Local to Pi188
    def dbLtoPi188( self, ):

        self.dbLocal( )
        self.connect             = "LtoPi188"

        self.db_db               = 'pi_db'

        self.db_user             = 'pi_user'
        self.db_passwd           = 'taunot3point1fourpi'

    # ----- db remote to a Pi  189
    def dbRtoPi189( self, ):

        self.dbRemote( )
        self.connect             = "RtoPi189"
        self.db_host             = '192.168.0.189'    # 178 even ethernet, 179 odd wifi
        self.db_db               = 'pi_db'

        self.db_user             = 'pi_user'
        self.db_passwd           = 'taunot3point1fourpi'

    # ----- db remote to a Pi 191 update mar 2018
    def dbRtoPi191( self, ):

        self.db_host             = '192.168.0.191'   #
        self.db_port             = 3306

        self.connect             = "RtoPi191"

        self.db_db               = 'pi_db'

        self.db_user             = 'pi'
        self.db_passwd           = 'KirscheTauEpoint14'

    # ----- db remote to a Pi 191 update mar 2018
    def dbLtoPi191( self, ):
        self.connect             = "LtoPi191"
        self.db_host             = '127.0.0.1'
        self.db_port             = 3306

        self.db_db               = 'pi_db'

        self.db_user             = 'pi'
        self.db_passwd           = 'KirscheTauEpoint14'

    # -----------------
    def sanity_check_parms( self, ):
        """
        look at parameter values and see if they are sane, looks like this will
        be a lot of work with little pay off, continue??
        where to output ??
        what return, what if fail
        for now just output to info -- maybe put in log and put up message -- but we may crash out !
        but the logger may not be running yet -- may need check before and check after
        need to run after the possible extensions so call from back in SmartTermainal ??
        maybe depend on modes so need if sort or statement
        for now may just blow
        """
        all_ok = True

        ok, val, msg = self.get_val(  "self.port" )
        if not ok:
            all_ok = False
            # log msg -- no put in get_val

#        print( ok, val, msg )
#
#        ok, val, msg = self.get_val(  "self.jack" )
#        if not ok:
#            all_ok = False
#            # log msg
#
#        print( ok, val, msg )
#            self.port             = "COM5"   #
#            self.port_list        =  [ "COM1",  "COM2",  "COM3",  "COM4",  "COM5",  "COM6",  "COM7",  "COM8",  "COM9",  "COM10", ]

        if    self.mode == "jack":
            pass

        elif  self.mode in [ "ddclock_test_mode", "ddclock_mode" ] :
            print( "sanity_check " + str( self.clock_mode )  )
            if self.chime_type  == "rotate":
                for i_chime in self.hour_chime_rotate_list:

                       # a string that converts to a number
                       if ( type( i_chime ) ) != type( "a string" ):

#                           print( str( type( i_chime ) ), flush = True )
                           a = 1/0   # force an exception -- reason: bad type
                       ix  = int( i_chime )   # testing conversion

        return all_ok

    # -----------------
    def get_val( self, parm_as_string ):
        """
        may be used as part of sanity check, use a bit unclear
        get value of passed item, swallow any exception but return ( false, None )
        if has value return ( true, value )
        """
        msg        = ""
        is_defined = True
        try:
            ret_val    = eval( parm_as_string )
        except Exception:
            is_defined = False
            ret_val    = None
            msg        = parm_as_string + " is not defined"

        return ( is_defined, ret_val, msg )

    # -----------------------------------
    def __str__( self,   ):
        """
        sometimes it is hard to see where values have come out. This may help if printed.
        not complete, add as needed -- compare across applications
        """
        line_begin  ="\n"
        a_str = ""
        a_str = f"{a_str}\n>>>>>>>>>>* parameters (some) *<<<<<<<<<<<<"
        a_str = f"{a_str}{line_begin}   mode                     {self.mode}"
        #a_str = f"{a_str}\n   snip_file_fn            {self.snip_file_fn}"
        #a_str = f"{a_str}\n   snippets_fn             {self.snippets_fn}"
        a_str = f"{a_str}{line_begin}   ex_editor                {self.ex_editor}"

        a_str = f"{a_str}{line_begin}   --- logging  ---"
        a_str = f"{a_str}{line_begin}   comm_logging_fn          {self.comm_logging_fn}"
        a_str = f"{a_str}{line_begin}   pylogging_fn             {self.pylogging_fn}"
        a_str = f"{a_str}{line_begin}   logger_id                {self.logger_id}"
        a_str = f"{a_str}{line_begin}   logging_level            {self.logging_level}"

        a_str = f"{a_str}{line_begin}   --- appearance ---"
        a_str = f"{a_str}{line_begin}   icon                     {self.icon}"
        a_str = f"{a_str}{line_begin}   win_geometry             {self.win_geometry}"
        a_str = f"{a_str}{line_begin}   win_max                  {self.win_max}"

        a_str = f"{a_str}{line_begin}   default_scroll           {self.default_scroll}"

        a_str = f"{a_str}{line_begin}   send_ctrls               {self.send_ctrls}"
        a_str = f"{a_str}{line_begin}   gui_sends                {self.gui_sends}"
        a_str = f"{a_str}{line_begin}   max_send_rows            {self.max_send_rows}"
        a_str = f"{a_str}{line_begin}   show_helper_frame        {self.show_helper_frame}"
        a_str = f"{a_str}{line_begin}   id_color                 {self.id_color}"
        a_str = f"{a_str}{line_begin}   id_height                {self.id_height}"
        a_str = f"{a_str}{line_begin}   bk_color                 {self.bk_color}"
        a_str = f"{a_str}{line_begin}   bot_spacer_height        {self.bot_spacer_height}"
        a_str = f"{a_str}{line_begin}   button_height            {self.button_height}"
        a_str = f"{a_str}{line_begin}   button_width             {self.button_width}"
        a_str = f"{a_str}{line_begin}   send_bg                  {self.send_bg}"


        # a_str = f"{a_str}\n   --- running on ---"
        # a_str = f"{a_str}\n   computername             {self.computername}"
        # a_str = f"{a_str}\n   our_os                   {self.our_os}"

        # a_str = f"{a_str}{line_begin}   --- misc ---"




        a_str = f"{a_str}{line_begin}   start_helper_function    {self.start_helper_function}"

        a_str = f"{a_str}{line_begin}   start_helper_delay       {self.start_helper_delay}"

        a_str = f"{a_str}{line_begin}   --- terminal comm ---"
        a_str = f"{a_str}{line_begin}   ext_processing_module    {self.ext_processing_module}"
        a_str = f"{a_str}{line_begin}   ext_processing_class     {self.ext_processing_class}"
        a_str = f"{a_str}{line_begin}   prefix_send              {self.prefix_send}"
        a_str = f"{a_str}{line_begin}   prefix_rec               {self.prefix_rec}"
        a_str = f"{a_str}{line_begin}   prefix_info              {self.prefix_info}"

        a_str = f"{a_str}{line_begin}   comm_class               {self.comm_class}"
        a_str = f"{a_str}{line_begin}   comm_mod                 {self.comm_mod}"
        a_str = f"{a_str}{line_begin}   port                     {self.port}"
        a_str = f"{a_str}{line_begin}   baudrate                 {self.baudrate}"
        a_str = f"{a_str}{line_begin}   bytesize                 {self.bytesize}"
        a_str = f"{a_str}{line_begin}   parity                   {self.parity}"
        a_str = f"{a_str}{line_begin}   stopbits                 {self.stopbits}"
        a_str = f"{a_str}{line_begin}   recTimeout               {self.recTimeout}"
        a_str = f"{a_str}{line_begin}   port_list                {self.port_list}"


        a_str = f"{a_str}{line_begin}   help_file                {self.help_file}"
        a_str = f"{a_str}{line_begin}   connect                  {self.connect}"

        a_str = f"{a_str}{line_begin}   echoSend                 {self.echoSend}"
        a_str = f"{a_str}{line_begin}   gt_delta_t               {self.gt_delta_t}"
        a_str = f"{a_str}{line_begin}   ht_delta_t               {self.ht_delta_t}"



        a_str = f"{a_str}{line_begin}   --- data ---"
        a_str = f"{a_str}{line_begin}   get_cpu_temp             {self.get_cpu_temp}"

        # a_str = f"{a_str}{line_begin}   stopbits                 {self.stopbits}"
        # a_str = f"{a_str}{line_begin}   prefix_send              {self.prefix_send}"



        a_str = f"{a_str}\n   and so much more.... \n\n"
        return a_str

"""


"""

# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    main app: smart_terminal.SmartTerminal(  )
    """
#    x
    print( "" )
    print( " ========== starting SmartTerminal from parameters.py ==============" )
    import smart_terminal

    # just one of:
    a_app = smart_terminal.SmartTerminal(  )
    # or
    # try:
    #     a_app = smart_terminal.SmartTerminal(  )

    # except Exception as exception:
    #     msg   = "exception in __main__ run the app -- it will end"
    #     a_app.logger.critical( msg )
    #     a_app.logger.critical( exception,  stack_info=True )   # just where I am full trace back most info
    #     raise

    # finally:
    #     print( "here we are done with smart terminal " )
    #     sys.stdout.flush()

# =================== eof ==============================










