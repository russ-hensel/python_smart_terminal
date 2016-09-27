# -*- coding: utf-8 -*-


import sys
import logging
import time

# -------------- local libs ------------------

#sys.path.append( "../rshlib" )
import moving_average    # or running average in rshlib
import data_value
import parameters
import data_value

"""
this does the data processing and db actions for the green_house application
unclear how much should come from parameters

length of moving average probably

"""
# ================= Class =======================
#
class GHProcessing( object ):
    """

    """

    # ------------------------------------------
    def __init__( self,  controller  ):
        # call ancestor ??
        # Set some exception infomation
        # currently pretty much a test
        self.controller    = controller
        self.parameters    = controller.parameters
        self.logger        = logging.getLogger( self.controller.logger_id + ".GHProcessing")

        self.logger.debug("in class GHProcessing init") # logger not currently used by here

        self.time          = time.time() # set in set_time -- taken as same for all measurements

        #self.last_time     = None
        self.last_time     = time.time()

        self.min_delta_t   = self.parameters.db_min_delta_time    # in seconds
        self.max_delta_t   = self.parameters.db_max_delta_time   # in seconds  save if this period of time goes by

        # not in parameters because not so easily changed
        self.no_temps      = 2
        self.no_humids     = 2
        self.no_lights     = 1
        self.no_doors      = 4

        # ----------------
        temp_run_len       = self.parameters.db_temp_len
        temp_delta         = self.parameters.db_delat_temp
        self.dv_temps      = []     # list, data_values of temps
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

        ok, values   = self.parse( line, "" )

        if not ok:
            self.logger.error("error in parse return value for temp >>>" + line + "<<<" )
            return    # NEED better handling here
        #else:
            #return

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

        ok, values   = self.parse( line, "" )
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

        db_sql       = (    "insert into gh_data_2( "
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

    # ----------------------------------------------------------
    def parse( self, line, id ):
       """
       parse out a string and with data
       string like:  "pa 122 592"
       first part is id, can be none?
       id not yet supported

       old::::::
       and apply running average.
       store result in self.time and .... all part of DataPoint
       return type of data found??? no
       return data point complete??? no
       any failure return -1 else return 1
       is it ok to overwrite data
       time is constantly updated.
       """
       ok       = True
       values   = []
       sdatas   = line.split()
       #print sdatas
       #sys.stdout.flush()

#       if len( sdatas ) < 2:
#           print "parse len < 2"
#           return -1

#       if sdatas[0] != id:
#           print "parse not correct id " + id
#           ok   = False
#           return ( ok, values )

       for  ix_sdatas in sdatas:

               try:
                   value = float( ix_sdatas.strip() )
                   values.append( value )
               except:
                   #print "parse not float exception  ", ix_sdatas.strip()
                   self.logger.error( "parse not float exception  " + str( ix_sdatas.strip() ) )
                   values.append( 0. )
                   ok       = False

       return ( ok, values )

# ----------------------------------------------------------

#import test_controller

if __name__ == '__main__':
        """
        test
        this really does not work without a controller or parameters
        can we make one here
        """

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

