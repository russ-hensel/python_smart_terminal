# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

#
#
# ToDo  * removed when done
#     Copied from mcuterminal, perhaps update from there time to time ( aug 2015 )
#     * add some sort of timed tasks unless I have another thread probably needs to be in time
#         perhaps should make a class, but will just embed now.
#         was going to hardcode but base on a list
#       * start with connect and version
#

import  importlib
import sys
sys.path.append( "../rshlib" )
#sys.path.append( "./" )
#sys.path.append( "D:/Russ/0000/SpyderP/rshlib" )
#sys.path.append( "D:/Russ/0000/SpyderP/" )
#sys.path.append( r"D:\Russ\0000\SpyderP\rshlib" )
print sys.path
#from   ..rshlib import logger
import logger
from   Tkinter import *
#import logger

import parameters
import gui
import os
#from   time import sleep
#from   time import time
import time

import db

# sys.path.append( "../irtools" )
# import irtools

#import MCUTerminal.rs232driver1

#Fimport pandas as pd
#import gui2
#import gui_three
#import arduinodriveremu
import  importlib
import  graphing


class TaskList:
    """
    may or may not be a list, will do that for now
    let controller push in the tasks?
    each entry is a tuple times will be in seconds
        time_start    from last task 0 if we just go right on to it
        delta_time    for repeating tasks
        repeats       0 for infinite -- should be final task
        taskname      probably calls a subroutine might even be it
                      these may need states as well so also classes
                      but first try as micro tasks, with soome sort of goback feature
        # how to make sure we are not called while updating????

    """
    
    def __init__(self, controller ):
        """
        """

        self.controller   = controller
        self.start_time   = time.time()   #  start for each one
        #self.send_complete = False
        #self.rec_complete  = False
        self.auto_on      = False
        #self.ix           = 0     # or -1
        self.tasks        = []
        self.done_rec     = False
        self.done_trans   = False
        # self.tasks[ self.ix ]  unpack or index into parts, put in own variable ?
        # add a time out
        # all take type, data


        # see docstring above for meaning of items in tuple
        #self.tasks.append( ( 5, 1, 1, self.controller.close_task() )   )  # close the comm port
        self.tasks.append( ( 5,  1, 1, self.controller.open_task )   )  # open the comm port
        self.tasks.append( ( 5, 5, 0, self.controller.version_task )   )  # close the comm port
        #self.tasks.append( ( 5, 1, 1, self.controller.close_task )   )  # close the comm port


        #self.tasks.append( ( 5, 1, 1, self.controller.verify_version() )   )  # ask for version and confirm

        #self.tasks.append( ( 5, 5, 0, self.controller.read_loop_task() )   )  # open the comm port

# the components for testing     
    def test_task(  self ):
        print "test_task"
        pass
        return
        
    def init_test_task():
        print "init_test_task"
        pass
        return

    def start_auto( self, ):
        """
        use from a cold start will start from
        first task, better to name start_auto ??
        """
        
        # set up as if we are finishing the -1 task
        self.repeats_ix   = 1      # counts down to 0 unless self.repeats is itself 0
        self.repeats      = 1
        self.ix_task      = -1     # because willi ndex up by one on firs call
        self.next_auto()
        # self.tasks        = [] presumed setup up could be passed in


    def next_auto( self, ):
        """
        """
        
        self.controller.myLogger.log( "next auto", None )
        # next implements repeats at period by time delta instead of time.next -- why ?
        self.repeats_ix   -= 1      # working to 0

        if  self.repeats   == 0:
            # repeat forever, act as if we were at the prior task then adance
            #self.ix_task      -= 1
            pass
        elif self.repeats_ix != 0:
            # back up a task then advance
            #self.ix_task      -= 1
            pass
        else:
            self.ix_task     += 1

        if self.ix_task >= len( self.tasks ) :
            self.controller.myLogger.log( "done; next auto set false ", None )
            self.auto_on     = False
            return

        self.done_rec     = False
        self.done_trans   = False
        self.time_next, self.time_delta, new_repeats, self.task_routine = self.tasks[ self.ix_task ]

        # now manage repeating agin
        if self.repeats_ix == 0:

            self.repeats      = new_repeats
            self.repeats_ix   = self.repeats  # or perhaps -1 depending on increment

        self.start_time   = time.time()    # next event time_delta later then reset this
        self.controller.myLogger.log( "next auto times " + str( self.start_time  ) + " " + str( self.time_next )  , None )
        self.auto_on      = True
        # how to make sure we are not called while updating????


        # self.tasks[ self.ix ]  unpack or index into parts, put in own variable ?
        """
        .close_task( send_or_rec )   ok to do in task
        if ( send_or_rec == "t" ) and ( not self.done_trans ):   # assume s first
             pass
             self.done_trans = True
        else  self.done_trans ( )
             pass
             self.done_rec  = True

        if self.done_rec and self.done_trans :
             if self.start_time +


        """
        
        
    def  do_task( self, trans_rec, tr_data ):
                """
                note early return
                """
                
                #what about the wating
                 #.close_task( send_or_rec )   ok to do in task
                #self.controller.myLogger.log( "self.start_time  " + str( self.start_time ), None )
                #self.controller.myLogger.log( "self.time_next  " + str( self.time_next ), None )

                if ( self.start_time + self.time_next ) >= time.time():
                    # self.controller.myLogger.log( "not time", None )
                    return

                if self.done_rec and self.done_trans :
                     # no repeats for now
                     self.next_auto()
                     return

                #self.controller.myLogger.log( "do task times " + str( self.start_time  ) + " " + str(  self.time_next  ) + " "
                #               + str( time.time() ) , None )
                if ( trans_rec == "t" ) and ( not self.done_trans ):   # assume s first
                     #pass
                     # may need to fix for data none
                     self.done_trans = self.task_routine( "t", "not used" ) # probably always a True
                     return
                #print "xxx"

                elif  ( trans_rec == "r" ) and self.done_trans and ( not self.done_rec ):  # transmit first if don_trans false how did we get here error !!!
                #elif  ( trans_rec == "r" ):
                     #pass
                     #print "xxx"

                     self.done_rec  = self.task_routine( "r", tr_data ) # probably always a True if there is data
                     # no return
                     
                     


class TestGui:
    def __init__(self,   ):

        self.myName         = " TestGui"
        self.version        = "2015 Oct 3.1"

        self.myParameters   = parameters.Parameters( self ) # open early may effect other

        # module and class name for the communications driver.
        self.comm_mod       = self.myParameters.comm_mod
        self.comm_class     = self.myParameters.comm_class

        self.myLogger       = logger.Logger( self )
        self.myLogger.open()  # later should get file from parameters??

        self.db             = db.DBAccess( self )
        self.graphDB        = graphing.GraphDB( self )
        
         # graphing.py GraphDB()

        self.looping        = False   # for our looping operations
        #self.task_list      = TaskList( self )

        self.prog_info()

        #self.myDriver       = arduinodriveremu.ArduinoDriverEmu( self )
        # actually create the communications driver.
        #sys.path.append( "../MCUTerminal" )
        #sys.path.insert(0, "../MCUTerminal" )
        self.myDriver       =  self.create_comm_class( self.myParameters.comm_mod, self.myParameters.comm_class )

        self.win       = Tk()    # this is the tkinter root for the GUI

        self.win.title( "TestGui  version: " + self.version )
        self.myGui     = gui.GUI( self, self.win,  [] )  # create the gui or view part of the program
        #self.myGui     = gui2.GUI2( self, self.win )  # create the gui or view part of the program
        #self.myGui     = gui_three.GUIThree( self, self.win )  # create the gui or view part of the program

        self.win.geometry( self.myParameters.win_geometry )    # ??move to parameters

        self.win.taskDelta     = self.myParameters.poll_delta_t  # in ms

        self.loop_period       = self.myParameters.loop_period
        self.loop_ix           = 0    # counter down in task

        self.win.after( self.win.taskDelta, self.task )   # have to kick off gui task the first time
        self.task_tick   = 0        # tick in task
        self.array_send  = False

        # should kick off auto


        # --------------------------------------------------------
        #print "about to start mainloop"
        self.win.mainloop()
        # print " init and we are all over....  "
        return


    def prog_info( self ):
        """
        log info about program and its argument/enviroment
        nice to have system time and date
        """

        self.logit( "" )
        self.logit( "============================" )
        self.logit( "" )

        self.logit( "Running " + self.myName + " version = " + self.version  )
        self.logit( "" )
        #  data_dir=russ_data  graph_type=graph_tot
        if len( sys.argv ) == 0:
            logit( "no command line arg " )
        else:
            ix_arg = 0
            for aArg in  sys.argv:

                self.logit( "command line arg " + str( ix_arg ) + " = " + sys.argv[ix_arg])
                ix_arg += 1

        self.logit( "current directory " +  os.getcwd() )
        return
        

    def create_comm_class( self, module_name, class_name):
        """
        this will load a driver from string names
        so that parameter file can specify dirver, often
        to change comm protocols.
        """
        self.logit( "create com class"  )

        self.logit( module_name  )

        self.logit(  class_name )

        #module = __import__(module_name)

        #self.logit(  str( module )  )


        #my_class = getattr( module, class_name )
        #instance = my_class( self )
        #print instance, instance.getName()

        #path = "importtest1.modulejoe.Joe"
        #module_name, class_name = path.rsplit(".", 1)
        print module_name
        print class_name
        MyClass = getattr(importlib.import_module(module_name), class_name)
        instance = MyClass( self )

        return instance


    def task( self, ):
            """
            polling task runs continually in the GUI
            reciving data is an important task.
            polling frequency set via taskDelta, ultimately in parameters
            """
            #print "tick"
            self.task_tick  += 1    # left over from ir, we have two sub tasks, why not reset counter
                                    # to 0 have one for each subtask is several

#==============================================================================
#             if self.task_list.auto_on:
#                     self.task_list.do_task( "t", "ignored" )
# 
#==============================================================================
            data   = self.recieve(  )

#==============================================================================
#             if self.task_list.auto_on:
#                     self.task_list.do_task( "r", data )   # argument for the data or reach into controller?
# 
#==============================================================================

            # need to stick recieved data in a list for processing by the main loop

            if self.array_send:
                #self.logit( str( self.task_tick  %  self.myParameters.send_array_mod )  )
                if ( ( self.task_tick % self.myParameters.send_array_mod ) == 0 ):  # 5 might be in parms
                        #---
                        #print "send ix_array", self.array_ix


                        #self.send( "xxx\n" )
                        self.send( "a"+ str(  self.ir_signal[ self.array_ix ] ) + "\n" )

                        self.array_ix  += 1
                        if ( self.array_ix  >= len( self.ir_signal ) ):
                            self.array_send  = False

            if self.looping:     #looping add a repeating transmit over and over

                self.loop_ix    += 1
                print self.loop_ix
                if self.loop_ix  > self.loop_period:
                    self.loop_ix = 0
                    sdata   = self.myParameters.loop_text

                    self.myDriver.send( sdata )
                    self.myGui.printToSendArea(  sdata )
                    
                    self.test_task( )                    
                    
                    
                    
                    
                    pass

            self.win.after( self.win.taskDelta, self.task)  # reschedule event
            return

    #==================== tasks =============
    def open_task( self, trans_rec, tr_data ):
        """
        ! post activity to terminal area
        """
        # how about repeat or fail, maybe tasks should have more returns or state

        if ( trans_rec == "t" ):
              self.myLogger.log( "open_task t", 1 )
              self.myGui.showRecFrame( "Open port: \n" )
              self.openDriver(  )
              return True
        else:  # recieve activity
              self.myLogger.log( "open_task r ", 1 )
              return True

    #==================== tasks =============
    def close_task( self, trans_rec, rec_data ):
        """
        ! post activity to terminal area
        """
        # how about repeat or fail, maybe tasks should have more returns or state

        if ( trans_rec == "t" ):
              self.myLogger.log( "close_task t", 1 )
              self.myGui.showRecFrame( "Open port: \n" )
              self.closeDriver(  )
              return True
        else:  # recieve activity
              self.myLogger.log( "close_task r " + rec_data, 1 )
              return True


    #-------------------------------------------
    def version_task( self, trans_rec, rec_data ):
        """
        ! post activity to terminal area
        """
        # how about repeat or fail, maybe tasks should have more returns or state
        #self.myLogger.log( "version_task", 1 )
        if ( trans_rec == "t" ):
              self.myLogger.log( "version_task t " + rec_data, 1 )
              self.myGui.showRecFrame( "Check Version: \n" )
              self.send( "v\n" )
              return True
        else:  # rec activity
              # looking for "WellMonitor"
              self.myLogger.log( "version_task r " + str( rec_data ), 1 )
              if rec_data is None:
                   return False

              ix  = rec_data.find( "WellMonitor", 0, len(rec_data) )


              self.myLogger.log( "version_task r " + rec_data, 1 )
              if ix != -1:
                  self.myGui.showRecFrame( "Version good: \n" )
                  return True
              else:
                  #self.myGui.showRecFrame( "Version not so good: \n" )
                  return False


    #==================== end tasks =============

    def openDriver( self ):
        """
        open the comm driver
        updates gui but does not keep status
        status probably availible in driver
        """

        val   = self.myDriver.open()
        if val:
            status = "Open"
            #self.myLogger.log( "opened ok", "ignored" )
        else:
            status = "Open Failed"
            #self.myLogger.log( "open failed",  "ignored" )

        self.myGui.setOpen( status )

        return


    def closeDriver( self ):

        #self.myLogger.log( "controller says close", "ignored" )

        self.myDriver.close()
        self.myGui.setOpen( "Closed" )

        return


    def send( self, adata ):
         """
         is this where crlf is fixed up, think in gui now -- which is wrong place
         add block on port closed
         """
         if self.myParameters.echoSend:
            self.myGui.printToSendArea( adata )

         self.myDriver.send( adata )
         return


    def recieve( self,  ):   # combine with task?
        """
        recieve only full strings ending with /n else
        accumulated in the driver /n is stripped
        """
        # for 232: breaks simulator

        data   = self.myDriver.getRecString( )
        if data == "":
             pass
        else:
             #self.myGui.showRecFrame( "# <<<" + data )
             self.myGui.showRecFrame( "# <<<" + data + "\n" )
        return data


    def sendArray( self, irlist ):
        """
        send arduino commands to load a new array of signals
        """
        # for now hardcode as ir array
        # reset array -- may need to define foo

        # ir signal recieved had following Low High microsecond values
        #         foo( [ 0, 160, 920, 160, 1740, 160,   780 ] )



        # this is the echo, but not the report which is above
        #               180  920  160  1740  160  780    160  2840

        # --- this needs to be moved to task some set up here then on there

        self.logit( "turn on send array"  )
        self.array_ix   = 0

        #self.ir_signal  = [ 180, 920, 160, 1740, 160, 780,   160, 2840, 160, 1320, 160, 1340, 160, ] # 1180, 160, 2700, 160, 12780, 200, 920,   \
                           #160, 2680, 160, 780, 160, 800, 160, 780, 160, 920, 160, 800, 140, 800,   \
                           #  160 ]
        self.ir_signal  = irlist
        self.myDriver.send( "z\n" )
        self.array_send = True    # if we were mult-threaded this would have to be here

        return


    def addDB( self,  ):
        """
        this is a test for now
        """
        self.db.dbAddRow( time.time(), 50., 1 )
        self.myLogger.log( "did db update did it work?", 1 )
        return
        
        
    def graph( self,  ):
        """
        this is a test for now - does simple graph
        """
        # graphing.py GraphDB()
        #self.myLogger.log( "need graphing to be implemented start new class", 1 )
        
        self.graphDB.testGraph()     
        
        return        


    def ports( self,  ):
         """
         probe for ports, not finished
         post to recieve area, save???
         """

         ports   = self.myDriver.listAvailable()
         self.myGui.showRecFrame( "Reported Ports: \n" )

         for aport in ports:
             self.myGui.showRecFrame( aport[0] )
             self.myGui.showRecFrame( "\n" )


    def logit( self, adata ):
        """
        for compatability with old code
        # self.logit( str( self.task_tick )  )   # self.logit( "msg"  )
        """
        self.log( adata, "logit" )
        return


    def log( self, adata, ato ):
        """
        just a call to logger
        is this needed/used, can component
        call directly?

        """
        self.myLogger.log( adata, ato )
        return


if __name__ == '__main__':

        irList   = []

        aApp = TestGui(  )
        # clean up, might be nice to get up into the app
        aApp.myDriver.close()
        aApp.db.dbClose()
        
        aApp.logit( aApp.myName + ": all done" )
        aApp.myLogger.close()
        


