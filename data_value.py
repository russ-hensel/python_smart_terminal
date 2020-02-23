# -*- coding: utf-8 -*-


"""
support for smart_terminal.py helps determine which data points are saved to the database
"""

#import serial
import sys
import time
import moving_average
#import time.test

class DataValue( object ):
    """
    copied from data point, revised for more general use
    holds a datapoint or measurement, pretty much a struct
    plus some processing, more than I expected.
    applies the moving average to the data after parsing
    """

    # ----------------------------------------------------------
    def __init__(self, run_ave_len, max_delta ):
       """
       keeps track of the value of reading including smoothing
       run_ave_len set the value of the period of the running average
       think about how period for moving average and other
       values are initialized
       time is the first time with a valid value for any reading
       !! pass in amount of smoothing
       """
       self.calibrate_function  = self.identity
       self.ave_value           = moving_average.Movingaverage( run_ave_len )
       self.max_delta           = max_delta   # max delta before update
       self.old_value           = 0.
       self.reset()

    # ----------------------------------------------------------
    def reset(self,   ):
       # time no longer used
       # self.time      = None          # many values share time shoule we keep it here ??
       #self.value  = None
       self.invalid_value      = -99    # data values to ignore
       self.ave_value.reset()
       self.value   = None

    # ----------------------------------------------------------
    def identity(self, raw_data  ):
        """
        use as calibrate function, no transform of data
        this is the identity operation, raw data = calibrated data
        plan to use as default for this class
        """
        value = raw_data
        return value

    # ----------------------------------------------------------
    def set_calibrate_function(self, calibrate_function  ):
        """
        setup the calibrate or conversion function

        """
        self.calibrate_function = calibrate_function
        return

    # ----------------------------------------------------------
    def add_value(self, value  ):
        """
        add a measurement to the value we are tracking
        use the calibrate function
        ignore invalid values
        """
        if value != self.invalid_value:
            self.ave_value.nextVal( self.calibrate_function( value ) )
        return self.get_value()

    # ----------------------------------------------------------
    def get_value(self,   ):
        """
        return a tuple, is update needed and what is the value
        nu, val = ....get_value()
        """
        need_update = ( abs( self.old_value  -  self.ave_value.value ) >= self.max_delta )

        return ( need_update, self.ave_value.value )

    # ----------------------------------------------------------
    def saved_value(self,   ):
        """
        record that the value has been saved so old value is updated
        """
        self.old_value  =  self.ave_value.value
        return self.ave_value.value

    # ----------------------------------------------------------
    def __str__(self):
       """
       for string representation,
       not very complete, has drifted out of date
       """
       #descr  = "Data Value time: " + str( self.time ) + "  data value:  " + str( self.ave_value.value )
       descr  = "Data value:  " + str( self.ave_value.value )

       return descr

    # ----------------------------------------------------------
    def printt( self ):
        print( self.__str__() )

# ----------------------------------------------------------

# ----------------------------------------------------------
def double( value  ):

    pass
    #print "double it"
    return 2. * value

if __name__ == '__main__':
        """
        little test
        """

        test = DataValue( 5, .5 )

        test.set_calibrate_function(  double_it )

        test.add_value( 1. )
        print( test.get_value() )

        test.saved_value()

        test.add_value( 1. )
        print( test.get_value() )

        test.add_value( 1. )
        print( test.get_value() )

        test.add_value( 2. )
        print( test.get_value() )

        test.add_value( 2. )
        print( test.get_value() )

        test.add_value( 2. )
        print( test.get_value() )

        test.saved_value()
        print( test.get_value() )

#        test.parse( "pa 81"        )
#        test.parse( "pa     82"   )
#
#
#        test.parse( "pa     83 "   )
#        test.parse( "pa84 "   )
#        print( "test: all done"  )


# ======================= eof ======================================

