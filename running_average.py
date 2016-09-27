# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

# pretty much taken from:
# http://rosettacode.org/wiki/Averages/Simple_moving_average

import sys
from collections import deque

"""
Computes moving or running averages, averages are always floats
"""

class RunningAverage( object ):

    def __init__(self, period):
        """
        construct, set the period
        """
        assert period       == int(period) and period > 0, "Period must be an integer >0"
        self.period         = period
        self.stream         = deque()    # store the data here
        self.reset()

    # ---------------------------------------------
    def __str__(self):
        descr  = "RunningAverage current val " + str( self.value )

        return descr

    # ---------------------------------------------
    def reset( self ):
        """
        resets the average without changing the period
        """
        self.stream.clear()

    # ---------------------------------------------
    def next_val(self, n):
        """
        add a value to moving average and return a smoothed value
        filling the stream still leaves some issues -- but looks
        like the right way to me
        may be issues on where float() is used
        """

        stream = self.stream

        stream.append(n)    # appends on the right

        streamlength = len(stream)
        if streamlength > self.period:
            stream.popleft()
            streamlength -= 1
        if streamlength == 0:
            self.value    =  0
        else:
            #print stream
            #sys.stdout.flush()
            self.value    = sum( stream ) / float( streamlength )
            #print stream
        #print "ra = " +str( self.value )
        #sys.stdout.flush()
        return self.value

    # ---------------------------------------------
    def del_left(self, ):
        """
        delete a value from average and return a smoothed value
        this removes the oldest value
        """
        stream         = self.stream
        streamlength   = len(stream)

        if streamlength > 0:
            stream.popleft()    #
            streamlength -= 1

        if streamlength == 0:
            self.value    =  0
        else:
            #print stream
            #sys.stdout.flush()
            self.value    = sum( stream ) / float( streamlength )
            #print stream
            #print self.value
            #sys.stdout.flush()
        #print self.stream, " ", self.value
        return self.value

# ---------------------------------------------
if __name__ == '__main__':
    """
    test
    """

    for period in [3, 5]:
        print ""
        print ("\nRunningAverage (class based): PERIOD =", period)
        ra = RunningAverage( period )
        for i in range(1,6):
            print ("  Next number = %-2g, ra = %g " % (i, ra.next_val( float(i))) )

        for i in range(5, 0, -1):
            print ("  Next number = %-2g, ra = %g " % (i, ra.next_val( float(i))) )

        print ""
        print "pulse"
        ra = RunningAverage(period)
        for i in [1,1,1,1,1,1,5,5,5,5,5,5,1,1,1,1]:
            print ("  Next number = %-2g, ra = %g " % (i, ra.next_val( float(i))) )

        print ra

# ========================= eof ========================


