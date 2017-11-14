# -*- coding: utf-8 -*-


#import sys
import logging
import time
#import abc
import abc_def
import tkinter as Tk


# -------------- local libs ------------------

# sys.path.append( "../rshlib" )
#import moving_average    # or running average in rshlib
import  data_value
import  smart_terminal
from    app_global import AppGlobal

"""
this does the data processing and db actions for the green_house application

"""
# ================= Class =======================
#
class GHProcessing( abc_def.ABCProcessing ):
    """
    extension for green house monitor
    self.mode              = "GreenHouse"  in parameters
    """
    # ------------------------------------------
    #def __init__( self,  controller  ):
    def __init__( self,    ):    
        # call ancestor ??
        # Set some exception infomation
        #self.controller    = controller
        self.controller             = AppGlobal.controller
        self.parameters             = self.controller.parameters
        self.helper_thread          = self.controller.helper_thread
        
        AppGlobal.abc_processing   = self
        
        self.logger                 = logging.getLogger( self.controller.logger_id + ".GHProcessing")

        self.logger.debug( "in class GHProcessing init" ) # logger not currently used by here

        self.time          = time.time() # set in set_time -- taken as same for all measurements

        self.last_time     = time.time()

        self.min_delta_t   = self.parameters.db_min_delta_time    # in seconds
        self.max_delta_t   = self.parameters.db_max_delta_time   # in seconds  save if this period of time goes by

        # number of data points not in parameters because not so easily changed
        self.no_temps       = 2
        self.no_humids      = 2
        self.no_lights      = 1
        self.no_doors       = 4

        self.button_actions = None     # set later

        # ----------------
        temp_run_len       = self.parameters.db_temp_len
        temp_delta         = self.parameters.db_delat_temp
        self.dv_temps      = []     # list = data_values of temperatures
        for ix in range( self.no_temps ):
            self.dv_temps.append(  data_value.DataValue( temp_run_len, temp_delta ) )

        # ----------------
        self.dv_humids      = []     # list, data_values  self.dv_humids
        for ix in range( self.no_humids ):
            self.dv_humids.append(  data_value.DataValue( self.parameters.db_humid_len, self.parameters.db_humid_delta ) )

        # ----------------
        self.dv_lights      = []     # list, data_values
        for ix in range( self.no_lights ):
            self.dv_lights.append(  data_value.DataValue( self.parameters.db_light_len, self.parameters.db_light_delta ) )

        # ----------------
        self.dv_doors      = []     # list, data_values
        for ix in range( self.no_doors ):
            self.dv_doors.append(  data_value.DataValue( self.parameters.db_door_len, self.parameters.db_door_delta ) )

    # ----------------------------------------
    def get_auto_by_name( self, a_name ):
        # an idea, try eval instead.

        pass
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
    # -------------------------------------------------
    def polling_ext( self, ):
        #print( "polling_ext" )
        pass

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
        move to the smart_terminal_helper to make more generally available -- does everyone have this thread 
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

    # ------------------------------------------
    def set_time( self,  ):
        """
        std set
        set the aquisition time of the data
        when is this ever called or updated ?? !!  perhaps aquire data
        """
        self.time    = time.time()

    # ------------------------------------------
    def process_temp_line( self,  line  ):
        """
        process a line containing temperature values
        how to handle failure??
        note call to save data, in process... after last data item is read
        !! improve error management
        """
        #print "process temp line"
        #self.logger.debug( "process_temp_line " + line )

        ok, values   = self.helper_thread.parse_out_floats( line, )

        if not ok:
            self.logger.error("error in parse return value for temp >>>" + line + "<<<" )
            return    # NEED better handling here

        if len( values ) != self.no_temps :
            self.logger.error("error in parse len of values for temp : " + str( len( values )) + " >>>" + line + "<<<" )
            return

        for ix_value, i_value in enumerate( values ):
            self.dv_temps[ix_value].add_value( i_value  )

    # ------------------------------------------
    def process_humid_line( self,  line  ):
        """
        repeat stuff from temp, humit......
        """
        #print "process humid line"
        # self.logger.debug( "process_humid_line " + line )

        ok, values   = self.helper_thread.parse_out_floats( line, )
        #print values

        if not ok:
            self.logger.error( "error in parse return value for humid" + line + "<<<" )
            return    # NEED better handling here

        if len( values ) != self.no_temps :
            self.logger.error("error in parse len of values for humid: " + str( len( values )) + " >>>" + line + "<<<" )
            return

        for ix_value, i_value in enumerate( values ):
            self.dv_humids[ix_value].add_value( i_value  )

        self.save_data()    # best call after the last item of data is acquired, or as part of next acquire

    # ------------------------------------------
    def process_light_line( self,  line  ):
        """
        repeat stuff from temp, humit......
        """
        #self.logger.debug( "process_light_line " + line )
        pass   # enough for testing temp

    # ------------------------------------------
    def process_door_line( self,  line  ):
        """
        repeat stuff from temp, humit......
        """
        #self.logger.debug( "process_door_line " + line )
        pass   # enough for testing temp

    # ------------------------------------------
    def save_data( self,    ):
        """
        when is this called?, try after last data measurement
        data
             0    timestamp
                  temp 1
                  temp 2
                  humid 1
                  humid 2
                  light
                  door 1
                  door 2
                  door 3
                  door 4
        determine if save is required and if so do it else not
        note early return
        !! want some error checking
        return nothing??
        """
        if  not ( self.need_update() ):
            #self.logger.info( "no update needed" )
            return

        #log_msg  = "dbAddRow "   #print( log_msg )
        #self.logger.debug( log_msg )

        db_sql       = (    "insert into env_data_table_1( "
                            "gh_time, "
                            "temp_1, temp_2, "
                            "humid_1, humid_2, "
                            "light, "
                            " door_1,  door_2, door_3, door_4 "
                            " ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
                            )

        # ---------- get data ------------
        # init and time

        db_data_list    = []
        db_data_list.append( self.time )

        # temp
        for i_value in self.dv_temps:
            nu, val = i_value.get_value()
            db_data_list.append( val )

        # humid
        for i_value in self.dv_humids:
            nu, val = i_value.get_value()
            db_data_list.append( val )

        # light
        db_data_list.append( 0. )

        # doors
        db_data_list.append( 0 )
        db_data_list.append( 0 )
        db_data_list.append( 0 )
        db_data_list.append( 0 )
        #  check length
        if len( db_data_list ) != 10:
            self.logger.error("error in len( db_data_list )" + str( len( db_data_list )))

        # finish
        db_data       = ( db_data_list[0], db_data_list[1],
                          db_data_list[2], db_data_list[3],
                          db_data_list[4], db_data_list[5],
                          db_data_list[6], db_data_list[7],
                          db_data_list[8], db_data_list[9],

                          )

        cursor        =  self.controller.db.db_connection.cursor()
        cursor.execute( db_sql, db_data )
        # self.logger.info( "cursor.executed" )

        self.controller.db.db_connection.commit()

        self.logger.debug( "db saved at" + str( self.time ) + " " + str( db_data_list ) )

        self.record_saved(  )  # update times in data points

    # ------------------------------------------
    def need_update( self,    ):
        """
        return True if update needed ( or code as to why? )
        determine if update is needed
        # maintain for each type of measure
        """
        # if less than min time skip it
        # if past max time just do it
        delta = self.time  -  self.last_time

        if delta <  self.min_delta_t:
            self.logger.info( "no need delta time update: " + str(   delta  ) )
            return False

        if delta >  self.max_delta_t:
            self.logger.info( "need delta time update: " + str(self.max_delta_t) )
            return True

        # look at deltas for all values
        need_it  = False

        # combine into one list or make list of lists
        for i_dv in self.dv_temps:
            ni, val = i_dv.get_value()
            if ni:
                self.logger.debug( "need temp. update" )
                need_it = True # or use logicical or

        # do same for other measurements

        for i_dv in self.dv_humids:
            ni, val = i_dv.get_value()
            if ni:
                self.logger.debug( "need humid. update" )
                need_it = True # or use logical or

        return need_it

    # ------------------------------------------
    def record_saved( self,    ):
        """
        record that record was saved and at what time
        """
        self.last_time     = self.time
        # update last values

        for i_dv in self.dv_temps:
            i_dv.saved_value()
            #ni, val = i_dv.get_value()

        for i_dv in self.dv_humids:
            i_dv.saved_value()

            #!! finish for other values
    # -------------------------------------------------
    def cb_find_and_monitor_arduino( self, a_list ):  #
        """
        call: gt
        """
        # port from gt to ht
        self.controller.post_to_queue( "call", self.find_and_monitor_arduino, (  ) )

    # -------------------------------------------------
    def do_send_list( self, a_list ):  #
        """
        test for now to make the terminal send a list
        """
        self.controller.do_send_list( a_list )

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
    def do_send_listxxxx( self, a_list ):  #
        """
        test for now to make the terminal send a list  -- may be called an array elsewhere
        """
        self.controller.do_send_list( a_list )
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






#        testC = TestController(  )
#        test  = GHProcessing(  testC )
#
#        test.process_temp_line( "68 78")
#
#        # errors
#        test.process_temp_line( "69 70    71")
#        test.process_temp_line( "22")

#==============================================================================
#         test.parse( "pa 81"        )
#         test.parse( "pa     82"   )
#
#
#         test.parse( "pa     83 "   )
#         test.parse( "pa84 "   )
#==============================================================================
#        print( "test: all done"  )


# ======================= eof ======================================

