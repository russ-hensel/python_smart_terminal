# -*- coding: utf-8 -*-

#
# History/ToDo  ** = when done   !! = planned or considerd ?? = think about
#   Copied from mcuterminal, perhaps update from there time to time ( aug 2015 )
#   ** add some sort of timed tasks unless I have another thread probably needs to be in time
#       perhaps should make a class, but will just embed now.
#       was going to hardcode but base on a list
#       ** start with connect and version tasks
#       ** measure task
#   ?? may be additional stuff in gui.py
#   !! make a lightweight gui
#   ** save data to database
#   ** open log file using popopen and parameter name of some sort
#   *! convert to python logging
#   *! improve doc, structure clean up
#   ** default the send area test
#   ** add place for test buttons
#   *! look at goto for looping have done a task need to coordinate with an arduino prog and a list.
#   !!
#   ** add command line second parm file like in ir terminal
#   !! makd a graphing only app, inc a gui
#   *! auto scroll off on
#   !! detect ports through trial try except, perhaps use the test string as well have list of ports to try
#           look for updates to python look for others code
#   *! continue to clean up prints and logging
#   *! add pylog to gui
#   ?? limit string length as option configure from parameters
#   ** works on PC and Pi

import logging
import Tkinter
import importlib
import sys
import os
import time

# ----------- my code  --------------------------

# ?? check to see if it is already appended?
#sys.path.append( "../rshlib" )

import  db
import  parameters
import  gui
#import  gui_new
#import  graphing
import  data_point
import  gh_processing
import  gh_graphing

# ================= Class =======================
# Define a class is how we crash out
class RSHException( Exception ):
    """
    Define a class to use when we get in big trouble
    inherit from an exception type
    this is how we crash out on major failure
    ?? could use some work
    !! log by itself, stack trace, have one , add except and try to keep going
    !! add global error count? here or in calling code
    """
    # ----------------------------------------
    def __init__(self, arg):
        # call ancestor ??
        # Set some exception information
        # currently pretty much a test
        self.msg = arg

# ================= Class =======================

class TaskVariableObjectIR():
    """
    idea is that this would be an auxiliary object to be passed in
    with some tasks that needed more data, this is one for IR transmission
    maybe, may be something else, perhaps for deer_me ???

    hold a list of ir timings to be sent with task_ir_trans ....

    a task list withing a task list, why not lots of tasks

    """
    # ----------------------------------------
    def __init__(self, ):
        # Set some exception information
        # keep track of where we are we increment on each access, this is how val are chosen

        self.cmd            = "a"  #   add data  -- could be ajusted externally?

        self.datas          = None   # then append data or load external xxx.set_datas()
        # self.max_x       = self.max_x      # 2
        self.ix_datas       = None   # should increment to 0
        self.ix_datas_max   = None   # see set_datas

        #print "self.max_x " + str( self.max_x )   print "self.max_y " + str( self.max_y )
        #sys.stdout.flush()
    # ----------------------------------------
    def set_datas( self, datas ):

        self.datas          = datas
        self.ix_datas       = 0                   # should increment to 0
        self.ix_datas_max   = len( self.datas )   # see set_datas

    # ----------------------------------------
    def get_next_send(self, ):
        """
        cmd  ........ up to next 10 values
        """
        # increment first
        #print "get_next_send( )"
        #sys.stdout.flush()
        # better use a slice

        if  self.ix_datas  >  self.ix_datas_max:
            return ""

        ix_max         = min( self.ix_datas   + 10,  self.ix_datas_max )
        sends          = self.datas[ self.ix_datas:ix_max ]
        self.ix_datas  = ix_max

        s_data         = [ str(i) for i in sends ]

        s              = " "
        data           = s.join( s_data )

        return data


# ================= Class =======================
class TaskVariableObject():
    """
    idea was that this would be an auxilary object to be passed in
    with some tasks that needed more data,
    there is one for IR as well should be super class probably.....
    here a tuple is hardcoded into datas, this is not a great way to do it
    these tuples are for the deer me strobe

    get controller or task list????
    this may be for download used with some particular task
    a task list withing a task list, why not lots of tasks
    """
    def __init__(self, ):
        # Set some exception infomation
        # keep track of where we are we increment on each access, this is how val are chosen

        self.cmds       = "nfr"  #   on, off, repeats

        self.datas      = []  # then append data

        self.datas.append( ( 1, 10, 11 ) )
        self.datas.append( ( 2, 20, 22 ) )
        self.datas.append( ( 3, 30, 33 ) )
        self.datas.append( ( 4, 40, 44 ) )
        self.datas.append( ( 5, 50, 55 ) )

        self.max_x      = len( self.datas[0])  # 2  # all should be the same len
        self.max_y      = len( self.datas )    # like 22

        # self.max_x      = self.max_x      # 2
        self.ix_list_y  = -1  # should increment to 0
        self.ix_list_x  = 4

        #print "self.max_x " + str( self.max_x )   print "self.max_y " + str( self.max_y )
        #sys.stdout.flush()
    # ----------------------------------------
    def get_next_send(self, ):
        """
        n f r
        """
        # increment first
        #print "get_next_send( )"
        #sys.stdout.flush()

        self.ix_list_x  += 1
        if    ( self.ix_list_x  >=  self.max_x ):

             self.ix_list_x  = 0
             self.ix_list_y  += 1
             #print "self.ix_list_x " + str( self.ix_list_x )
             #print "self.ix_list_y " + str( self.ix_list_y )
             #sys.stdout.flush()

             if    ( self.ix_list_y  >=  self.max_y ):
                 # we are done
                 print "get_next_send we are done"
                 sys.stdout.flush()
                 return ""
        # pull together data and return
        data  =  str( self.datas[self.ix_list_y] [self.ix_list_x] )
        # if    self.ix_list_x == 0:
        data = self.cmds[self.ix_list_x] + str( data )   # str could be done on init or elsewhere for more eff.

        #print "data " + data
        #sys.stdout.flush()
        return data

# =========================== Class ATask =================================
class ATask:
    """
    Items for entry into a TaskList
    pretty much a struct
    items are mostly functions or times
    added a TVO and msg
    """
    def __init__(self, task_list, task_trans,    task_rec,
                                  task_special,  task_time_error,
                                  repeats,
                                  time_start,   time_delta, time_error   ):
        """
        initializes the values, later access with dot notation
        4 functions, transmit, receive, time error, special function
        3 times
        1 count  how many times task repeats
        more details below
        """
        self.task_list             = task_list            # list i am added to
        #self.task_function         = task_function       # function i preform
        self.task_rec              = task_rec             # receive function
        self.task_trans            = task_trans           # transmit function
        self.time_start            = time_start           # time in seconds I delay after added to queque
        self.time_delta            = time_delta           # time in seconds delay befor I run again
        self.time_error            = time_error           # time in seconds after starting ( + start time ) before calling error function
        self.task_time_error       = task_time_error      # function called when error
        self.task_special          = task_special
        self.repeats               = repeats              # number of times I repeat, 0 for infinite or indefinite
        self.task_variable_object  = None                 # not always needed
        self.task_msg              = "task_msg defaulted" # not always needed
        self.msg                   = "msg defaulted"      # may be dead !!

        self.task_list.append( self )

    def set_TVO(self, task_variable_object ):
        """
        std set function
        a task variable object is an optional component for tasks that might need optional values
        I am using with "deer me"  must be customized to go with the task functions in this guy
        can be pretty much anything with go back is a number
        """
        self.task_variable_object   = task_variable_object

    def set_msg(self, msg ):
        """
        std set function
        """
        self.msg   = msg

# =============================================================
class TaskList:
    """
    largely a list of things of type ATask and information to control their use
    New, rename without suffix and with Old and new to swap in and out
    list of tasks to be executed automatically

    """
    def __init__(self, controller ):
        """
        """
        self.controller   = controller
        self.start_time   = time.time()   #  start for each one

        #self.logger       = logging.getLogger("TaskList")
        self.logger       = controller.logger
        #logger.info("added %s and %s to get %s" % (3, 8, 8))

        self.auto_on      = False   # default change with start_auto, stop_auto

        self.tasks        = []     # list of tasks
        self.ix_task      = None   # the index into the task list

        # for working on the current task
        self.repeats_ix   = None      # counts down to 0 unless self.repeats is itself 0
        self.repeats      = None      # what

        #self.done_rec     = False
        #self.done_trans   = False
        self.what_next     = None    # flag for what is next
        #self.task_next    = 1
        # basically an enum:
        # values for the next action return code from tasks -- tells what will happen next
        self.trans_next   = 1    # transmit next in this ix
        self.rec_next     = 2    # receive task in this ix
        self.special_next = 3    # do special task, may be error in this ix
        self.advance_next = 4    # advance to next task ix, can be used from transmit to skip the receive
        self.same_next    = 5    # could instead return task we are on -- not clear, untested stay on ix and stay on step within


#    this is one way to initialize the list, odd but works, often last task repeats 0 times, indefinitely

#    def __init__(self, task_list, task_trans,    task_rec,
#                                  task_special,  task_time_error,
#                                  repeats,
#                                  time_start,   time_delta, time_error   ):


#        need_me  = ATask( self, task_trans      = self.task_version_trans,      task_rec         = self.task_version_rec,
#                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
#                                repeats         = 3,
#                                time_start      = 10,   time_delta = 5, time_error = 1 )

    # ----------------------------------------
    def make_tasks_for_x( self, ):
        """
        make tasks for something, deer me, well monitor ?
        """
        # open port,
        need_me  = ATask( self, task_trans      = self.task_open_trans,         task_rec         = self.task_open_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 2,   time_delta = 5, time_error = 100  )

        need_me  = ATask( self, task_trans      = self.task_version_trans,      task_rec         = self.task_version_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 5,   time_delta = 5, time_error = 10  )

        need_me  = ATask( self, task_trans      = self.task_list_trans,         task_rec         = self.task_list_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 0, # it will end itself
                                time_start      = .1,   time_delta = .1, time_error = 100  )

        #a_tvo    = TaskVariableObject()
        #need_me.set_TVO( a_tvo )


    # ----------------------------------------
    def make_tasks_for_well_monitor( self, ):
        """
        make
        tasks for something, deer me, well monitor ?
        """
        self.logger.debug( "make_tasks_for_well_monitor" )
        self.task_list.reset_tasks()
        # open port,
        need_me  = ATask( self, task_trans      = self.task_open_trans,         task_rec         = self.task_open_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 2,   time_delta = 5, time_error = 100  )

        need_me  = ATask( self, task_trans      = self.task_version_trans,      task_rec         = self.task_version_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 5,   time_delta = 5, time_error = 10  )

        need_me  = ATask( self, task_trans      = self.task_list_trans,         task_rec         = self.task_list_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 0, # it will end itself
                                time_start      = .1,   time_delta = .1, time_error = 100  )

        a_tvo    = TaskVariableObject()
        need_me.set_TVO( a_tvo )


    # ----------------------------------------
    def make_tasks_for_green_house( self, ):
        """
        !! have tasks ready for test
        make tasks for green house, uses some stuff in
        parameters
        status, under development
        """
        self.logger.debug( "make_tasks_for_green_house" )

        self.reset_tasks()

        # open port,
        need_me  = ATask( self, task_trans      = self.task_open_trans,         task_rec         = self.task_open_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 2,   time_delta = 5, time_error = 100  )
        # check version
        need_me  = ATask( self, task_trans      = self.task_version_trans,      task_rec         = self.task_version_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 5,   time_delta = 5, time_error = 10  )

        # print message
        need_me  = ATask( self, task_trans      = self.task_print_trans,      task_rec         = self.task_print_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 5,   time_delta = 5, time_error = 10  )
        need_me.set_msg( "this is message 1" )


        # print message
        need_me  = ATask( self, task_trans      = self.task_print_trans,      task_rec         = self.task_print_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 1,   time_delta = 5, time_error = 10  )
        need_me.set_msg( "this is message 2" )


        # print message
        need_me  = ATask( self, task_trans      = self.task_print_trans,      task_rec         = self.task_print_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 1,   time_delta = 5, time_error = 10  )
        need_me.set_msg( "this is message 3" )


#        # print message
#        need_me  = ATask( self, task_trans      = self.task_print_trans,        task_rec         = self.task_print_rec,
#                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
#                                repeats         = 1,
#                                time_start      = 1,   time_delta = 5, time_error = 10  )
#        need_me.set_msg( "this is message 4" )


#        # print message
#        need_me  = ATask( self, task_trans      = self.task_print_trans,        task_rec         = self.task_print_rec,
#                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
#                                repeats         = 1,
#                                time_start      = 1,   time_delta = 5, time_error = 10  )
#        need_me.set_msg( "this is message 5" )


#        # print message
#        need_me  = ATask( self, task_trans      = self.task_print_trans,        task_rec         = self.task_print_rec,
#                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
#                                repeats         = 1,
#                                time_start      = 1,   time_delta = 5, time_error = 10  )
#        need_me.set_msg( "this is message 6" )


        # aquire data  -- but wait after version
        need_me  = ATask( self, task_trans      = self.task_gh_trans_aquire,    task_rec         = self.task_gh_rec_aquire,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1, # = 0 infinite loop
                                time_start      = 5,   time_delta = .1, time_error = 10  )

        # get temperature
        need_me  = ATask( self, task_trans      = self.task_gh_trans_temp,      task_rec         = self.task_gh_rec_temp,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1, # = 0 infinite loop
                                time_start      = .1,   time_delta = .1, time_error = 10  )


                                        # get temperature
        need_me  = ATask( self, task_trans      = self.task_gh_trans_humid,      task_rec         = self.task_gh_rec_humid,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1, # = 0 infinite loop
                                time_start      = .1,   time_delta = .1, time_error = 10  )



        # go back !!!!!!!!
        need_me  = ATask( self, task_trans      = self.task_go_back_n,          task_rec         = self.task_go_back_n,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 0, # = 0 infinite loop -- but not for go back
                                time_start      = .1,   time_delta = 5, time_error = 10  )
        need_me.set_msg( "task_go_back_n " )
        need_me.set_TVO( 3 )

        # ====================== end of loop ========================

        # close port, this is normally the never occuring end
        need_me  = ATask( self, task_trans      = self.task_close_trans,    task_rec         = self.task_close_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1, # = 0 infinite loop
                                time_start      = .1,   time_delta = 5, time_error = 10  )

        # print message
        need_me  = ATask( self, task_trans      = self.task_print_trans,      task_rec         = self.task_print_rec,
                                task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
                                repeats         = 1,
                                time_start      = 5,   time_delta = 5, time_error = 10  )

        need_me.set_msg( "this is message 999" )

    # ----------------------------------------
    def reset_tasks( self, ):
        self.tasks = []     # new list instead of emptying prior array, ok as well as someone not using a copy
        # perhaps should reset some index as well ??

    # ----------------------------------------
    def append( self, atask ):
        """
        append a task to the task list
        """
        self.tasks.append( atask )

    # ----------------------------------------
    def start_auto( self, ):
        """
        start automatic processing
        use from a cold start will start from
        first task, better to name start_auto ??
        """

        # this sets up a phony auto since we are right away going to the next
        self.ix_task      = -1    # the index into the task list
                                  # because willi ndex up by one on first call
        # set up as if we are finishing the -1 task thes values indicate it is over
        self.repeats_ix   = 1      # counts down to 0 unless self.repeats is itself 0
        self.repeats      = 1      # need me?

        self.next_auto()
        self.controller.gui.showRecFrame( "Start Auto: \n" )
        self.auto_on      = True

    # ----------------------------------------
    def stop_auto( self, ):
        """
        stop auto processing
        may be called on error condition
        """
        self.controller.gui.showRecFrame( "Stop Auto: \n" )
        self.auto_on      = False

    # -------------------------------------------------------
    def goto_delta( self, delta ):
        """
        # !! needs testing, off by 1 init right need arduino
        this is a goto for the task list, normally used for looping
        -delta goes back, normally the situation for looping
        """
        self.ix_task     += delta

        if self.ix_task >= len( self.tasks ) :
            self.logger.error( "goto_delta now beyond end of list calling stop_auto( ) " )
            self.stop_auto( )
            #self.auto_on     = False
            return

        self.repeats       = self.tasks[self.ix_task].repeats
        self.repeats_ix    = self.repeats
        self._init_task_()
        return

    # -------------------------------------------------------
    def next_auto( self, ):
        """
        set up and execute the next auto which may or may not be a repeat
        if not a repeat set up for the on the list, or if at end shut
        down the auto
        """
        # are we in infinite/indefinite  task
        if  self.repeats   == 0:
            self._init_task_()
            return

        # check to see if we need to advance task or do a repat on this

        self.repeats_ix   -= 1      # working to 0

        if self.repeats_ix != 0:
            self._init_task_()
            return

        # advance on task list
        self.ix_task     += 1

        if self.ix_task >= len( self.tasks ) :
            self.logger.info( "done all tasks ; calling stop_auto( ) " )
            self.stop_auto( )
            return

        self.repeats       = self.tasks[self.ix_task].repeats
        self.repeats_ix    = self.repeats
        self._init_task_()
        return

    # -------------------------------------------------------
    def _init_task_( self, ):
        """
        initializes for running a task or repeat after correct self.ix_task is set
        """
        # self.ix_task now at proper value, set up the task for do_task
        self.time_next       = time.time( )      + self.tasks[self.ix_task].time_start     # time_delta used after first time
        self.time_error      = self.time_next    + self.tasks[self.ix_task].time_error

        self.what_next       = self.trans_next    # set to control what is next  set after each call

    # -------------------------------------------------------
    def  do_task( self, trans_rec, tr_data ):
        """
        This is were we do the task on self.tasks[], usually trans or receive, but may have error or special
        if special next or error no delap just done
        always pass in data even if none then use something like empty strings
        trans_rec     t or r for transmit receive
        tr_data       data passed in to transmit or receive -- more info ??
        do a task on the task list
        note possible early return
        """
        # past time: time error
        if self.time_error  <= time.time():
            self.logger.info( "do_task time_error" )
            self.tasks[self.ix_task].task_time_error( self.tasks[self.ix_task] )  # calling with myself ??
            return

        # not time yet
        if self.time_next  >= time.time():
            return

        # is this right place based on timing, probably
        # advance to next task ( is this based on count or special processing in another task )
        if self.what_next  == self.advance_next:
            # self.logger.info( " do_task() self.advance_next" )
            self.next_auto()
            return

        if ( trans_rec == "t" ) and ( self.what_next == self.trans_next  ):   # assume s first

            self.what_next = self.tasks[self.ix_task].task_trans( "ignored" ) # commonly a receive next but maybe not
            if self.what_next == self.same_next:
                 self.what_next = self.trans_next

        elif  ( trans_rec == "r" ) and ( self.what_next == self.rec_next  ):  # transmit first if don_trans false how did we ge t here error !!!
             self.what_next = self.tasks[self.ix_task].task_rec(  tr_data ) # task changes on error or data not complete
             if self.what_next == self.same_next:
                 self.what_next = self.rec_next

        # wait or do it here
        if  ( self.what_next == self.special_next  ):
             self.logger.info( "self.what_next == self.special_next" )


             self.what_next = self.tasks[self.ix_task].task_special( "ignored"  ) # task changes on error or data not complete
             if self.what_next == self.same_next:
                 self.what_next = self.special_next

# ============== some tasks =========================

# -------------- ir tasks ----------------------------
    #----------------- send IR stream  --------------------------
    def task_ir_trans( self, ignore_data ):
        """
        probably dead, update or delete for infrared terminal
        transmit a list of stuff one at a time -- in this case tuples for deer me strobe
        may post activity to terminal area
        """
        # need to find my object and use him, I should belong to

        # self.controller.myllogger.log( " task_list_trans t ", 1 )
        #self.controller.myGui.showRecFrame( " task_list_trans() \n" )
        data = self.tasks[self.ix_task].task_variable_object.get_next_send()
        if data == "":
           print "hit the end of the data in tvo"
           # not great way of ending, assumes that repeates was set to 0  did not work
           self.repeats     = 1
           self.repeats_ix  = 1
           return self.advance_next

        self.controller.send( data + "\n" )
        return self.rec_next

    #-----------------
    def task_ir_rec( self, rec_data ):
        """
        probably dead, update or delete for infrared terminal
        may post activity to terminal area
        """
        # just receive anything
        if rec_data is None:
           self.logger.info( "task_list_rec() rec_data is None " )
           return self.same_next

        #self.controller.parameters.self.arduino_string
        #ix  = rec_data.find( self.controller.parameters.arduino_string, 0, len(rec_data) )
        return self.advance_next    # transmit get me out
        # return self.advance_next

# -------------- gh tasks ----------------------------

    # ============= aquire data =================
    # ----------  -------------
    def task_gh_trans_aquire( self, rec_data ):
        """
        transmit the aquire request
        """
        #self.logger.info( "task_gh_trans_aquire" )
        self.controller.gui.showRecFrame( "aquire data \n" )
        self.controller.send( "a\n" )

        return self.rec_next

    # ----------  -------------
    def task_gh_rec_aquire( self, rec_data ):
        """
        receive the aquire response "ok" line
        """
        if rec_data == "":
           #self.logger.debug( "version_task rec_data is empty string " )
           return self.same_next

        ix  = rec_data.find( "ok", 0, len( rec_data ) )

        if ix != -1:
          self.controller.gui.showRecFrame( "data aquired: \n" )
          self.controller.gh_processing.set_time()   # if not done there will be no saving based on time
          return self.advance_next
        else:
          self.controller.gui.showRecFrame( "aquire error? " + rec_data + "\n" )
          self.logger.debug( "Version not so good:^^^" + rec_data  + "^^^",  )
          return self.advance_next  # for now go on anyway  !!

        #return "never get here"

    # ============ temperature =======================
    def task_gh_trans_temp( self, ignore_data ):
        """
        transmit the temperature request
        """
        self.controller.gui.showRecFrame( "get temperature \n" )
        self.controller.send( "t\n" )
        return self.rec_next

    # ----------  -------------
    def task_gh_rec_temp( self, rec_data ):
        """
        receive the temperature line and process
        """
        if rec_data == "":
           #self.logger.debug( "task_gh_rec_temp rec_data is empty string " )
           return self.same_next

        self.controller.gh_processing.process_temp_line( rec_data )
        return self.advance_next

    # ============ humid =======================
    def task_gh_trans_humid( self, ignore_data ):
        """
        transmit the humid request
        """
        self.controller.gui.showRecFrame( "get humid \n" )
        self.controller.send( "h\n" )
        return self.rec_next

    # ----------  -------------
    def task_gh_rec_humid( self, rec_data ):
        """
        receive the temperature line and process
        """
        if rec_data == "":
           return self.same_next
        #self.myllogger.log( "version_task 2 r^^^" + rec_data  + "^^^", 1 )
        self.controller.gh_processing.process_humid_line( rec_data )
        return self.advance_next

# -------------- general tasks ----------------------------

    # ---------- open com port -------------
    def task_open_trans( self, ignore_data ):
        """
        trans task for opening the comm driver
        post activity to terminal area
        return: next task code
        """
        # how about repeat or fail, maybe tasks should have more returns or state

        self.controller.gui.showRecFrame( "Open port: \n" )
        self.controller.open_com_driver(  )
        return self.rec_next

    # -----------------------
    def task_open_rec( self, data ):
        """
        rec task for opening the comm driver
        basically just waits for received data, does not inspect
        !! add error checking
        ?? this only works if arduino is reset else it should be skipped
        return: code for what is next
        """
        #self.controller.myllogger.log( "open_task r " + data, 1 )
        return self.advance_next

    #----------------- close comm port --------------------------
    def task_close_trans( self, ignore_data ):
        """
        task to close the comm port
        post activitself.controllery to terminal area
        """
        # how about repeat or fail, maybe tasks should have more returns or state
        self.logger.info( "close_task t"  )
        self.controller.gui.showRecFrame( "Close port: \n" )
        self.controller.closeDriver(  )
        return self.rec_next

    #-------------------------------------------
    def task_close_rec( self, data ):
        """
        task to close the comm port
        post activitself.controllery to terminal area
        perhaps this should be skipped
        """
        self.logger.info( "close_task r " + data )
        return self.advance_next

    #----------------- version check arduino software version --------------------------
    def task_version_trans( self, ignore_data ):
        """
        a task: tries to get version from the uprocessor and validate
        post activity to terminal area
        """
        # how about repeat or fail, maybe tasks should have more returns or state
        #self.myllogger.log( "version_task", 1 )
        self.logger.debug( "version_task send check version" )
        self.controller.gui.showRecFrame( "Check Version: \n" )
        self.controller.send( "v\n" )
        return self.rec_next

# --------------------------------
    def task_version_rec( self, rec_data ):
        """
        a task: tries to get version from the uprocessor and validate
        post activity to terminal area
        version control from Parameters
        """
        if rec_data == "":
           #self.logger.debug( "version_task rec_data is empty string " )
           return self.same_next

        ix  = rec_data.find( self.controller.parameters.arduino_string, 0, len( rec_data ) )
        self.logger.info( "task_version_recr^^^" + rec_data  + "^^^",  )
        if ix != -1:
          self.controller.gui.showRecFrame( "Version good: \n" )
          return self.advance_next
        else:
          self.controller.gui.showRecFrame( "Version not so good: got " + rec_data + "\n" )
          self.logger.info( "Version not so good:^^^" + rec_data  + "^^^",  )

          if rec_data == "":
               self.logger.info( "problem: version_task rec_data is empty string we should not be here" )

          return self.special_next      # return self.advance_next

    # ---------- open com port -------------
    def task_print_trans( self, ignore_data ):
        """
        just show the msg
        """
        msg   = "task_print_trans " + str(  self.tasks[ self.ix_task ].msg )
        self.controller.gui.showRecFrame( msg + "\n" )
        print msg
        #self.logger.info( msg )

        return self.rec_next

    #-----------------
    def task_print_rec( self, rec_data ):
        """
        may post activity to terminal area
        """
        msg   = "task_print_rec " + str(  self.tasks[ self.ix_task ].msg )
        self.controller.gui.showRecFrame( msg + "\n" )
        print msg
        #self.logger.info( msg )

        return self.advance_next    #

    #----------------- send a list tasks  --------------------------
    def task_list_trans( self, ignore_data ):
        """
        dead update or delete
        transmit a list of stuff one at a time -- in this case tuples for deer me strobe
        may post activity to terminal area
        """
        # need to find my object and use him, I should belong to

        # self.controller.myllogger.log( " task_list_trans t ", 1 )
        #self.controller.myGui.showRecFrame( " task_list_trans() \n" )
        data = self.tasks[self.ix_task].task_variable_object.get_next_send()
        if data == "":
           print "hit the end of the data in tvo"
           # not great way of ending, assumes that repeates was set to 0  did not work
           self.repeats     = 1
           self.repeats_ix  = 1
           return self.advance_next

        self.controller.send( data + "\n" )
        return self.rec_next

    #-----------------
    def task_list_rec( self, rec_data ):
        """
        may post activity to terminal area
        """
        # just receive anything  !! this may not be right use "" ??
        if rec_data is None:
           self.logger.info( "task_list_rec() rec_data is None " )
           return self.same_next

        #self.controller.parameters.self.arduino_string
        #ix  = rec_data.find( self.controller.parameters.arduino_string, 0, len(rec_data) )
        return self.advance_next    # transmit get me out
        # return self.advance_next

    #----------------- generally back up some number of task ix and set to trans next --------------
    # use for looping -- the go to is relative
    # may be used as a special task or a receive task ??
    def task_go_back_n( self, ignore_data ):
        """
        make task list looping
        """
        msg   = "task_go_back_n " + str(  self.tasks[ self.ix_task ].msg )
        self.controller.gui.showRecFrame( msg + "\n" )
        #print msg
        #self.logger.info( msg )

        self.repeats_ix = 1     # will be decremented
        self.repeats    = 1     # in case we were a repeating task which would be us odd
        self.ix_task    -=  ( self.tasks[ self.ix_task ].task_variable_object   + 1) # need one extra

        return self.advance_next  # if we set ix one too low   self.

# ===================================

    #----------------- throw and exception  --------------------------
    def task_special_exception( self, ignore_data ):
        """
        a task: throw an exception - pretty much ends it all
        crude !! fix up later
        """
        # self.controller.myGui.showRecFrame( "Version good: \n" )
        self.logger.debug( "task_special_exception" )
        self.controller.gui.printToSendArea(  "gui task_special_exception" )
        #root.destroy() # does this end tkinter ?  need reference to root in controller??

        # how to manage this exception kind of crashes us out
        #raise RSHException( 'from special_exception_task()' )
        #root.destroy() # does this end tkinter ?
        return self.same_next
        #return self.special_next
        #return self.advance_next

# ========================== Begin Class ================================
class SmartTerminal:
    """
    main and controller class for the Smart Terminal application
    see bottom of file for app startup
    """
    def __init__(self ):

        # ------------------- basic setup --------------------------------
        print ""
        print "=============== starting smart terminal  ========================= "
        print ""

        self.app_name       = "SmartTerminal "              # std name often used in other apps
        self.version        = "2016 09 27.01 ( beta ) "     # std name

        # ----- parameters

        self.parmeters_x    = "none"        # name without .py for parameters extension may be replaced by command line args
        self.get_args( )
        # command line might look like this
        # python smart_terminal.py    parameters=gh_paramaters

        self.parameters     = parameters.Parameters( self )  #  std name -- open early may effect other

        # get parm extensions  look at ir terminal -- this may modify anything in parameters still pre logger
        self.logger         = None    # set later none value protects against call against nothing
        if self.parmeters_x != "none":
              self.parmeters_xx   =  self.create_comm_class( self.parmeters_x, "ParmetersXx" )
              self.parmeters_xx.modify( self.parameters )

        self.logger_id      = self.parameters.logger_id       # std name
        self.logger         = self.config_logger()            # std name

        self.app_name       += " Mode: " + self.parameters.mode    # std name ??

        # module and class name for the communications driver.
        self.comm_mod       = self.parameters.comm_mod
        self.comm_class     = self.parameters.comm_class

        self.connect        = self.parameters.connect
        self.mode           = self.parameters.mode

        self.array_ix       = 0       # need to look into whole send array, may be obsolete  !!
        self.ir_signal      = None    # may be obsolete  !!
        self.starting_dir   = os.getcwd()    # or perhaps parse out of command line
        self.prog_info()

        # some of this stuff might be controlled by mode parameters or the type of processing created
        if self.connect     != "no":

            self.db             = db.DBAccess( self, CSVMode = False )

        # this is important so check !! change to dict
        if   self.mode == "Terminal":
            print "parameter says " +  self.mode

        elif self.mode == "GreenHouse":
            print "create greenhous processing "
            self.gh_processing  = gh_processing.GHProcessing( self )
            self.gh_graphing    = gh_graphing.GraphDB( self )

        elif self.mode == "RootCellar":
            print "parameter says " +  self.mode

        else:
            print "parameter says ??? " + self.mode

        if self.connect     != "no":
            self.graphDB        = graphing.GraphDB( self )

        self.data_point     = data_point.DataPoint( self.parameters.run_ave_len )

        self.looping        = False   # for our looping operations
        self.task_list      = TaskList( self )

        self.task_send_list = None     # list of things to be send via tasks see send_list_task
        self.task_send_ix1  = -1       # index for above, better packaged in an object -- yes later
        self.task_send_ix2  = -1       # index for above, better packaged in an object -- yes later

        self.com_driver       =  self.create_comm_class( self.parameters.comm_mod, self.parameters.comm_class )

        self.win              = Tkinter.Tk()    # this is the tkinter root for the GUI move to gui after new working well plus bunch after here

        if self.parameters.os_win:
            # icon may cause problem in linux for now only use in win
            # print "in windows setting icon"
            self.win.iconbitmap( self.parameters.icon )

        a_title   = self.app_name + " version: " + self.version
        if self.parmeters_x    != "none":
            a_title  += " parameters=" +   self.parmeters_x

        self.win.title( a_title )

        #self.gui          = gui.GUI( self, self.win,  [] )  # create the gui or view part of the program
        self.gui           = gui.GUI( self, self.win,  )  # create the gui or view part of the program

        self.win.geometry( self.parameters.win_geometry )

        self.win.taskDelta  = self.parameters.poll_delta_t  # in ms

        self.loop_period    = self.parameters.loop_period
        self.loop_ix        = 0    # counter down in task  !! may be obsolete

        self.win.after( self.win.taskDelta, self.polling )   # have to kick off gui task the first time
        self.task_tick   = 0        # tick in task
        self.array_send  = False

        if  self.parameters.task_list_on:
              self.task_list.start_auto( )   # kick off auto

        # --------------------------------------------------------
        #print "starting mainloop"
        self.win.mainloop()
        # print " init and we are all over....  "

        self.com_driver.close()     # !! serial

        if self.connect     != "no":
            self.db.dbClose()

        self.logger.info( self.app_name + ": all done" )
        return

    # --------------------------------------------------------
    def config_logger( self, ):
        """
        configure the logger in usual way
        return: the logger
        """
        logger = logging.getLogger( self.logger_id  )

        logger.handlers = []
        logger.setLevel( self.parameters.logging_level )     # DEBUG , INFO	WARNING	ERROR	CRITICAL

        # create the logging file handler.....
        fh = logging.FileHandler(   self.parameters.pylogging_fn )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info("Done config_logger") #  .debug   .info    .warn    .error

        return logger

     # -------------------------------------------------------
    def prog_info( self ):
        """
        log info about program and its argument/enviroment
        after logger is set up
        """
        self.logger.info(  "" )
        self.logger.info(  "" )
        self.logger.info(  "============================" )
        self.logger.info(  "" )

        self.logger.info( "Running " + self.app_name + " version = " + self.version  )
        self.logger.info(  "" )
        # !! add mode

        if len( sys.argv ) == 0:
            self.logger.info( "no command line arg " )
        else:
            ix_arg = 0
            for aArg in  sys.argv:

                self.logger.info( "command line arg " + str( ix_arg ) + " = " + sys.argv[ix_arg])
                ix_arg += 1

        self.logger.info(  "current directory " +  os.getcwd() )
        return

    #----------------------------------------------
    def get_args( self, ):
        """
        get the argument off the command line
        no spaces allowed around the = sign
        note log file not yet open?
        """
        for iarg in sys.argv[1:]:
            #print iarg
            argsplits   = iarg.split("=")
            parm_name   = argsplits[0]
            parm_value  = argsplits[1]
            #print argsplits

            # so far only one is captured
            if parm_name == "parameters":
                self.parmeters_x  =  parm_value   #
                print "command line arg >> " + iarg    # log file not open

            else:
                print "no parmeter extensions"

        return

    # -------------------------------------------------------
    def create_comm_class( self, module_name, class_name):
        """
        this will load a driver from string names
        so that parameter file can specify dirver, often
        to change comm protocols.
        will also load other stuff from strings, more general than just comm class
        """

        if not( self.logger is None ):
            self.logger.info(  "create com class "  +  module_name +  " " +  class_name )

        print module_name + " " + class_name
        a_class    = getattr(importlib.import_module(module_name), class_name)
        instance   = a_class( self )

        return instance

    # -------------------------------------------------------
    def polling( self, ):
            """
            polling task runs continually in the GUI
            reciving data is an important task.
            also auto tasks will be run from here
            polling frequency set via taskDelta, ultimately in parameters
            http://matteolandi.blogspot.com/2012/06/threading-with-tkinter-done-properly.html
            safely invoke the method tk.after_idle to actually schedule the update. That's it!
            """
            self.task_tick  += 1    # left over from ir, we have two sub tasks, why not reset counter
                                    # to 0 have one for each subtask is several

            if self.task_list.auto_on:
                    self.task_list.do_task( "t", "ignored" )

            data   = self.receive(  )       # this is the basic task that makes the app recive, transmit from button

            if self.task_list.auto_on:    # if data is none should i still do task?  maybe for error check
                    self.task_list.do_task( "r", data )   # argument for the data or reach into controller?

            # need to stick received data in a list for processing by the main loop
            # this is obsolete may be time to rip out !!!
            if self.array_send:
                #self.loggerit( str( self.task_tick  %  self.parameters.send_array_mod )  )
                if ( ( self.task_tick % self.parameters.send_array_mod ) == 0 ):  # 5 might be in parms
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
                    sdata   = self.parameters.loop_text

                    self.com_driver.send( sdata )
                    self.gui.printToSendArea(  sdata )

            self.win.after( self.win.taskDelta, self.polling )  # reschedule event
            return

    #-------------------------------------------
    def send_list_task( self, trans_rec, rec_data ):
        """
        a task
        get a measurement from the uprocessor
        ! post activity to terminal area
        """
        # self.task_send_list
        # self.task_send_ix1  = -1
        # how about repeat or fail, maybe tasks should have more returns or state
        self.logger.debug( "send_list_task" )
        if ( trans_rec == "t" ):
              #self.myllogger.log( "measure_task t " + rec_data, 1 )
              self.gui.showRecFrame( "Measure...: \n" )
              if  self.task_send_ix1 == 0:
                    self.send( "n" + self.task_send_list[self.task_send_ix2][ self.task_send_ix1 ] + "\n" )
                    self.task_send_ix1 = 1
              elif self.task_send_ix1 == 1:
                    self.send( "f" + self.task_send_list[self.task_send_ix2][ self.task_send_ix1 ] + "\n" )
                    self.task_send_ix1 = 2
              elif self.task_send_ix1 == 2:
                    self.send( "r" + self.task_send_list[self.task_send_ix2][ self.task_send_ix1 ] + "\n" )
                    self.task_send_ix2 += 1

              return True

        else:  # rec activity
              #self.myllogger.log( "measure_task r^^^" + str( rec_data )  + "^^^", 1 )
              if rec_data is None:
                   return False

              if rec_data == "":
                   return False

              self.gui.showRecFrame( "send_list_task: " + rec_data + "\n" )
              #self.myllogger.log( "measure_task r2^^^" + rec_data  + "^^^", 1 )

              return True

    #-------------------------------------------
    def error_task( self, ):
        """
        an error task
        mostly log !! need upgrade
        """
        msg = "error_task......."
        self.gui.showRecFrame( msg )
        self.logger.info( msg )
        return

    #==================== end tasks =============
    def open_com_driver( self ):
        """
        open the comm port driver
        updates gui , status available in driver
        !! add return True False
        """
        val   = self.com_driver.open()
        if val:
            status = "Open"
            self.logger.info( "open_driver, opened ok" )
        else:
            status = "Open Failed"
            self.logger.info( "open failed, ignored" )

        self.gui.set_open( status )

        return

    #-------------------------------------------
    def closeDriver( self ):
        """
        close the communications port driver, update gui
        """
        self.com_driver.close()
        self.gui.set_open( "Closed" )

        return

    # -------------------------------------------------------
    def send( self, adata ):
         """
         send the data over the comm port, may post to gui
         add block on port closed ?? -- or disable send buttons??
         """
         if self.parameters.echoSend:
            self.gui.printToSendArea( adata )

         self.com_driver.send( adata )
         return

    # -------------------------------------------------------
    def receive( self,  ):   # combine with task?
        """
        receive data via the comm port
        display data
        return data   "" if no data
        -----
        receive only full strings ending with /n else
        accumulated in the driver /n is stripped
        """
        # for 232: breaks simulator

        data   = self.com_driver.getRecString( )
        if data == "":
             pass
        else:
             self.gui.showRecFrame( "# <<<" + data + "\n" )
        return data

    #-------------------------------------------
    def sendArray( self, irlist ):
        """
        sends an array of data to update the uprocessor
        was for ir, probably no place in well monitor
        send arduino commands to load a new array of signals
        !!! obsolete ?
        """
        # --- this needs to be moved to task some set up here then on there

        self.logger.info( "turn on send array"  )
        self.array_ix   = 0

        #self.ir_signal  = [ 180, 920, 160, 1740, 160, 780,   160, 2840, 160, 1320, 160, 1340, 160, ] # 1180, 160, 2700, 160, 12780, 200, 920,   \
                           #160, 2680, 160, 780, 160, 800, 160, 780, 160, 920, 160, 800, 140, 800,   \
                           #  160 ]
        self.ir_signal  = irlist
        self.com_driver.send( "z\n" )
        self.array_send = True    # if we were mult-threaded this would have to be here

        return

    #-------------------------------------------
    def addDB( self,  ):
        """
        hardcoded test routine for adding to the data base
        this is a test for now  !! clean up delete
        """
        self.db.dbAddRow( time.time(), 50., 1 )
        self.logger.debug( "did db update did it work?" )
        return

    # ----------------------------------------------
    def graph( self,  ):
        """
        this is a test for now - does simple graph !! clean up delete
        """
        self.graphDB.testGraph()
        return

    # ----------------------------------------------
    def os_start_db( self,  ):
        """
        used as callback from gui button
        nice idea will not work in win run as admin.....
        """
        from subprocess import Popen, PIPE  # since infrequently used ??

        if self.parameters.start_db  == "": # no command to start db

            pass # consider message box
        else:
            proc = Popen( [ self.parameters.start_db ] )

    # ----------------------------------------------
    def os_open_logfile( self,  ):
        """
        used as callback from gui button
        """
        from subprocess import Popen, PIPE  # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, self.parameters.pylogging_fn ] )

    # ----------------------------------------------
    def os_open_parmfile( self,  ):
        """
        used as callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + "parameters.py"

        from subprocess import Popen, PIPE  # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

    # ----------------------------------------------
    def os_open_parmxfile( self,  ):
        """
        used as callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + self.parmeters_x + ".py"

        from subprocess import Popen, PIPE  # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

# ------------------ callbacks for buttons -----------------
    # ----------------------------------------------
    def cb_gui_test_1( self,  ):
        """
        call back for gui button test_1
        """
        self.task_list.make_tasks_for_green_house()
        self.task_list.start_auto( )

    # ----------------------------------------------
    def cb_gui_test_2( self,  ):
        """
        call back for gui button
        """
        self.task_list.stop_auto( )

    # ----------------------------------------------
    def cb_gui_test_3( self,  ):
        """
        call back for gui button
        """
        self.task_list.stop_auto( )
        self.gh_graphing.testGraph()

    # ----------------------------------------------
    def ports( self,  ):
         """
         probe for ports, not finished  ??
         post to receive area
         windows 10 seems to break come back empty
         """
         ports   = self.com_driver.listAvailable()
         self.gui.showRecFrame( "Reported Ports: \n" )

         for aport in ports:
             self.gui.showRecFrame( aport[0] )
             self.gui.showRecFrame( "\n" )

    # ----------------------------------------------

if __name__ == '__main__':
        """
        run the app
        """
        a_app = SmartTerminal(  )

        # --------------- a test -----------------------------------
#        print "test"
#        aTVO   = TaskVariableObject()
#
#        while True:
#            gns  = aTVO.get_next_send()
#            print gns
#            if gns == "":
#                break

#        # another test
#        print "this is a test TaskVariableObjectIR"
#        aTVO   = TaskVariableObjectIR()
#        aTVO.set_datas( [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 ]    )
#
#        while True:
#            gns  = aTVO.get_next_send()
#            print gns
#            if gns == "":
#                break


# ====================== eof ========================



