# -*- coding: utf-8 -*-


#import sys
import logging
import time
import datetime
import abc_def
import tkinter as Tk

# -------------- local libs ------------------

# sys.path.append( "../rshlib" )
#import moving_average    # or running average in rshlib
#import data_value
#import parameters
from    app_global import AppGlobal

import  smart_terminal


"""
this does the data processing and db actions for the green_house application
unclear how much should come from parameters

length of moving average probably

"""
# ================= Class =======================
#
class DDCProcessing( abc_def.ABCProcessing ):
    """
    extension for DDCProcessing

    """
    # ------------------------------------------
    def __init__( self,    ):
        # call ancestor ??
        # Set some exception infomation
        self.controller         = AppGlobal.controller
        self.parameters         = AppGlobal.parameters
        self.helper_thread      = self.controller.helper_thread
        
        AppGlobal.abc_processing = self

        self.logger             = logging.getLogger( self.controller.logger_id + ".DDCProcessing")

        self.logger.debug( "in class DDCProcessing init" ) # logger not currently used by here

        self.time               = time.time() # set in set_time -- taken as same for all measurements

        self.last_time          = time.time()

        self.minute_delat       = datetime.timedelta( minutes = 1 )

        self.last_datetime      = None
        self.last_minute        = None
        self.button_actions     = None     # set later

        # these are int value for the aruino interface actually divide by 10 and converted to floats
        self.std_acc_minute     =  100
        self.std_speed_minute   =  100

        self.std_acc_hour       = 100
        self.std_speed_hour     = 100

        self.set_wait_time      = 10        # what units




        # ----------------

    # ----------------------------------------
    def add_gui( self, parent, ):  # if this were a class then could access its variables later
        """
        call: gt
        make frame for motor control and return it
        add buttons for different stepping now for unipolar in 3 modes, expand
        """
        self.button_var     = Tk.IntVar()   # must be done after root is created

        ret_frame           = Tk.Frame( parent, width = 600, height=200, bg = self.parameters.bk_color, relief = Tk.RAISED, borderwidth=1 )

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

        self.button_actions      = button_actions  # controls creation and actions of additional buttons

        #color          = "blue"
        a_frame        = Tk.Frame( ret_frame, width = 600, height=200, bg = "gray", relief = Tk.RAISED, borderwidth=1 )

        #a_frame.grid( row = 0, column = 0, sticky = Tk.E + Tk.W + Tk.N  )    # better than pack blow
        #a_frame.pack(  side = Tk.TOP, expand = Tk.YES, ) #fill=Tk.Y ))      # seems to place at middle
        a_frame.pack( side = Tk.LEFT)     # this seems pretty good

        for ix, i_button_action  in  enumerate( self.button_actions ):
            # make button
            a_button = Tk.Button( a_frame, width = 35, height = 3, text = i_button_action.name, wraplength = 100 )
            a_button.bind( "<Button-1>", self.do_button_action )
            # 8 is number of buttons across
            a_row     =  0
            a_col     =  ix

            # print( a_row, a_col )
            a_button.grid(  row = a_row, column = a_col, sticky ='E' + "W" )
            a_frame.grid_columnconfigure( a_col, weight=1 )
            i_button_action.set_button( a_button )

        return ret_frame

    # ----------------------------------------
    def monitor_arduino_loop( self ):
        """
        assumes port opened successfully
        infinite loop
        call: run in ht not controller
        ret: only on failure, probably should be exception
        """
        # typically stat functions with this sort of thing
        helper_thread    = self.controller.helper_thread
        # gui              = self.controller.gui
        # helper_label     = gui.helper_label  no direct access to gui
        #helper_thread.print_info_string( "Starting Arduino Monitoring..." )
        helper_thread.post_to_queue(  "info", None, "Starting Arduino Monitoring..." )    # rec send info
        #helper_thread.release_gui_for( 5 )
        # beware long v response wait a bit here say 10 sec
        helper_thread.sleep_ht_for( 10 )

        while True:
            self.set_time( )
            send_rec_wait  = 10.   # a long time should slow down only if a problem
            rec_data       = helper_thread.send_receive( "a", send_rec_wait  )  # throw except if times out
            ix  = rec_data.find( "ok", 0, len( rec_data ) )
            if ix == -1:
                msg = "failed to find ok got: >>>" + rec_data + "<<<"
                self.logger.error( msg )
                print ( msg  )   # !! use log  print in recive area
                # need to inform gui and probably throw exception !!
                return   False   # probably should be infinite except

            #self.controller.send( "t\n" )
            rec_data       = helper_thread.send_receive( "t", send_rec_wait  )  # throw except if times out
            self.process_temp_line( rec_data )

            rec_data       = helper_thread.send_receive( "h", send_rec_wait  )  # throw except if times out
            self.process_humid_line( rec_data )

            helper_thread.sleep_ht_for( 10. )

    # ----------------------------------------
    def find_and_monitor_arduino( self ):
        """
        call: ht

        """
        # typically start with these 2 lines
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
             self.monitor_arduino_loop()
        else:
             #helper_label.config( text = "arduino not found " )
             #self.controller.gui.show_item( "helper_info", "arduino not found " )
             helper_thread.print_info_string(   "Error: Arduino not found -- looked for " + self.parameters.arduino_version ) # + a_port )
             return


    # -------------------------------------------------
    def polling_ext( self, ):
        print( "polling_ext" )





    # -------------------------------------------------
    def minute_chime( self, a_minute ):  #
        """
        may be called before its time 
        we are only called if a minute has gone by so lets find out which minute use
        this started as doing the dances from the pi but first implement on the arduino and call dance no.
        """
        if self.last_minute == a_minute:
            # no chime
            return
        
        # ferrit out the special cases
        if   ( a_minute == 0 ):
#            self.set_minute_speed_acc( 10, 20 )
#            self.go_to_minute( a_minute )
             self.do_minute_dance( "1" )

        elif   ( a_minute == 13 ):
             self.do_minute_dance( "2" )
#            self.set_minute_speed_acc( 10, 20 )
#            self.go_to_minute( a_minute )

        elif   ( a_minute == 14 ):
            self.do_minute_dance( "3" )


        elif   ( a_minute == 15 ):
            self.do_minute_dance( "4" )
#            self.set_minute_speed_acc( 10, 20 )
#            self.go_to_minute( a_minute )

        else:
            pass
        
        self.set_minute_speed_acc( self.std_speed_minute,  self.std_acc_minute )
        self.go_to_minute( a_minute )

        self.last_minute == a_minute
        
    # -------------------------------------------------
    def set_minute_speed_acc( self, a_speed,  a_acc ):
  
          send_data   = "m0"
          self.helper_thread.send_receive(  send_data, self.set_wait_time  )

          send_data   = "s" + str( a_speed )
          self.helper_thread.send_receive(  send_data, self.set_wait_time  )

          send_data   = "a" + str( a_acc )
          self.helper_thread.send_receive(  send_data, self.set_wait_time  )

    # -------------------------------------------------
    def go_to_minute( a_minute ):
          send_data   = "t" + str( a_minute )
          self.helper_thread.send_receive(  send_data, 20  )

    # -------------------------------------------------
    def do_minute_dance( self, a_dance_string ):
          """
          for better speed make a_dance a string
          """
          send_data   = "m0"
          self.helper_thread.send_receive( self, send_data, self.set_wait_time  )

          send_data   = "d" + a_dance_string
          self.helper_thread.send_receive( self, send_data, 100  )

    # -------------------------------------------------
    def cb_find_and_monitor_arduino( self, a_list ):  #
        """
        call: gt
        """
        # port from gt to ht
        self.controller.post_to_queue( "call", self.find_and_monitor_arduino, (  ) )

    #----------------------------------------------
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

    # -------------------------------------------------
    def cb_test_test_ports( self, ignore ):
        """
        call:  cb in gt, use post if calling ht
        """
        print( "cb_test_test_ports ignore", ignore )
           # self.controller.           helper_thread.test_test_ports(   , (  ) )
        self.controller.post_to_queue( "call", self.controller.helper_thread.find_arduino  , (  ) )
        
    # -------------------------------------------------
    def cb_end_helper( self, ignore ):
        #print( "ignore", ignore )
           # self.controller.           helper_thread.test_test_ports(   , (  ) )
        self.controller.post_to_queue( "call", self.controller.helper_thread.end_helper  , (  ) )

# =================================
class ButtonAction( object ):
    """
    this may become an asbstract class for plug in button actions in the smart terminal, a bit like processing add to the array
    need ref to my processing object probably
    hold info to implement a button in the gui
    looks like a struct so far
    """
    def __init__( self, a_processor, a_name, a_function ):
        self.processor       =  a_processor     # why this it is a mini controller where used?
        self.name            =  a_name
        self.function        =  a_function      # where are the arguments elswhere in the thing in function_args with set_args
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
        maybe make a tuple and use *() when calling to unback
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





