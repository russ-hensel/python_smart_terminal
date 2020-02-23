# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 15:42:56 2020

@author: Russ_2

This is a test of the rollover logic used in the arduino progrogram
there is also a spreadsheet for this




>>> f"{new_comedian}"
'Eric Idle is 74.'
>>> f"{new_comedian!r}"
'Eric Idle is 74. Surprise!'


You can use space around = as in f"{name =}" that will expand to f"name ={name}



"""


class RollOver(object):
    def __init__(self):
        """
        the wrong way to instance variables, java like but works
        """
        self.current_clock      = 0
        self.next_event         = 10

        self.CLOCK_ROLLOVER	    = 4294967295
        self.MAX_DELTA_T	    = 500000
        self.MAX_TIME_AHEAD	    = 1000
        self.ROLLOVER_AT	    = self.CLOCK_ROLLOVER - self.MAX_DELTA_T
        self.just_to_be_sure    = 100
        self.ADJ_TIME	        = (  self.CLOCK_ROLLOVER -   self.ROLLOVER_AT +
                                      self.MAX_TIME_AHEAD  + self.just_to_be_sure  )              # 501100

    def str_consts(self):
          """
          """
          a_str      =     f"#define CLOCK_ROLLOVER   = {self.CLOCK_ROLLOVER}"
          a_str      +=  f"\n#define MAX_DELTA_T      = {self.MAX_DELTA_T}"
          a_str      +=  f"\n#define MAX_TIME_AHEAD   = {self.MAX_TIME_AHEAD}"
          a_str      +=  f"\n#define ROLLOVER_AT      = {self.ROLLOVER_AT}"
          a_str      +=  f"\n#define ADJ_TIME         = {self.ADJ_TIME}"

          return a_str

    def print_consts(self):
        """
        """
        print( self.str_consts()  )

    def str_vars(self):
        """
        """
        a_str      =     f"self.current_clock = {self.current_clock}"
        a_str      +=  f"\nself.next_event    = {self.next_event}"
        a_str      +=  f"\ndelta               = {self.next_event - self.current_clock }"
#      a_str      +=  f"\nself.MAX_TIME_AHEAD = {self.MAX_TIME_AHEAD}"
#      a_str      +=  f"\nself.ROLLOVER_AT = {self.ROLLOVER_AT}"
#      a_str      +=  f"\nself.ADJ_TIME = {self.ADJ_TIME}"

        return a_str

    def adv_clock( self, delta_t ):
        """
        """
        print( f"\n---------advance clock by {delta_t}")
        self.current_clock   += delta_t
        if self.current_clock > self.ROLLOVER_AT :
           print( ">>>rollover" )
           self.current_clock = ( self.current_clock + self.ADJ_TIME )  %  self.CLOCK_ROLLOVER
           self.next_event    = ( self.next_event    + self.ADJ_TIME )  %  self.CLOCK_ROLLOVER


        msg   = self.str_vars()
        print( msg )

    def steps( self, no_steps, delta_t, ):
        """
        """
        for i in range(0, no_steps):
            self.adv_clock( delta_t )


# seem to show logic and these constants work fine



a_rollover    =   RollOver()

a_rollover.print_consts()
print( a_rollover.str_vars() )

#a_rollover.next_event  = a_rollover.current_clock + 500


a_rollover.current_clock   = a_rollover.ROLLOVER_AT - 1000
a_rollover.next_event      = a_rollover.current_clock + 500
print( a_rollover.str_vars() )

a_rollover.adv_clock( 200 )

a_rollover.steps( 11,  200 )





