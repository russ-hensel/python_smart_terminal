# -*- coding: utf-8 -*-

"""
ext_process_dm.py (for smart_terminal.py ) extended processing for dear me : this does the actions to scare away the deer

"""

import logging
import datetime
import abc_def
import tkinter as Tk
import random
#import time
import simpleaudio as sa
# import numpy as np

# -------------- local libs ------------------
from    app_global import AppGlobal

import  smart_terminal

# ================= Class =======================
#
class TickTimeMaker(  ):
    """
    makes a TickTimer for now rotating from a list later more random
    """
    # ------------------------------------------
    def __init__( self,    ):
        """
        """
        # msg    = (f"init TickTimeMaker{1+2}")
        # AppGlobal.logger.info( msg )
        random.seed( a=None, version=2 )   # default a is to use system time

        self.ix_tick_timer         = -1   # start from 0 but pre increment

        self.tick_timer_makers     = []   # for now just a list of functions

        a_tick_timer_maker         =  ( self.setup_light_out_of_sync, self.setup_sound_battle_drums )
        self.tick_timer_makers.append( a_tick_timer_maker )

        a_tick_timer_maker          =  ( self.setup_light_strobe_1,   self.setup_sound_ambulance )
        self.tick_timer_makers.append( a_tick_timer_maker )

        self.ix_tick_timer_max      = len( self.tick_timer_makers )


        # ------ sound
        self.sound_makers           = [
                                             self.setup_sound_battle_drums,
                                             self.setup_sound_ambulance,
                                             self.setup_sound_bomb,
                                             self.setup_sound_coyote,
                                             self.setup_sound_dogs_barking,

                                        ]

        # # this for testing else comment out
        # self.sound_makers           = [
        #                                      self.setup_sound_battle_drums,

        #                                 ]


        # ----- light
        # can set to just one for testing
        self.light_makers           = [
                                            self.setup_light_strobe_1,
                                            self.setup_light_out_of_sync,
                                            self.setup_light_alt_strobe,
                                        ]
        # # this for testing else comment out
        # self.light_makers           = [
        #                                     self.setup_light_alt_strobe,
        #                                 ]

   # ----------------------------------------
    def next_tick_timer( self, a_tick_timer ):
        """
        get a new tick_timer or reset old
        we get a light setup and a sound setup both functions
        then we call the functions against the tick timer
        which modifies it effectively making it a new one
        """
        if a_tick_timer   is None:
            a_tick_timer   = TickTimer()
        else:
            a_tick_timer.reset()

        # for now this is patched to only use random !!
        if False:
            self.ix_tick_timer       += 1
            if  self.ix_tick_timer_max   <= self.ix_tick_timer:
                self.ix_tick_timer    = 0

            light_setup, sound_setup  = self.tick_timer_makers[ self.ix_tick_timer ]
        else:
            ix      = random.randrange( 0, len( self.light_makers ) )

            light_setup     = self.light_makers[ ix ]

            ix      = random.randrange( 0, len( self.sound_makers ) )
            sound_setup     =   self.sound_makers[ ix ]

        # perhaps a reset here .......
        a_tick_timer.reset()

        light_setup( a_tick_timer )
        sound_setup( a_tick_timer )

        msg   = f"new TickTimer {a_tick_timer.timer_name}"
        AppGlobal.helper_thread.print_info_string( msg )
        AppGlobal.logger.debug( msg )

        return a_tick_timer

   # ----------------------------------------
    def get_next_done_at( self ):
        """
        what is says
        later make random -- this fixed time for some testing
        """
        dt_next      =   ( datetime.datetime.now() +

                           datetime.timedelta( seconds =  15 *  60  ) )
                           #  or perhaps also useful     datetime.timedelta( seconds=5, minutes=17, hours=2, days=55 )
                           # datetime.timedelta( seconds = ( 5 * 60  ) + 30  ) )
        return dt_next


#----------- Here be lights
   # ----------------------------------------
    def setup_light_out_of_sync( self, a_tick_timer ):
        """
        setup_light..... functions justs sets some instance variables
                         into the tick timer, this will control the arduinos light behaviour
        two lights fairly long blink, drift out of sync
        light A  1 sec on 1 sec off, one sec on 1 sec off....                              1000  0 1000 0
        light B  1 sec on 1.1 sec off, one sec on 1.1 sec off....   all for 20 seconds     1000  0 1100 0

        arg     a_tick_timer    what it says, already reset
        retun   a_tick_timer
        """
        a_tick_timer.timer_name            = "out_of_sync"

        a_tick_timer.done_at               = self.get_next_done_at()

        a_tick_timer.ix_cycle_max          = 30     # counter is number of times we cycle tick max and roll it over

        a_tick_timer.ix_tick_max           = 2000    # roll over tick actions -- new cycle?? tenths

        # set next as necessary -- add as necessary -- access as properties

        a_tick_timer.tick_strs_0            = ["i0", "l1000 9 1000 9", "i1", "l1000 9 1100 9", "s1" ]

        return a_tick_timer

  # ----------------------------------------
    def setup_light_strobe_1( self, a_tick_timer ):
        """
        two lights fairly long blink, drift out of sync
        light A  1 sec on 1 sec off, one sec on 1 sec off....                              1000  0 1000 0
        light B  1 sec on 1.1 sec off, one sec on 1.1 sec off....   all for 20 seconds     1000  0 1100 0
        """
        a_tick_timer.timer_name            = "strobe_1"
        a_tick_timer.done_at               = self.get_next_done_at()

        a_tick_timer.ix_cycle_max          = 1     # close out when reach this

        a_tick_timer.ix_tick_max           = 200   # roll over tick actions

        # set next as necessary -- add as necessary -- access as properties
        a_tick_timer.ix_tick_act_1         = -1     # -1 not used
        a_tick_timer.ix_tick_act_2         = -1

        a_tick_timer.tick_strs_0            = ["i0", "l1000 9 1000 9", "i1", "l1000 9 1100 9", "s1" ]

        return a_tick_timer

  # ----------------------------------------
    def setup_light_alt_strobe( self, a_tick_timer ):
        """
        in dev ....
        first one light strobes, then the other then both
        consider 20 seconds for each
        this is also a test for setting up tick_act > 0

        """
        a_tick_timer.timer_name            = "alt_strobe"
        a_tick_timer.done_at               = self.get_next_done_at()

        a_tick_timer.ix_cycle_max          = 2     # close out when reach this  number of cycles around the settings so 2 cycles, ix_cycle == 2 does not run

        a_tick_timer.ix_tick_max           = 180   # roll over tick actions  -- think this is in units of .1 sec ?? or seconds  - set in parms keep at .1 sec


        # check for single spaces or none in strings
        # light A  .1 sec on .9 sec off, ...                            100  0 900 0
        # light B  off     not sure how to do this try     1  0 1000 *100  0          = 1 0 100000 0    # !! try from terminal could first num be 0
        a_tick_timer.tick_strs_0            = ["s0", "i0", "l100 9 900 9", "i1", "l1 9 100000 9", "s1" ]
        #                                code   see arduino program dear_me
        #                                       "i0"              index light to strobe 0
        #                                       "l100 9 900 9",   on for 100 ms, off for 900 ms, the 9's are ignore by s1
        #                                       "i1"    ..... repeat for strobe 1
        #                                       "s1"  run the strobe routine s1

        # second sequence
        a_tick_timer.ix_tick_act_1         = 30     # -1 means not used

        # light B .1 sec on .9 sec off, ...                            100  0 900 0
        # light A  off     not sure how to do this try     1  0 1000 *100  0          = 1 0 100000 0    # !! try from terminal could first num be 0
        #                                               off                    rapid short blink
        a_tick_timer.tick_strs_1           = ["s0", "i0", "l1 9 100000 9", "i1", "l100 9 900 9", "s1" ]

        # third sequence
        a_tick_timer.ix_tick_act_2         = 60     # -1 means not used

        # light B  rapid short blink                           100  0 900 0
        # light A  rapid short blink
        #                                           rapid short blink         rapid short blink
        a_tick_timer.tick_strs_2           = ["s0", "i0", "l1 9 100000 9", "i1", "l100 9 900 9", "s1" ]

        # may want to compute based on above
        # a_tick_timer.ix_tick_max           = 600   # roll over tick actions  -- think this is in units of .1 sec ?? or seconds  - set in parms keep at .1 sec


        return a_tick_timer

#----------- Here be Sounds
   # ----------------------------------------
    def setup_sound_battle_drums(self, a_tick_timer ):
        """
        setup_sound..... functions justs sets some instance variables
                         into the tick timer, this will what sounds are played
        """

        a_tick_timer.timer_name            += "/battle_drums"
        a_tick_timer.sound_fns             = [
                                               r"./sounds/battle-drum-rolls-sound-effect.wav",
                                               r"./sounds/battle-drum-rolls-sound-effect.wav",

                                             ]
        return a_tick_timer

   # ----------------------------------------
    def setup_sound_ambulance( self, a_tick_timer ):
        a_tick_timer.timer_name            += "/ambulance"
        a_tick_timer.sound_fns             = [
                                               r"./sounds/ambulance-siren-distant.wav",
                                               r"./sounds/ambulance-siren-distant.wav",
                                             ]
        return a_tick_timer

   # ----------------------------------------
    def setup_sound_bomb( self, a_tick_timer ):
        a_tick_timer.timer_name            += "/bomb"
        a_tick_timer.sound_fns             = [
                                               r"./sounds/bomb-sound-effect.wav",
                                             ]
        return a_tick_timer

   # ----------------------------------------
    def setup_sound_coyote( self, a_tick_timer ):
        a_tick_timer.timer_name            += "/coyote"
        a_tick_timer.sound_fns             = [
                                               r"./sounds/coyote-calls.wav",
                                             ]
        return a_tick_timer

   # ----------------------------------------
    def setup_sound_dogs_barking( self, a_tick_timer ):
        a_tick_timer.timer_name            += "/dogs_barking"
        a_tick_timer.sound_fns             = [
                                               r"./sounds/dogs-barking.wav",
                                             ]
        return a_tick_timer

   # ----------------------------------------
    def setup_sound_dog_barking_close( self, a_tick_timer ):
        a_tick_timer.timer_name            += "/dog_barking_close"
        a_tick_timer.sound_fns             = [
                                               r"./sounds/dog-barking-close-sound-effect.wav",
                                             ]
        return a_tick_timer

   # ----------------------------------------
    def setup_sound_dogs_barking_aggressive( self, a_tick_timer ):
        a_tick_timer.timer_name            += "/dogs_barking_aggressive"
        a_tick_timer.sound_fns             = [
                                               r"./sounds/Dogs-barking-aggressive-sound-loop.wav",
                                             ]
        return a_tick_timer

   # ----------------------------------------
    def setup_sound_drum_beat( self, a_tick_timer ):
        a_tick_timer.timer_name            += "/drum_beat"
        a_tick_timer.sound_fns             = [
                                               r"./sounds/drum-beat-sound-effect.wav",
                                             ]
        return a_tick_timer


    test_list  = [
        r"./sounds/ambulance-siren-distant.wav",
        r"./sounds/battle-drum-rolls-sound-effect.wav",
        r"./sounds/bomb-sound-effect.wav",
        r"./sounds/coyote-calls.wav",
        r"./sounds/dog-barking-close-sound-effect.wav",
        r"./sounds/dogs-barking.wav",
        r"./sounds/Dogs-barking-aggressive-sound-loop.wav",
        r"./sounds/drum-beat-sound-effect.wav",
        r"./sounds/drum-beat-sound-effect-2.wav",
        r"./sounds/emergency-siren-close-long.wav",
        r"./sounds/hunting-dogs-sound-effects.wav",
        r"./sounds/loud-alarm-tone.wav",
        r"./sounds/loud-train-horn-sound.wav",
        r"./sounds/military-sounds.wav",
        r"./sounds/police-siren-sound.wav",
        r"./sounds/SgP.wav",
        r"./sounds/thuder-strike-sound.wav",
        r"./sounds/train-sound.wav",
        r"./sounds/wavedemo6.wav",
        r"./sounds/wolf-howling-sound-effect.wav",
        ]


    # # ----------------------------------------
    # def setup_strobe_1( self, ):
    #     """
    #     not tested
    #     1 tenth on, 1 tenth off, 1 tenth on  .... off for 10 seconds
    #     """
    #     a_tick_timer                       = TickTimer()
    #     a_tick_timer.timer_name            = "setup_strobe_1" # see if meta programming way to do this

    #     a_tick_timer.sound_fns             =  [ r"./sounds/SgP.wav", r"./sounds/SgP.wav",]

    #     a_tick_timer.ix_cycle_max          = 1     # close out when reach this

    #     a_tick_timer.ix_tick_max           = 200   # roll over tick actions

    #     # set next as necessary -- add as necessary -- access as properties
    #     a_tick_timer.ix_tick_act_1         = -1     # -1 not used
    #     a_tick_timer.ix_tick_act_2         = -1

    #     a_tick_timer.tick_strs_0            = ["i0", "l1000 9 1000 9", "i1", "l1000 9 1100 9", "s1" ]

    #     # self.ticker.add_ticker_timer( a_tick_timer )
    #     return a_tick_timer

# ================= Class =======================
#
class TickTimer(   ):
    """
    does some action based on ticks, uses a time base measured in ticks, called in some way from polling
    not sure if this will be basis for an abstract class or not
    for now assume acts in a cycle, tick time rolls over at timer


    Seems to be based on two major cycles
         ticks happend each .1 seconds, none are skipped, ints, so == is exact
         Inner    ix_tick         increment on each tick goes to max ix_tick_max then rolls over
         outter   ix_cycle        increment on each roll over of ix_tick   goes to ix_cycle_max ( unless 0 run forever )

    """
    # ------------------------------------------
    def __init__( self,    ):
        """
        meant to be parameterized and extended
        """

        self.reset()

   # ------------------------------------------
    def __str__( self,    ):
        """
        meant to be parameterized and extended
        """
        a_str      = f"TickTimer                    {self.timer_name}"

        a_str      = f"{a_str}\n     sound_fn_ix        {self.sound_fn_ix }"    # this can index off to infininty that is ok
        a_str      = f"{a_str}\n     self.sound_player  {self.ix_cycle }"
        # self.sound_player.is_playing()   but could be none

        a_str      = f"{a_str}\n     ix_cycle       {self.ix_cycle }"
        a_str      = f"{a_str}\n     ix_cycle_max   {self.ix_cycle_max }"

        a_str      = f"{a_str}\n     ix_tick            {self.ix_tick }"
        a_str      = f"{a_str}\n     ix_tick_max        {self.ix_tick_max }"

        a_str      = f"{a_str}\n     ix_tick_act_1  {self.ix_tick_act_1 }"
        a_str      = f"{a_str}\n     ix_tick_act_2  {self.ix_tick_act_2 }"

        a_str      = f"{a_str}\n     is_closed          {self.is_closed }"

        # a_str      = f"{a_str}\n     ix_tick_act_2    {self.ix_tick_act_2 }"
        # a_str      = f"{a_str}\n     ix_tick       {self.ix_tick }"

        a_str      = f"{a_str}\n     done_at             {self.done_at }"

        return a_str

    # ------------------------------------------
    def reset( self,    ):
        """
        do what ever is necessary to reset for reuse -- dups ?
        """
        self.sound_player          = None
        self.sound_fn_ix           = 0

        self.sound_fns             = None
        self.ix_cycle              = 0    # incremented when tick rolls over
        self.ix_cycle_max          = 10   # "close out when reach this" if 0 run for ever -- this is no of cycle the cycle at this number does not run
        self.ix_tick               = -1   # since we increment befor testing
        self.ix_tick_max           = 10   # roll over tick actions

        # set next as necessary -- add as necessary -- access as properties
        # change to lists ?
        # these controll actions when ix_tick reaches specific values, array approach would probably be and improvement
        self.ix_tick_act_1         = -1   # time in ticks to send associated list of strings -1 for never
        self.ix_tick_act_2         = -1   # as with _1

        self.tick_strs_0           = []
        self.tick_strs_1           = []
        self.tick_strs_2           = []

        self.close_strs            = ["!"]
        self.timer_name            = "some timer no name"    # really a debug or info thing

        self.sound_fns             = []
        self.done_at               = None    # when we make a new one -- this is invalid, so immediately set in some function
        self.is_closed             = False   # no longer playing, but resting until done_at

    # ------------------------------------------
    def close( self,    ):
        """
        do what ever is necessary to shut me down
        """
        # means done or inactive, quicker test -- but may still be waiting for next tick_timer to be started
        # msg     = f"close() for tick_timer = {self}"
        # # print( msg )
        # AppGlobal.logger.info( msg )
        # print( self.close_strs )  # perhaps #
        self.send_strs( self.close_strs )

        if  self.sound_player  is not None:
            self.sound_player.stop()
            self.sound_player  = None

        self.is_closed   = True

    # ------------------------------------------
    def increment_tick( self,    ):
        """
        increment tick and act on it
        we have both sound behavior and light behaviour
            sound
                play the sounds one after the other, each time around if we are still active we
                see if a sound is playing, and if not go to next if any.
            light
                light ususally sets final time
                at tick = 0 send
                at self.ix_tick_act_1:    send tick_strs_1 and so on .... last check up to 2
                                          if the ix_tick_act_n is -1 it never "happens"

        """
        self.ix_tick    += 1

        # print( f"increment_tick {self.ix_tick}")
        if self.is_closed:   # when reached max cycles we have been flagged done but may not ready for a new one
            return

        if ( len ( self.sound_fns ) > 0 ) and ( self.sound_player is None ):
            # first time through and need sound to play
             fn                  = self.sound_fns[ self.sound_fn_ix ]
             wave_obj            = sa.WaveObject.from_wave_file( fn )
             msg                 = f"play sound (a) from {self.timer_name}: {fn}"
             AppGlobal.helper_thread.print_info_string( msg )
             AppGlobal.logger.info( msg )

             self.sound_player   = wave_obj.play()

        elif  ( self.sound_player is not None ) and ( not ( self.sound_player.is_playing() ) ):      # not playing go on to next if exists
            self.sound_fn_ix           += 1
            # msg     = f"incremented sound_fn_ix: {self.sound_fn_ix} len sound_fns:  {len( self.sound_fns )}"
            # AppGlobal.logger.info( msg )

            if self.sound_fn_ix  < len( self.sound_fns ):
                fn                  = self.sound_fns[ self.sound_fn_ix ]
                msg                 = f"play sound (b) from {self.timer_name}: {fn}"
                AppGlobal.helper_thread.print_info_string( msg )
                AppGlobal.logger.info( msg )
                wave_obj            = sa.WaveObject.from_wave_file( fn )
                self.sound_player   = wave_obj.play()


        # start a new cycle
        if self.ix_tick  >= self.ix_tick_max:
            self.ix_tick        = -1  #  because increment before test
            self.ix_cycle      += 1
            self.sound_fn_ix    = 0
            msg   = f"new cycle to {self.ix_cycle}"
            AppGlobal.helper_thread.print_info_string( msg )
            AppGlobal.logger.info( msg )

            # msg   = f"new cycle tick_timer {self}"
            # AppGlobal.logger.info( msg )

            if not( self.ix_cycle_max  == 0 ):
                if self.ix_cycle >= self.ix_cycle_max:
                    msg   = f"{self.timer_name} closing on tick {self.ix_tick} cycle {self.ix_cycle}"
                    AppGlobal.helper_thread.print_info_string( msg )
                    AppGlobal.logger.info( msg )
                    self.close()
                    return

            # now what will do next
        if   self.ix_tick  == 0:
            # for now just send sting 1
            self.send_strs( self.tick_strs_0  )

        elif self.ix_tick  == self.ix_tick_act_1:
            msg   = f"ix_tick_act_1 {self.tick_strs_1}"
            AppGlobal.helper_thread.print_info_string( msg )
            self.send_strs( self.tick_strs_1  )

        elif self.ix_tick  == self.ix_tick_act_2:
            self.send_strs( self.tick_strs_2  )

    # ------------------------------------------
    def send_strs( self,  a_strs  ):
        """
        send list of strings
        """
        msg    =f"send string list {a_strs}"
        AppGlobal.logger.debug( msg )
        msg    =f"sending string tick_timer_now {self}"
        AppGlobal.logger.debug( msg )
        for i_str in a_strs:
            print( i_str )
            AppGlobal.helper_thread.send_receive( i_str, 1  )

        # may be right way to send AppGlobal.helper_thread.send_receive(  self.get_led_pwm(   ), self.set_wait_time  )

# ================= Class =======================
class Ticker(   ):
    """
    sends out the ticks to the TickTimers
    for now a new tick time after every delta_tick_timer
    it is the polling for the tick timer
    """
    # ------------------------------------------
    def __init__( self,    ):
        """
        """
        self.delta_tick                 = datetime.timedelta( seconds = 1 ) #   1 makde calcs easy but may be a bit fast later from parms ??

        self.last_tick_dt               = datetime.datetime( 1973, 0o1, 18, 3, 45, 50)   # 1973-01-18 03:45:50   #  siginifican time in past
        #self.tick_timer_list            = []   # why a list should probably only be one

        self.tick_timer_maker           = TickTimeMaker( )  # this guy makes tick_timers

        # variables for set_next_scare
        self.delta_tick_timer           = 3 * 60 # seconds overrides any individual timing
        self.ix_tick_timer              =  self.delta_tick_timer  # count down to zero

        self.tick_timer                 = self.tick_timer_maker.next_tick_timer( None )

  # ------------------------------------------
    def polling( self,    ):
        """
        what it says
        !! how often called ??   self.parameters.ht_delta_t   ---   we are set up now for .1 sec, keep it this for dm
        !! no matter how often polling is called this cuts the tick down too self.delta_tick as long a polling is at least that fast
        """
        real_now                = datetime.datetime.now()
        time_delta              = real_now - self.last_tick_dt
        if time_delta  < self.delta_tick:
            return

        self.last_tick_dt               = real_now
        # # print( f"tick {time_delta} {real_now}" )
        # for i_tick_timer in self.tick_timer_list:
        #     i_tick_timer.increment_tick()
        if self.tick_timer is not None:
            self.tick_timer.increment_tick()
        else:
            msg    = "no tick_timer"
            print( msg )
            pass

        self.set_next_scare( )   # implicitly called with self.last_tick_dt  now a scare is just a tick_timer

    # ------------------------------------------
    def set_next_scare_old( self, ):   # implicitly called with self.last_tick_dt
        """
        does something only if time is up, in testing was a dead end
        version 2 lets stay in tick timer  -- use status or something
        """
        # idea based on seconds as clock I may come back to it
        tt_now          = self.last_tick_dt.timetuple()
        time_of_day_sec = ( tt_now[3] * 60  * 60 ) + ( tt_now[4] *60 ) + tt_now[5]
        msg   = f"set_next_scare:  time_of_day_sec {time_of_day_sec}"

        # this is simple plan for testing and i need to fix this is killing extended lights.....\]
        xxxx
        self.ix_tick_timer       -= 1
        if  self.ix_tick_timer <= 0:
            self.ix_tick_timer    = self.delta_tick_timer
            # shut down old .... check other code, for now put some here
            msg    = f"set_next_scare -- old tick_timer { self.tick_timer }"
            AppGlobal.logger.info( msg )
            self.tick_timer.close()     # out with old
            self.tick_timer             = self.tick_timer_maker.next_tick_timer( self.tick_timer ) # in with new
            msg   = "NEW tick timer... =================================="
            AppGlobal.helper_thread.print_info_string( msg )
            # shut down old .... check other code, for now put some here

    # ------------------------------------------
    def set_next_scare( self, ):   # implicitly called with self.last_tick_dt
        """
        does something only if time is up, in testing was a dead end
        based on time and some algorithm set up the next TickTimer ( or reuse existing one )
        so as a first try lets have a sorted list by time of day, find the greatest one in the past
        and execute the function at that point -- but need to mark off which are processed so not done again
        """
        if datetime.datetime.now() > self.tick_timer.done_at :

            msg    = f"set_next_scare END this tick_timer "
            AppGlobal.logger.info( msg )
            msg    = f"set_next_scare old tick_timer{ self.tick_timer }"
            AppGlobal.logger.info( msg )
            self.tick_timer.close()     # out with old
            self.tick_timer             = self.tick_timer_maker.next_tick_timer( self.tick_timer ) # in with new
            msg   = "\n\nnew tick timer...============================"
            AppGlobal.helper_thread.print_info_string( msg )
            msg    = f"set_next_scare new tick_timer{ self.tick_timer }"
            AppGlobal.logger.info( msg )


    # ------------------------------------------
    def compute_now( self,    ):
        """
        now is current time to be used by the clock, may be in demo mode so
        that this is a function rather than in line code
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

# ================= Class =======================
#
class DMProcessing( abc_def.ABCProcessing ):  # could we be more generic in name
    """
    extension for DMProcessing: Deer Me
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

        self.ticker             = Ticker()

        #self.chime_and_time     = ChimeAndTime()

        self.button_actions     = None     # set later

        # these are int value for the aruino interface actually divide by 10 and converted to floats

        # some of these not in parms, phase these out

        # can set short for testing -- does wait check the receive !! ??
        self.set_wait_time      = .10        # what units what mean  --- for arduino response

        #random.seed( a=None, version=2 )
        # self.minute_chime_dict = { 14: "1", 15: "1",  }  moved to parms

        # self.real_time          = True      # use the real time else use test time parameters
        #self.test_setup_2()

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

        # # -------------------------
        # a_button_action         = ButtonAction( self, "Interrupt: Helper", self.cb_end_helper )
        # #a_button_action.set_args( the_steping )
        # button_actions.append(   a_button_action )

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

        # a_row   = 0
        # a_col   = 0
        # a_col   += 1
        # self.time_label   = ( Tk.Label( a_frame, text = "time now 00:00", relief = Tk.RAISED, width = button_width,  )  )
        # #a_label.grid( row = lrow, column = lcol, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+
        # self.time_label.grid(  row = a_row, column = a_col, sticky = "NSEW"    ) #'E' + "W" + "S" + "N" )

        a_row               =  1
        button_actions      = []

        return ret_frame

    # ----------------------------------------
    def auto_run( self ):
        """
        used to start off the help thread in an auto start mode, normally controlled from
        parameters
        this really needs to be in the helper thread so that is how we will kick it off using
        the queud, this may limit arguments or they may have to be gotten at in some other way
        run is gui thread, may lock it up is there a way to yield control briefly, the delay should do it
        !! may want in a try and swallow any error as it will kill other stuff
        """
        helper_thread    = self.controller.helper_thread


        helper_thread.sleep_ht_with_msg_for( 10, "Beginning auto_run... ", 5, True )

        ok, a_port = helper_thread.find_arduino( )

        #helper_thread.release_gui_for( 0 )
        if not( ok ):
            msg  = f"Error: Arduino not found -- looked for {self.parameters.arduino_version} )" # + a_port )
            helper_thread.print_info_string(  msg )
            return

        # continut on to run, do not worry so much about old state
        helper_thread.print_info_string(  "found Arduino on " + a_port )
        helper_thread.processing_ext_enabled  = True

        # active_color   = "red"
        # passive_color  = "light gray"

        # self.set_hr_button.config( background       = passive_color )
        # self.set_hr_button.config( activebackground = passive_color )  # not sure what this does see ex tkinkter -- may differ on linux

        # self.set_min_button.config( background       = passive_color )
        # self.set_min_button.config( activebackground = passive_color )

        # self.run_button.config( background           = passive_color )
        # self.run_button.config( activebackground     = passive_color )

        # #self.run_button.config( activebackground = "red" )
        # self.run_demo_button.config( background       = passive_color )
        # self.run_demo_button.config( activebackground = passive_color )
        # # --------------

        # self.run_button.config( background       = active_color )
        # self.run_button.config( activebackground = active_color )  # for linux

        # self.last_datetime = None  # normally done in ht but it should not be running now so ok??
        # self.start_clock()

        # self.mode  = "run"

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
        # print( "polling_ext" )
        self.ticker.polling()

    # ----------------------------------------
    def test_setup_2xxx( self, ):
        """
        make this work with initial arduino setup
        """
        a_tick_timer    = TickTimer()

        a_tick_timer.ix_cycle_max          = 12    # close out when reach this

        a_tick_timer.ix_tick_max           = 10    # roll over tick actions

        # set next as necessary -- add as necessary -- access as properties
        a_tick_timer.ix_tick_act_1         = 2
        a_tick_timer.ix_tick_act_2         = 4

        a_tick_timer.tick_strs_0            = ["i0", "l100 200 130 400", "i1", "l105 200 130 400", "s1" ]

        self.ticker.tick_timer              = a_tick_timer

    # ----------------------------------------
    def test_setup_3xxx( self, ):
        """
        make this work with initial arduino setup
        try for awhile as a second cycle
        """
        a_tick_timer    = TickTimer()

        a_tick_timer.ix_cycle_max          = 3     # close out when reach this

        a_tick_timer.ix_tick_max           = 10    # roll over tick actions

        # set next as necessary -- add as necessary -- access as properties
        a_tick_timer.ix_tick_act_1         = 2
        a_tick_timer.ix_tick_act_2         = 4

        a_tick_timer.tick_strs_0            = ["i0", "l200 200 230 400", "i1", "l205 200 230 400", "s1" ]

        self.ticker.tick_timer              = a_tick_timer

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
         AppGlobal.helper_thread.processing_ext_enabled   = not( AppGlobal.helper_thread.processing_ext_enabled )
         msg    = f"AppGlobal.helper_thread.processing_ext_enabled= {AppGlobal.helper_thread.processing_ext_enabled}"
         print( msg )

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





