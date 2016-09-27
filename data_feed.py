# -*- coding: utf-8 -*-

#import serial
#import sys
import time

class Data_feed( object ):
       """
       probably for testing 
       seems to be imbedded in db_test.py
       for feeding a bit at a time -- this may or may not be too simple to implement
       will fail on 0 len file.
       """
       
       def __init__(self, file_name   ):
           
         with open( file_name ) as f:
             self.lines = f.readlines()
             
         #print self.lines    
         self.ix_max = len( self.lines )
         self.ix = 0
         
         # timetest   = TimeTest()
         print( "Data_feed: warning in test mode time is not really time.time " )  # might do better here 
           
           
       def next_feed( self,  ):
           """
           make this circular  
           """
           
           retval  = self.lines[ self.ix ]
           self.ix  += 1
           if self.ix >= self.ix_max:
               self.ix = 0
           return retval
           
           
           
           
      