# -*- coding: utf-8 -*-


"""
ext_process_ddc.pu
extended processing for ddclock: this does the actions for the ddclock

"""

import logging
import datetime
import abc_def
import tkinter as Tk
import random
import time

# -------------- local libs ------------------
from    app_global import AppGlobal

import  smart_terminal

# ================= Class =======================
#
class ChimeAndTime(   ):
    """
    stores chime and time info for ddclock processing

    """
    # ------------------------------------------
    def __init__( self,    ):

        # self.time_mode                  = AppGlobal.clock_mode   #  "run"    # "run_demo"    demo .... get from parameters  AppGlobal.parameters.   ....
        self.led_chime_values           = AppGlobal.parameters.led_chime_values
        self.led_background_values      = AppGlobal.parameters.led_background_values
        self.chime_enabled              = True    # not implemented !!


        self.init_time()


#        # current_ what we just computed last_ the last sent to the clock
#        self.last_datetime      = None     # if none causes time to be initialized
#
#        self.last_hour          = None     # last hour set
#        self.current_hour       = None
#
#        self.current_hour_24    = None     # used for background led
#
#        self.last_minute        = None     # last minute set
#        self.current_minute     = None
#
#        #self.current_led_chime  = None     # if chime is in effect the minute ( which may be in future ) for the chime
#        self.last_led_minute    = None
#        self.current_led_minute = None     # if a led chime this is set to a minute value else none  -- may not need this
#
#        self.last_led_tick      = None
#        self.current_led_tick   = 0        # ticks are the units ( now 10 sec ) at which the led brightness may be changed
#                                           # have a function for this


        # hand speed and acceleration -- could move to parms
        self.std_acc_minute     = 100
        self.std_speed_minute   = 100

        self.std_acc_hour       = 100
        self.std_speed_hour     = 100

        # move this setup to parms, and a day, night and sleep background level
        # let this start a minute in advance  -- really need to do sequential ints, this centers on self.led_current_tick
#        self.led_pwm_dict       = { -6: "0",  -5: "20", -4: "40", -3: "80", -2: "160", -1: "220", -0: "220",
#                                     1: "220", 2: "160", 3: "80",  4: "40",  6: "20",   6: "0",    7: "0",}

        self.set_wait_time      = .10        # what units what mean  --- for arduino response
    # ------------------------------------------
    def init_time( self,    ):
        """
        init all times, used at init, and used to restart clock so we get all chimes 
        think need to to last and current 
        """
        self.last_datetime      = None     # if none causes time to be initialized

        self.last_hour          = None     # last hour set
        self.current_hour       = None

        self.current_hour_24    = None     # used for backgrount led

        self.last_minute        = None     # last minute set
        self.current_minute     = None

        #self.current_led_chime  = None     # if chime is in effect the minute ( which may be in future ) for the chime
        self.last_led_minute    = None
        self.current_led_minute = None     # if a led chime this is set to a minute value else none  -- may not need this

        self.last_led_tick      = None
        self.current_led_tick   = 0        # ticks are the units ( now 10 sec ) at which the led brightness may be changed
                                           # have a function for this
        self.hour_rotate_index  = 0        # for hour_rotating_chime 
        
    # ------------------------------------------
    def last_eq_none( self,    ):
        """
        set last values to None so all chimes will kick in
        """
        # current_ what we just computed last_ the last sent to the clock
        self.last_datetime      = None     #
        self.last_hour          = None     # last hour set
        self.last_minute        = None     # last minute set
        self.last_led_minute    = None
        self.last_led_tick      = None

    # ------------------------------------------
    def compute_now( self,    ):
        """
        now is current time to be used by the clock, may be in demo mode so
        that this is a function rather than inline code
        this should be the only place to get the time
        returns a datetime
        """
        real_now                = datetime.datetime.now()
        if  AppGlobal.clock_mode == "run_demo":
            begin_demo_dt       = AppGlobal.parameters.begin_demo_dt
            ret                 = ( begin_demo_dt  +
                                  ( ( real_now - begin_demo_dt ) * AppGlobal.parameters.time_multiplier ) )
        else:  # run"
            ret  = real_now
        return ret

    # ------------------------------------------
    def polling( self,    ):

        now      = self.compute_now()

        self.current_hour_24    = now.hour                        # what are the valid hours 0 <= hour < 24,datetime.hour  In range(24) does not include 24                                                                     
        self.current_hour       = self.current_hour_24

        # normalize for 12 hr clock -- but include 12 not 0 for midnight ... this is I think the consistent decision but may need to be  revisited 
        if   self.current_hour == 0:
             self.current_hour  = 12
             
        elif self.current_hour > 12:
            self.current_hour   -= 12

        self.current_minute     = now.minute

        # we will chime 60 then chime the hour, then chime 0
        # next code assumes led chimes at 15, 30, 45, 60, 0

        if   self.current_minute >= 10 and self.current_minute <= 20:
            self.current_led_minute   = 15
        elif self.current_minute >= 25 and self.current_minute <= 35:
            self.current_led_minute   = 30
        elif self.current_minute >= 40 and self.current_minute <= 50:
            self.current_led_minute   = 45
        elif self.current_minute >= 55 and self.current_minute <= 60:
            self.current_led_minute   = 60
        elif self.current_minute >= 0  and self.current_minute <= 5:
            self.current_led_minute   = 0
        else:
            self.current_led_minute   = None

        if self.current_led_minute is not None:
#            print( self.current_led_minute, flush = True )
            # optmize this later

            # self.current_led_tick   is translated to a value in conjunction with self.current_led_minute

            if self.current_led_minute == 60:
                current_led_dt        = now.replace(  minute = 59,  second = 59, microsecond = 999999 ) # as near as I can get, could have a fixed derlt time to add

            else:
                current_led_dt        = now.replace(  minute = self.current_led_minute,  second = 0, microsecond = 0 ) # does not work for minute 60

            delta                       = now - current_led_dt
            delta                       = delta.total_seconds()
            self.current_led_tick       = int( delta/20 )      # devisor set period between update ( seconds )

        else:
            current_led_dt              = None
            delta                       = None
            self.led_seconds            = None
            self.current_led_tick       = None   # this means use the background level also used to see if update is needed.

        # debug
#        print( "\n --------------------")
#        print( f"now {now}" )
#        print( f"self.current_minute {self.current_minute}" )
#        print( f"self.current_led_minute {self.current_led_minute}" )
##        print( f"self.current_led_dt {self.current_led_dt}" )
##        print( f"delta {delta}" )
#        print( f"self.current_led_tick {self.current_led_tick}" )
##        print( f"delta_led {delta_led}" )
##        print( f"led_seconds {led_seconds}" )

        self.hour_chime( )

    # -------------------------------------------------
    def hour_chime( self,  ):  #
        """
        calls a cascade of chimes, led, minute, hour
        if hr change, then chime both minute and hour and adjust clock hands to current time

        may be called before its time
        we are only called if a minute has gone by so lets find out which minute use
        this started as doing the dances from the pi but first implement on the arduino and call dance no.
        Args:  self.  ....  a_hour, the hour to chime ( as a int ?? )
        """
        if self.last_hour == self.current_hour:
            # no hr chime but perhaps minute
            self.minute_chime(  )
            return
        # if an hour chime we need to do minute 60
        # then hour,
        # then minute 0
        msg     = "hour chime: " + str( self.current_hour )
        #print( msg )
        AppGlobal.helper_thread.print_info_string( msg )
        # !! more chime types inc none set up as a dict, change to 24 hour enabled 

        #  self.minute_chime(  60 )   old code .... did this do something useful?? !!

        chime_type    = AppGlobal.parameters.chime_type
        chime         = "0"
        if    chime_type == "random":
              chime      = self.hour_random_chime( self.current_hour )

        elif  chime_type == "assigned":
              chime      = self.hour_assigned_chime( self.current_hour )
              
        elif  chime_type == "rotate":
              chime      = self.hour_rotate_chime( self.current_hour )
              

        self.do_hour_chime( chime,  )
        self.last_hour    = self.current_hour
        self.minute_chime(  )

        # !!     self.display_time()
        AppGlobal.helper_thread_ext.display_time()

    # -------------------------------------------------
    def minute_chime( self,  ):  #
        """
        Purpose:  do minute chime, if it is time
                  this determines which chime should be used

        ?? do hour dance if appropriate
        Args:    a_minute   .. used as arg to facilitate demo mode

        """
        self.led_chime()
        a_minute      = self.current_minute

        if self.last_minute == self.current_minute:
            # no chime
            return

#        # !! disable minutes
#        self.last_minute = a_minute
#        self.display_time()
#        return
        msg     = "minute chime: " + str( a_minute )
        #print( msg )
        AppGlobal.helper_thread.print_info_string( msg )

        if a_minute not in AppGlobal.parameters.minute_chime_dict:
            minute_chime   = "0"
        else:
            minute_chime   =  AppGlobal.parameters.minute_chime_dict[ a_minute ]

        self.do_minute_chime( minute_chime, self.current_minute )

        self.last_minute = self.current_minute

        AppGlobal.helper_thread_ext.display_time()

    # -------------------------------------------------
    def led_chime( self,  ):  #
        """
        Purpose:  do led, if it is time


        Args:   self.

        """
        if self.last_led_tick == self.current_led_tick:
            return     # no chime

        self.last_led_tick      = self.current_led_tick

        msg     = "led chime: " + str( self.current_led_tick  )

        AppGlobal.helper_thread.print_info_string( msg )

        AppGlobal.helper_thread.send_receive(  self.get_led_pwm(   ), self.set_wait_time  )

    # -------------------------------------------------
    def do_hour_chime( self, a_chime, ):  #a_hour ):
          """
          actually send the string to the arduino to do the chime
          chime is managed in the arduino, may want to extend with code in python ??
          arduino complains but does not fail if a_chime out of range
          call from hour_chime probably
          Args:     a_chime    chime number as a string -- check with arduino for valid range, !! move setting to parms
          """
          a_hour     = self.current_hour
          if AppGlobal.parameters.hour_off:
              return

          send_data   = "c1 " + a_chime + " " + str( a_hour )
          AppGlobal.helper_thread.send_receive( send_data, self.set_wait_time  )
          time.sleep( 3 )   # but in gui thread i think  !!

    # -------------------------------------------------
    def do_minute_chime( self, a_chime, a_minute ):
          """
          as in name, parameters may disable
          for better speed make a_chime a string
          Args: a_chime, chime number as a string
                  a_minute  chime minute a number ??
          """
  #          print( "called do_minute_chime" )
  #          return
          #
          if AppGlobal.parameters.minute_off:
              return
          send_data   = "c2 " + a_chime + " " + str( a_minute )
          AppGlobal.helper_thread.send_receive( send_data, self.set_wait_time  )

    # -------------------------------------------------
    def get_led_pwm( self, ):
        """
        Purpose: see return
        Args:
            self.current_led_tick
            self.current_hour_24
        Returns:
            pwm value as a string
        """
        try:
            background   = self.led_background_values[ self.current_hour_24 ]
        except KeyError as exception:
            background   = 5  # parm it ??

        if self.current_led_tick == None:
            pwm   = "l" + str( background )  # py 3.5
            return pwm

        try:
            led_multiplier   = self.led_chime_values[ self.current_led_tick  ]
        except KeyError as exception:
            led_multiplier   = 1.

        brightness   = min( int( background * led_multiplier ), 254  )
        pwm     = "l" + str( brightness  )

        return pwm

    # -------------------------------------------------
    def get_led_background( self,  ):  #
        """
        not called yet, !! code in ??
        Purpose:
            determine the led pwm during the more or less off time
            for example
                bright during the day
                dim at night
                off for karen
        Note: for effiency may save old value so the recalc need not be made
        Args:
            self.current_hour_24
        Return:
            led_pwm value
        """
        if   self.current_minute >= 10 and self.current_minute <= 20:
            self.current_led_minute   = 15
        elif self.current_minute >= 25 and self.current_minute <= 35:
            self.current_led_minute   = 30
        elif self.current_minute >= 40 and self.current_minute <= 50:
            self.current_led_minute   = 45
        elif self.current_minute >= 55 and self.current_minute <= 60:
            self.current_led_minute   = 0
        elif self.current_minute >= 0 and self.current_minute <= 5:
            self.current_led_minute   = 0
        else:
            self.current_led_minute   = None

    # -------------------------------------------------
    def hour_assigned_chime( self, a_hour ):  #
        """
        each hour is assigned a deterministic time
        may need to maintain for number of chimes
        return string
        !! looks like a default would be a good idea
        Arg: a_hour   number ?? pretty sure
        Return:  chime_type, number as a string
        """
        try:
            chime_type    = AppGlobal.parameters.hour_chime_dict[ a_hour ]
        except KeyError as exception:
            chime_type    = 0 
            msg           = " key error in hour_assigned_chime for key a hour " + str( a_hour ) + " default to 0"
            self.logger.debug( msg ) 
            
        return( chime_type )

    # -------------------------------------------------
    def hour_random_chime( self, a_hour ):  #
        """
        may need to maintain for number of chimes in parms?
        return string
        !! make range auto why a_hour -- looks like to keep the call signature consistent        Arg: a_hour   string number ??
        Return:  chime_type, probably a number as a string

        """
        return( str( random.randrange( 0, 13 ) ) )  # !! update to match chimes in....
        
    # -------------------------------------------------
    def hour_rotate_chime( self, a_hour ):  #
        """
        advance by some number thru the total number of chimes
        the advance should probably be relatively prime to the total
        number of availabe chimes
        
        Arg: a_hour   not used but signature same for all
        Return:  chime_type,  number as a string

        """
        self.hour_rotate_index  += AppGlobal.parameters.hour_chime_rotate_amt
        
        if self.hour_rotate_index >= len( AppGlobal.parameters.hour_chime_rotate_list ):
            self.hour_rotate_index = 0
        
        return( AppGlobal.parameters.hour_chime_rotate_list[ self.hour_rotate_index ] ) 
        
  
# ================= Class =======================
#
class DDCProcessing( abc_def.ABCProcessing ):
    """
    extension for DDCProcessing
    all in helper thread ht except:  __init__, add_gui, and the call backs for the buttons cb_ ... ( unless I missed something )

    """
    # ------------------------------------------
    def __init__( self,    ):
        # call ancestor ??

        AppGlobal.helper_thread_ext  = self     # may be new feb 2019
        AppGlobal.abc_processing     = self     # phase out

        self.controller         = AppGlobal.controller
        self.parameters         = AppGlobal.parameters

        self.helper_thread      = AppGlobal.helper_thread   #  !! WAS   .helper_thread  helper_thread_ext

        self.logger             = logging.getLogger( self.controller.logger_id + ".DDCProcessing")
        self.logger.debug( "in class DDCProcessing init" ) # logger not currently used by here

        #self.minute_delat       = datetime.timedelta( minutes = 1 )   # just a convient unit

#        self.time               = None       # time.time() # set in set_time -- taken as same for all measurements

        self.mode               = "undefined for now "   # "set_min" "set_hr" "run"  "run_demo"

        self.chime_and_time     = ChimeAndTime()

        self.button_actions     = None     # set later

        # these are int value for the aruino interface actually divide by 10 and converted to floats

        # some of these not in parms, phase these out

        # can set short for testing -- does wait check the receive !! ??
        self.set_wait_time      = .10        # what units what mean  --- for arduino response

        random.seed( a=None, version=2 )
        # self.minute_chime_dict = { 14: "1", 15: "1",  }  moved to parms

        # self.real_time          = True      # use the real time else use test time parameters

    # ----------------------------------------
    def add_gui( self, parent, ):  # if this were a class then could access its variables later
        """
        call: gt
        make frame for motor control and return it
        add buttons for different stepping now for unipolar in 3 modes, expand
        """
        button_width        = 20

        self.button_var     = Tk.IntVar()   # must be done after root is created

        ret_frame           = Tk.Frame( parent, width = 600, height=200, bg = self.parameters.bk_color, relief = Tk.RAISED, borderwidth=1 )

        # --------------- row 2
        button_actions      = []

        # ------------------------------------------
        a_button_action         = ButtonAction( self, "Helper: Find and Monitor Arduino", self.cb_find_and_monitor_arduino  )
        # a_button_action.set_args( ( "call", self.controller.helper_thread.test_test_ports  , (  ) ) )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "Helper: \nFind Arduino", self.cb_test_test_ports  )
        # a_button_action.set_args( ( "call", self.controller.helper_thread.test_test_ports  , (  ) ) )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "Interrupt: Helper", self.cb_end_helper )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "Toggle ext polling", self.cb_toggle_ext_polling )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        #color          = "blue"
        a_frame        = Tk.Frame( ret_frame, width = 600, height=200, bg = "gray", relief = Tk.RAISED, borderwidth=1 )

        #a_frame.grid( row = 0, column = 0, sticky = Tk.E + Tk.W + Tk.N  )    # better than pack blow
        #a_frame.pack(  side = Tk.TOP, expand = Tk.YES, ) #fill=Tk.Y ))      # seems to place at middle
        a_frame.pack( side = Tk.LEFT)     # this seems pretty good

        for ix, i_button_action  in  enumerate( button_actions ):
            # make button
            a_button = Tk.Button( a_frame, width = button_width, height = 3, text = i_button_action.name, wraplength = 100 )
            a_button.bind( "<Button-1>", self.do_button_action )
            # 8 is number of buttons across
            a_row     =  0
            a_col     =  ix
            # print( a_row, a_col )
            a_button.grid(  row = a_row, column = a_col, sticky ='E' + "W" )
            a_frame.grid_columnconfigure( a_col, weight=1 )
            i_button_action.set_button( a_button )

        self.button_actions      = button_actions  # controls creation and actions of additional buttons

        a_col   += 1
        self.time_label   = ( Tk.Label( a_frame, text = "time now 00:00", relief = Tk.RAISED, width = button_width,  )  )
        #a_label.grid( row = lrow, column = lcol, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+
        self.time_label.grid(  row = a_row, column = a_col, sticky = "NSEW"    ) #'E' + "W" + "S" + "N" )

        # --------------- row 2
        a_row               =  1
        button_actions      = []

        # ------------------------------------------
        a_button_action         = ButtonAction( self, "Set Hr", self.cb_mode_set_hr  )
        # a_button_action.set_args( ( "call", self.controller.helper_thread.test_test_ports  , (  ) ) )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "Set Min", self.cb_mode_set_min  )
        # a_button_action.set_args( ( "call", self.controller.helper_thread.test_test_ports  , (  ) ) )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "Run", self.cb_mode_run )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "Run Demo", self.cb_mode_run_demo )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "---", self.cb_tweak_minus_3 )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "--", self.cb_tweak_minus_2 )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "-", self.cb_tweak_minus_1 )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "+", self.cb_tweak_plus_1 )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "++", self.cb_tweak_plus_2 )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "+++", self.cb_tweak_plus_3 )
        #a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        a_col   = 0
        a_row   = 1
        for ix, i_button_action  in  enumerate( button_actions ):
            # make button
            a_button = Tk.Button( a_frame, width = button_width, height = 2, text = i_button_action.name, wraplength = 100 )
            a_button.bind( "<Button-1>", self.do_button_action )
            # 8 is number of buttons across
            #a_row     =  0
            if ix <= 3:
                a_col  =   ix
            else:
                a_col  = ix -4
                a_row  = 2

            # print( a_row, a_col )
            a_button.grid(  row = a_row, column = a_col, sticky ='E' + "W" )
            a_frame.grid_columnconfigure( a_col, weight=1 )
            i_button_action.set_button( a_button )

            if   ix == 0:
                self.set_hr_button     = a_button
            elif ix == 1:
                self.set_min_button    = a_button
            elif ix == 2:
                 self.run_button       = a_button
            elif ix == 3:
                 self.run_demo_button  = a_button
                 pass

            self.button_actions      += button_actions

        return ret_frame

    # ----------------------------------------
    def monitor_arduino_loop( self ):
        """
        green house, adapt for ddclock ?? -- right now I used extended polling instead
        this is not used

        assumes port opened successfully
        infinite loop
        call: run in ht not controller
        ret: only on failure, probably should be exception
        """
        pass

    # ----------------------------------------
    def auto_run( self ):
        """
        this really needs to be in the helper thread so that is how we will kick it off using
        the queud, this may limit arguments or they may have to be gotten at in some other way
        run is gui thread, may lock it up is there a way to yield control briefly, the delay should do it
        !! may want in a try and swallow any error as it will kill other stuff
        """
        helper_thread    = self.controller.helper_thread

#        helper_thread.print_info_string( "first"  )
#        time.sleep( 15 )
#        helper_thread.print_info_string( "second" )
#        time.sleep( 5 )
#        helper_thread.print_info_string( "third"  )

        helper_thread.sleep_ht_with_msg_for( 10, "Beginning auto_run... ", 5, True )

        ok, a_port = helper_thread.find_arduino( )

        #helper_thread.release_gui_for( 0 )
        if not( ok ):

             helper_thread.print_info_string(   "Error: Arduino not found -- looked for " + self.parameters.arduino_version ) # + a_port )
             #return
             #helper_label.config( text = "found arduino on " + a_port )    # helper_thread
             #self.controller.gui.show_item( "helper_info", "found arduino on " + a_port )

        # continut on to run, do not worry so much about old state
        helper_thread.print_info_string(  "found Arduino on " + a_port )

        active_color   = "red"
        passive_color  = "light gray"

        self.set_hr_button.config( background       = passive_color )
        self.set_hr_button.config( activebackground = passive_color )  # not sure what this does see ex tkinkter -- may differ on linux

        self.set_min_button.config( background       = passive_color )
        self.set_min_button.config( activebackground = passive_color )

        self.run_button.config( background           = passive_color )
        self.run_button.config( activebackground     = passive_color )

        #self.run_button.config( activebackground = "red" )
        self.run_demo_button.config( background       = passive_color )
        self.run_demo_button.config( activebackground = passive_color )
        # --------------

        self.run_button.config( background       = active_color )
        self.run_button.config( activebackground = active_color )  # for linux

        self.last_datetime = None  # normally done in ht but it should not be running now so ok??
        self.start_clock()

        self.mode  = "run"

    # ----------------------------------------
    def find_and_monitor_arduino( self ):
        """
        looks dead, at least for now
        green house, adapt for ddclock ?? or move to main helper ??
        call: ht

        """
        helper_thread    = self.controller.helper_thread
        #gui              = self.controller.gui
        #helper_label     = gui.helper_label

        helper_thread.sleep_ht_with_msg_for( 10, "Beginning find and Monitor Arduino... ", 5, True )

        ok, a_port = helper_thread.find_arduino( )

        #helper_thread.release_gui_for( 0 )
        if ok:
             #helper_label.config( text = "found arduino on " + a_port )    # helper_thread
             #self.controller.gui.show_item( "helper_info", "found arduino on " + a_port )
             helper_thread.print_info_string(  "found Arduino on " + a_port )
             #self.monitor_arduino_loop()
        else:
             #helper_label.config( text = "arduino not found " )
             #self.controller.gui.show_item( "helper_info", "arduino not found " )
             helper_thread.print_info_string(   "Error: Arduino not found -- looked for " + self.parameters.arduino_version ) # + a_port )

    # -------------------------------------------------
    def polling_ext( self, ):
        """
        extension from polling in smart_terminal_helper
        call  ht
        instead of calling a looping function, i do both sometimes, why??
        """
        #print( "polling_ext" )
         # may not be using this but just call some other loop ???

        self.chime_and_time.polling(  )  # sets instance var
#        print( timeish.strftime("%Y-%m-%d %H:%M:%S") )

#        self.chime_and_time.hour_chime( self.current_hour   )  #
        #self.minute_chime(  self.current_minute )
        #self.hour_chime(    self.current_hour   )  #

    # -------------------------------------------------
    def start_clock( self, ):
        """
        start the time running
        which thread, now in gt but this may be bad !!
        in gt, sets a flag to kick off running
        violate to ht in auto_run perhaps
        """
        AppGlobal.helper_thread.processing_ext_enabled   = False
        # delay perhaps better move to other thread
#        self.chime_and_time.last_datetime                = None
        
        self.chime_and_time.init_time()    
        
        
        # should send init set of hands for minuet, hour, led, this is in gt so 
        # could post over, but it would not process for a bit so could
        # untill enabled, but running here may be ok
        # try out in gt
        # try just running polling
        
        self.chime_and_time.polling()
        
        AppGlobal.helper_thread.processing_ext_enabled   = True

    # -------------------------------------------------
    def display_time( self, ):
        """
        display instance time in the gui .. probably should be done from gui thread, not helper
        does not move the hands
        """
        minute_text  = ("000" + str( self.chime_and_time.last_minute ))
        minute_text  = minute_text[ -2: ]
        self.time_label.config( text =  "time => " + str( self.chime_and_time.last_hour ) + ":" + minute_text )

  # ----------------------------------
    def change_mode( self, old_mode, new_mode ):
         """
         thread: gt
         may call in ht for auto start
         may want to look into the tweak buttons, enable disable
         """
         active_color   = "red"
         passive_color  = "light gray"
         if old_mode == new_mode:
             return

         if  old_mode  == "set_hr":
             self.set_hr_button.config( background       = passive_color )
             self.set_hr_button.config( activebackground = passive_color )  # not sure what this does see ex tkinkter -- may differ on linux

         elif old_mode  == "set_min":
             self.set_min_button.config( background       = passive_color )
             self.set_min_button.config( activebackground = passive_color )

         elif old_mode  == "run":
             self.run_button.config( background       = passive_color )
             self.run_button.config( activebackground = passive_color )

         elif old_mode  == "run_demo":
             #self.run_button.config( activebackground = "red" )
             self.run_demo_button.config( background       = passive_color )
             self.run_demo_button.config( activebackground = passive_color )
         # --------------
         if   new_mode  == "set_min":
             self.set_min_button.config( background       = active_color )
             self.set_min_button.config( activebackground = active_color )

             AppGlobal.helper_thread.processing_ext_enabled   = False
             AppGlobal.gui.print_info_string( "Set Min to 0 ")
             self.controller.send( "c2 0 0"  )
             self.controller.send( "c1 0 12" )

         elif new_mode  == "set_hr":
             # ?? post some message ?
             self.set_hr_button.config( background       = active_color )
             self.set_hr_button.config( activebackground = active_color )

             AppGlobal.helper_thread.processing_ext_enabled   = False
             AppGlobal.gui.print_info_string( "Set Hr to 12 ")
             self.controller.send( "c1 0 12" )
             self.controller.send( "c2 0 0"  )

         elif new_mode  == "run":
             self.run_button.config( background       = active_color )
             self.run_button.config( activebackground = active_color )  # for linux

             self.last_datetime    = None  # normally done in ht but it should not be running now so ok??
             AppGlobal.clock_mode  = "run"
             self.start_clock()

         elif new_mode  == "run_demo":
             self.run_demo_button.config( background       = active_color )
             self.run_demo_button.config( activebackground = active_color )
             AppGlobal.clock_mode  = "run_demo"
             self.last_datetime    = None  # normally done in ht but it should not be running now so ok??
             self.start_clock()

         self.mode  = new_mode

     # -------------------------------------------------
    def do_tweak( self, tweak_amt ):
        """
        tweak the clock hand by a small amount,
        use dict instead amt or could easily be done in button in a few lines
        or send amount as a string
        """
#        print( "do_tweak " + self.mode )
        if  ( self.mode  != "set_hr" ) and ( self.mode  != "set_min" ):
            return

        action  = "t"
        mode    = "1 "
        amt     = "1"

        if self.mode  == "set_min":
            mode    = "2 "    # min
        else:
            mode    = "1 "    # hr

        # or a dict with tuples
        if   tweak_amt == 3:
            amt      = "20"
            action   = "n"
        elif tweak_amt == 2:
            amt      = "8"
            action   = "n"
        elif tweak_amt == 1:
            amt      = "1"
            action   = "t"
        elif tweak_amt == -1:
            amt      = "-1"
            action   = "t"
        elif tweak_amt == -2:
            amt      = "-8"
            action   = "n"
        elif tweak_amt == -3:
            amt      = "-20"
            action   = "n"
        else:
            # should not be one
            pass

        # unclear this should go to helper thread !!
        send_data   = action + mode + amt
        self.helper_thread.send_receive( send_data, self.set_wait_time  )
        #time.sleep( 3 )   # but in gui thread i think

    # ----------------------- cb_ is a call back normally for a button in gt ----------------

    def do_button_action( self, event ):
        """
        call: gt
        think this works but is odd we can actually do function based on the widget, and this does not
        do a good job if invalid button is called
        easy to add functions that look at the button text but could actually use the button instance self.button_actions.
        """
        for ix, i_button_action in  enumerate( self.button_actions ):
            text     = i_button_action.name       # or i_button_action.button == event.widget  !! probably better
            btext    = event.widget[ "text" ]
            if event.widget == i_button_action.button:
                #event.widget.config( bg="gray" )   # this may blink the button when the action happens look into this
                i_button_action.function( i_button_action.function_args )
                # self.current_action =  act    # not sure what did look in old cod
                break

    #----------------------------------------------
    def cb_test_test_ports( self, ignore ):
        """
        call:  cb in gt, use post if calling ht
        """
        self.controller.post_to_queue( "call", self.controller.helper_thread.find_arduino  , (  ) )

    # -------------------------------------------------
    def cb_find_and_monitor_arduino( self, a_list ):  #
        """
        call: gt
        """
        # port from gt to ht
        self.controller.post_to_queue( "call", self.find_and_monitor_arduino, (  ) )

    # -------------------------------------------------
    def cb_end_helper( self, ignore ):
        #print( "ignore", ignore )
           # self.controller.           helper_thread.test_test_ports(   , (  ) )
        self.controller.post_to_queue( "call", self.controller.helper_thread.end_helper  , (  ) )

     # -------------------------------------------------
    def cb_toggle_ext_polling( self, ignore ):
         AppGlobal.helper_thread.processing_ext_enabled   = not( AppGlobal.helper.processing_ext_enabled )

     # -------------------------------------------------
    def cb_start_clock( self, ignore ):
         self.start_clock()

     # -------------------------------------------------
    def cb_mode_set_hr( self, ignore ):
         self.change_mode(  self.mode, "set_hr" )

    # -------------------------------------------------
    def cb_mode_set_min( self, ignore ):
         self.change_mode(  self.mode, "set_min" )

    # -------------------------------------------------
    def cb_mode_run( self, ignore ):
         #pass
         self.change_mode(  self.mode, "run" )

    # -------------------------------------------------
    def cb_mode_run_demo( self, ignore ):
         #pass
         self.change_mode(  self.mode, "run_demo" )

    # -------------------------------------------------
    def cb_tweak_minus_3( self, ignore ):
        self.do_tweak( -3 )

#    def cb_tweak_minus_3( self, ignore ):
#        self.do_tweak( -3 )
    # -------------------------------------------------
    def cb_tweak_minus_2( self, ignore ):
        self.do_tweak( -2 )

    def cb_tweak_minus_1( self, ignore ):
        self.do_tweak( -1 )

    def cb_tweak_plus_1( self, ignore ):
        self.do_tweak( 1 )

    def cb_tweak_plus_2( self, ignore ):
        self.do_tweak( 2 )

    def cb_tweak_plus_3( self, ignore ):
        self.do_tweak( 3 )

# =================================
class ButtonAction( object ):
    """
    this may become an abstract class for plug in button actions in the smart terminal, a bit like processing add to the array
    need ref to my processing object probably
    hold info to implement a button in the gui
    looks like a struct so far
    parts are not all used, may not be used as named  see add_gui
    think once had more grand plans, may go back to it as dict with button the key, way to put in named var.
    """
    def __init__( self, a_processor, a_name, a_function ):
        self.processor       =  a_processor     # why this it is a mini controller where used?
        self.name            =  a_name
        self.function        =  a_function      # where are the arguments elsewhere in the thing in function_args with set_args
        self.function_args   = [ self.name, "I am an argument", "and another " ]
        self.button          = None

    # -------------------------------------------------
    def set_button( self, a_button ):
        """
        use when button actually created ( or move a factory in here??) may not be used
        """
        self.button          = a_button

    # -------------------------------------------------
    def set_args( self, a_args ):
        """
        set args, but unless list seems can only set one
        maybe make a tuple and use *() when calling to unpack
        """
        self.function_args   = a_args

# ----------------------------------------------------------

#import test_controller

if __name__ == '__main__':
    """
    test
    this really does not work without a controller or parameters
    can we make one here
    """
    print( "" )
    print( " ========== starting SmartTerminal from gr_processing.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )


# ======================= eof =====================





