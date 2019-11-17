# -*- coding: utf-8 -*-

# hopefully this can work for root cellar and greenhouse just by changing parameters.mode
# maybe at a later date well

#import sys
import logging
import time
#import abc
import abc_def
import tkinter as Tk
import os

# -------------- local libs ------------------

#import moving_average    # or running average in rshlib
import  data_value
import  smart_terminal
from    app_global import AppGlobal

"""


"""
# ================= Class =======================
#
class ProcessingForEnv( abc_def.ABCProcessing ):
    """
    extension for green house monitor and RootCeller -- now extend for WellMonitor
    self.mode              = "GreenHouse"  in parameters
    uses the mode in basically switch statements, probably should have seperate classes in the future
    """
    # ------------------------------------------
    #def __init__( self,  controller  ):
    def __init__( self,    ):
        # call ancestor ??
        # Set some exception infomation
        AppGlobal.abc_processing    = self
        self.controller             = AppGlobal.controller
        self.parameters             = AppGlobal.parameters
        self.helper_thread          = self.controller.helper_thread

        self.logger                 = logging.getLogger( self.controller.logger_id + ".ProcessingForEnv")
        #self.logger                 = logging.getLogger(  self.controller.logger_id + ".helper" )

        self.logger.debug( "in class ProcessingForEnv init" ) #

        self.time          = time.time() # set in set_time -- taken as same for all measurements

        self.last_time     = time.time()

        self.arduino_rep_fail   = 0    # number of time ( perhaps in a row where response from arduino fails )

        self.min_delta_t   = self.parameters.db_min_delta_time    # in seconds
        self.max_delta_t   = self.parameters.db_max_delta_time    # in seconds  save if this period of time goes by

        # number of data points not in parameters because not so easily changed -- but now is, may not work completely
        self.no_temps       = self.parameters.no_temps
        self.no_humids      = self.parameters.no_humids
        self.no_lights      = self.parameters.no_lights
        self.no_doors       = self.parameters.no_doors
        self.no_press       = self.parameters.no_press

        self.get_cpu_temp   = self.parameters.get_cpu_temp

        self.monitor_loop_delay   = self.parameters.monitor_loop_delay   # make even more local in loop function

        self.button_actions = None     # set later

        # ----------------
        self.temp_cpu      = -99  # -99 means no data here
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

        self.dv_press      = []     # list, data_values
        for ix in range( self.no_press ):
            self.dv_press.append(  data_value.DataValue( self.parameters.db_press_len, self.parameters.db_press_delta ) )

        self.logger.debug( "ProcessingForEnv init complete" )

    # ----------------------------------------
    def get_auto_by_name( self, a_name ):
        # an idea, try eval instead.

        pass

    # ----------------------------------------
    def add_gui( self, parent, ):  # if this were a class then could access its variables later
        """
        call: gt
        make frame for extended processing
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

        # -------------------------
        a_button_action         = ButtonAction( self, "Debug:test", self.cb_debug_test )
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
        """
        call ht
        """
        #print( "polling_ext" )
        # may not be using this but just call some other loop ???
        pass

    # ----------------------------------------
    def get_cpu_temp( self ):
        """
        read cpu temp, on windows return signal value for no measurement
        may only be on pi not all linux but go with this for now
        return float
        """

        if self.parameters.os_win:
            temp_f = -99.
        else:
            temp        = os.popen("vcgencmd measure_temp").readline()

            temp_c      = float( temp.replace("temp=","").replace("'C\n", ""))   # cent
            #temp=int( float(getCPUtemperature()) )
            temp_f      = ( ( 9.0/5.0 ) * temp_c ) + 32

        return ( temp_f )

        # ----------------------------------------
    def monitor_arduino_loop_paramaterized( self ):
        """
        should adapt to different measurement thru the parameters in parameters.py
        new sept 2018, may not be tested
        assumes port opened successfully
        infinite loop
        call: run in ht not controller
        ret: only on failure, probably should be exception
        !! times perhaps should be paramaterized
        data not found will end loop is this what we want ??
        """
        # typically stat functions with this sort of thing
        helper_thread    = self.controller.helper_thread

        helper_thread.post_to_queue(  "info", None, "Starting Arduino Monitoring..." )    # rec send info
        #helper_thread.release_gui_for( 5 )
        # beware long v response wait a bit here say 10 sec
        helper_thread.sleep_ht_for( 10 )

        while True:
            # catch and ignore exceptions so we cannot crash out ??
            self.set_time( )
            send_rec_wait  = 10.   # a long time should slow down only if a problem -- may want to move to parameters.p
            self.logger.debug( "monitor_arduino_loop_paramaterized looping" )
            if self.get_cpu_temp:
                self.temp_cpu  = self.get_cpu_temp( )

            rec_data       = helper_thread.send_receive( "a", send_rec_wait  )  # throw except if times out
            ix             = rec_data.find( "ok", 0, len( rec_data ) )
            if ix == -1:
                msg = "failed to find ok got: >>>" + rec_data + "<<<"    # !! or did we time out
                self.logger.error( msg )
                print ( msg  )   # !! use log  print in recive area
                # need to inform gui and probably throw exception !!
                self.arduino_rep_fail   += 1
                if  self.arduino_rep_fail > 3:  # ?? move to parameters.py
                    pass
                    # ask for a restart here
                    self.helper_thread.post_to_queue( "call", self.controller.restart_from_helper, () )

                    return   False   # probably should be infinite except  !! this will kill the loop, no more data
            else:
                self.arduino_rep_fail   = 0

            if self.no_temps > 0:
                rec_data       = helper_thread.send_receive( "t", send_rec_wait  )  # throw except if times out
                self.process_temp_line( rec_data )

            if self.no_humids > 0:
                rec_data       = helper_thread.send_receive( "h", send_rec_wait  )  # throw except if times out
                self.process_humid_line( rec_data )

            if self.no_press > 0:
                rec_data       = helper_thread.send_receive( "p", send_rec_wait  )  # throw except if times out
                self.process_press_line( rec_data )

            msg = "check self.arduino_rep_fail: >>>" + str( self.arduino_rep_fail ) + "<<<"    #
            self.logger.debug( msg )
            if self.arduino_rep_fail   == 0:   # if error in this cycle no save, hope for best in future
                    self.save_data()           # best call after the last item of data is acquired, or as part of next acquire

            helper_thread.sleep_ht_for( self.monitor_loop_delay )


    # ----------------------------------------
    def monitor_arduino_loop( self ):
        """
        assumes port opened successfully
        infinite loop
        call: run in ht not controller
        ret: only on failure, probably should be exception
        !! times perhaps should be paramaterized
        data not found will end loop is this what we want ??
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
            # catch and ignore exceptions so we cannot crash out ??
            self.set_time( )
            send_rec_wait  = 10.   # a long time should slow down only if a problem

            # cpu_temp

            self.temp_cpu  = self.get_cpu_temp( )

            rec_data       = helper_thread.send_receive( "a", send_rec_wait  )  # throw except if times out
            ix             = rec_data.find( "ok", 0, len( rec_data ) )
            if ix == -1:
                msg = "failed to find ok got: >>>" + rec_data + "<<<"    # !! or did we time out
                self.logger.error( msg )
                print ( msg  )   # !! use log  print in recive area
                # need to inform gui and probably throw exception !!
                self.arduino_rep_fail   += 1
                if  self.arduino_rep_fail > 3:  # ?? move to parameters.py
                    pass
                    # ask for a restart here
                    self.helper_thread.post_to_queue( "call", self.controller.restart_from_helper, () )

                    return   False   # probably should be infinite except  !! this will kill the loop, no more data
            else:
                self.arduino_rep_fail   = 0

            #self.controller.send( "t\n" )
            rec_data       = helper_thread.send_receive( "t", send_rec_wait  )  # throw except if times out
            self.process_temp_line( rec_data )

            rec_data       = helper_thread.send_receive( "h", send_rec_wait  )  # throw except if times out
            self.process_humid_line( rec_data )

            if self.arduino_rep_fail   == 0:   # if error in this cycle no save, hope for best in future
                    self.save_data()           # best call after the last item of data is acquired, or as part of next acquire

            helper_thread.sleep_ht_for( self.monitor_loop_delay )

    # ----------------------------------------
    def monitor_arduino_loop_well_monitor( self ):
        """
        !! should be able to put conditions in so use same loop for all apps ??
        assumes port opened successfully
        infinite loop
        call: run in ht not controller
        ret: only on failure, probably should be exception
        !! times perhaps should be paramaterized
        data not found will end loop is this what we want ??
        """

        print( "testing monitor_arduino_loop_paramaterized()!!!!!!!!!!!!!!!!!!!!!" )
        self.monitor_arduino_loop_paramaterized()
        return

        # typically stat functions with this sort of thing
        helper_thread    = self.controller.helper_thread
        # gui              = self.controller.gui
        # helper_label     = gui.helper_label  no direct access to gui
        #helper_thread.print_info_string( "Starting Arduino Monitoring..." )
        helper_thread.post_to_queue(  "info", None, "Starting Arduino Monitoring (Well Monitor)..." )    # rec send info
        #helper_thread.release_gui_for( 5 )
        # beware long v response wait a bit here say 10 sec
        helper_thread.sleep_ht_for( 10 )

        while True:
            # catch and ignore exceptions so we cannot crash out ??
            self.set_time( )
            send_rec_wait  = 10.   # a long time should slow down only if a problem

            # cpu_temp

            self.temp_cpu  = self.get_cpu_temp( )

            rec_data       = helper_thread.send_receive( "a", send_rec_wait  )  # throw except if times out
            ix             = rec_data.find( "ok", 0, len( rec_data ) )
            if ix == -1:
                msg = "failed to find ok got: >>>" + rec_data + "<<<"    # !! or did we time out
                self.logger.error( msg )
                print ( msg  )   # !! use log  print in recive area
                # need to inform gui and probably throw exception !!
                self.arduino_rep_fail   += 1
                if  self.arduino_rep_fail > 3:  # ?? move to parameters.py
                    pass
                    # ask for a restart here
                    self.helper_thread.post_to_queue( "call", self.controller.restart_from_helper, () )

                    return   False   # probably should be infinite except  !! this will kill the loop, no more data
            else:
                self.arduino_rep_fail   = 0

            #self.controller.send( "t\n" )
            rec_data       = helper_thread.send_receive( "p", send_rec_wait  )  # throw except if times out
            self.process_press_line( rec_data )

#            rec_data       = helper_thread.send_receive( "h", send_rec_wait  )  # throw except if times out
#            self.process_humid_line( rec_data )

            if self.arduino_rep_fail   != 0:   # if error in this cycle no save, hope for best in future
                    self.save_data()           # best call after the last item of data is acquired, or as part of next acquire

            helper_thread.sleep_ht_for( self.monitor_loop_delay )

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

        #helper_thread.release_gui_for( 0 )   !! at least log
        if ok:
             #helper_label.config( text = "found arduino on " + a_port )    # helper_thread
             #self.controller.gui.show_item( "helper_info", "found arduino on " + a_port )
             helper_thread.print_info_string(  "found Arduino on " + a_port )

             if self.parameters.mode == "WellMonitor":
                 self.monitor_arduino_loop_well_monitor()
             else:
                 self.monitor_arduino_loop()
        else:
             #helper_label.config( text = "arduino not found " )
             #self.controller.gui.show_item( "helper_info", "arduino not found " )
             msg  = "find_and_monitor_arduino Error: Arduino not found -- looked for " + self.parameters.arduino_version
             self.logger.error( msg )
             helper_thread.print_info_string( msg ) # + a_port )
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
    def process_press_line( self,  line  ):
        """
        process a line containing pressure values
        note call to save data, in process... after last data item is read
        !! improve error management
        """
        #print "process temp line"
        #self.logger.debug( "process_temp_line " + line )

        ok, values   = self.helper_thread.parse_out_floats( line, )

        if not ok:
            self.logger.error( "error in parse return value for pressure >>>" + line + "<<<" )
            return    # NEED better handling here

        if len( values ) != self.no_press :
            self.logger.error( "error in parse len of values for press : " + str( len( values )) + " >>>" + line + "<<<" )
            return

        for ix_value, i_value in enumerate( values ):
            self.dv_press[ix_value].add_value( i_value  )

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
            self.logger.error( "error in parse return value for temp >>>" + line + "<<<" )
            return    # NEED better handling here

        if len( values ) != self.no_temps :
            self.logger.error( "error in parse len of values for temp : " + str( len( values )) + " >>>" + line + "<<<" )
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

        if len( values ) != self.no_humids :
            self.logger.error("error in parse len of values for humid: " + str( len( values )) + " >>>" + line + "<<<" )
            return

        for ix_value, i_value in enumerate( values ):
            self.dv_humids[ix_value].add_value( i_value  )

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
        will save dat if save is required
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

        log_msg  = "in save_data() "   #print( log_msg )
        self.logger.debug( log_msg )

        if  not ( self.need_update() ):
            #self.logger.info( "no update needed" )
            return



        # bad ideas we shoul have some standards even if we have to reload data
        if  self.parameters.mode == "RootCellar":  # may need to expand priro to fix
            self.save_data_for_RootCellar() # later figure out if parameterization is ok
            return

        elif self.parameters.mode == "WellMonitor":  # may need to expand priro to fix
             self.save_data_for_WellMonitor()
             return

        elif self.parameters.mode == "GreenHouse":  # may need to expand priro to fix
             self.save_data_for_GreenHouse()
             return

        else:
            # should log error                               )
            # you are probabbly screwed unless you fix this  perhaps back to greenhouse
            return

    def save_data_for_GreenHouse( self, ):
        """
        Purpose: as in function name
        Return: change in state, inc db
        """

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

        # light-- future enhance
        db_data_list.append( 0. )

        # doors -- future enhance
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
    def save_data_for_RootCellar( self,    ):
        """

        """
        db_sql       = (    "insert into env( "
                                "env_timestamp, "
                                "temp_cpu, "
                                "temp_1, temp_2, temp_3, "
                                "humid_1 "
                                " ) values ( %s, %s, %s, %s, %s, %s  )" # count the %
                                )

        # ---------- get data ------------
        # init and time

        db_data_list    = []
        db_data_list.append( self.time )

        # temp_cpu
        db_data_list.append( self.temp_cpu )

        # temps
        for i_value in self.dv_temps:
            nu, val = i_value.get_value()
            db_data_list.append( val )

        # humid
        for i_value in self.dv_humids:
            nu, val = i_value.get_value()
            db_data_list.append( val )

        # light
        #db_data_list.append( 0. )

        #  check length
        if len( db_data_list ) != 6:
            self.logger.error("error in len( db_data_list )" + str( len( db_data_list )))

        # finish use * something ??
        db_data       = ( db_data_list[0], db_data_list[1],
                          db_data_list[2], db_data_list[3],
                          db_data_list[4], db_data_list[5],
                          )

        cursor        =  self.controller.db.db_connection.cursor()

        lmsg          = ( "sql = " + db_sql + " data: " + str( db_data ) )
        self.logger.debug( lmsg )

        cursor.execute( db_sql, db_data )
        # self.logger.info( "cursor.executed" )

        self.controller.db.db_connection.commit()

        self.logger.debug( "db saved at" + str( self.time ) + " " + str( db_data_list ) )

        self.record_saved(  )  # update times in data points

    # ------------------------------------------
    def save_data_for_WellMonitor( self,    ):
        """

        """
        self.logger.debug( "save_data_for_WellMonitor" )

        db_sql       = (    "insert into well_data( "
                                "timestamp_key, "
                                "temp_cpu, "
                                "pressure_1 "
                                " ) values ( %s, %s, %s )" # count the %
                                )

        # ---------- get data ------------
        # init and time
        db_data_list    = []
        db_data_list.append( self.time )

        # temp_cpu
        db_data_list.append( self.temp_cpu )

        # temps
        for i_value in self.dv_press:
            nu, val = i_value.get_value()
            db_data_list.append( val )


        #  check length
        if len( db_data_list ) != 3:
            self.logger.error("save_data_for_WellMonitor error in len( db_data_list )" + str( len( db_data_list )))

        # finish use * something ??
        db_data       = ( db_data_list[0], db_data_list[1],
                          db_data_list[2],
                        )

        cursor        =  self.controller.db.db_connection.cursor()

        lmsg          = ( "sql = " + db_sql + " data: " + str( db_data ) )
        self.logger.debug( lmsg )

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
        self.logger.debug( "need_update() checking" )
        delta = self.time  -  self.last_time

        if delta <  self.min_delta_t:
            self.logger.debug( "no need delta time update: " + str(   delta  ) )
            return False

        if delta >  self.max_delta_t:
            self.logger.info( "need delta time update: " + str(self.max_delta_t) )   # !! may want to change level
            return True

        # look at deltas for all values
        need_it  = False

        # cpu temp ?

        # combine into one list or make list of lists
        for i_dv in self.dv_temps:
            ni, val = i_dv.get_value()
            if ni:
                self.logger.info( "need temp. update" )
                need_it = True # or use logicical or

        # do same for other measurements

        for i_dv in self.dv_humids:
            ni, val = i_dv.get_value()
            if ni:
                self.logger.info( "need humid. update" )
                need_it = True # or use logical or

        for i_dv in self.dv_press:
            ni, val = i_dv.get_value()
            self.logger.debug( "need_update() checking pressure delta" )
            if ni:
                self.logger.info( "need press. update" )
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

        for i_dv in self.dv_press:
            i_dv.saved_value()

            #!! finish for other values

    # ---------- button call backs
    # -------------------------------------------------
    def cb_find_and_monitor_arduino( self, a_list ):  #
        """
        call: gt
        """
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
    def cb_test_test_ports( self, ignore ):
        """
        call:  cb in gt, use post if calling ht
        """
        print( "cb_test_test_ports ignore", ignore )
           # self.controller.           helper_thread.test_test_ports(   , (  ) )
        self.controller.post_to_queue( "call", self.controller.helper_thread.find_arduino  , (  ) )

    # -------------------------------------------------
    def cb_debug_test( self, ignore ):
        """
        call:  cb in gt, use post if calling ht
        """
        print( "cb_test_test_ports ignore", ignore )
           # self.controller.           helper_thread.test_test_ports(   , (  ) )
        self.controller.post_to_queue( "call", self.controller.ext_processing.monitor_arduino_loop  , (  ) )

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

