# -*- coding: utf-8 -*-

#import serial
import sys
import time
import moving_average
#import time.test

class DataPoint( object ):
    """
    holds a datapoint or measurement, pretty much a struct
    plus some processing, more than I expected.
    applies the moving average to the data after parsing
    """

    # ----------------------------------------------------------
    def __init__(self, run_ave_len  ):
       """
       keeps track of the value of reading including smoothing
       run_ave_len set the value of the period of the running average 
       think about how period for moving average and other
       values are initialized
       time is the first time with a valid value for any reading
       !! pass in amount of smoothing
       """

       self.ave_pressure  = moving_average.Movingaverage( run_ave_len )

       self.reset()

    # ----------------------------------------------------------
    def reset(self,   ):

       self.time      = None
       #self.pressure  = None
       self.ave_pressure.reset()
       self.pressure   = None

    # ----------------------------------------------------------
    def __str__(self):
       """
       for string representation, 
       """
       descr  = "Data Point time: " + str( self.time ) + "  pressure:  " + str( self.ave_pressure.value )

       return descr

    # ----------------------------------------------------------
    def parse_test( self, sdata, stime ):
        """
        time passed in as string for testing
        """
        self.parse( sdata )
        self.time            = float( stime )

    # ----------------------------------------------------------
    def parse( self, sdata ):
       """
       parse out a string and add the data
       string like:  "pa 122"
       and apply running average.
       store result in self.time and .... all part of DataPoint
       return type of data found??? no
       return data point complete??? no
       any failure return -1 else return 1
       is it ok to overwrite data
       time is constantly updated.
       """

       sdatas = sdata.split()
       print sdatas
       sys.stdout.flush()

       if len( sdatas ) < 2:
           print "parse len < 2"
           return -1

       if sdatas[0] != "pa":
           print "parse not pa"
           return -1

       try:
           pressa = float( sdatas[1].strip() )
       except:
           print "parse not float exception  ", sdatas[1].strip()
           return -1

       self.time      = time.time()

       self.pressure  = self.ave_pressure.nextVal( pressa )
       return 1

    # ----------------------------------------------------------
    def printt( self ):
        print( self.__str__() )

# ----------------------------------------------------------
if __name__ == '__main__':
        """
        test 
        """

        test = DataPoint( 5 )
        
        test.parse( "pa 81"        )
        test.parse( "pa     82"   )
        
        
        test.parse( "pa     83 "   )
        test.parse( "pa84 "   )
        print( "test: all done"  )


# ======================= eof ======================================
