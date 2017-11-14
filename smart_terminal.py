# -*- coding: utf-8 -*-

#
# History/ToDo  ** = when done   !! = planned or considerd ?? = think about
#   Copied from mcuterminal, perhaps update from there time to time ( aug 2015 )

#   Important sub projects:
#   ** probe com ports
#   !! work on restart in polling
#   ** introduce a second thread
#   !! add launch grapher
#   ?? give grapher access to terminal parameters
#
#   ** add some sort of timed tasks unless I have another thread probably needs to be in time
#       perhaps should make a class, but will just embed now.
#       was going to hardcode but base on a list
#       ** start with connect and version tasks
#       ** measure task
#   ?? may be additional stuff in gui.py
#   ?? make a lightweight gui
#   ** save data to database
#   ** open log file using popopen and parameter name of some sort
#   ** convert to python logging
#   *! improve doc, structure clean up
#   ** default the send area test
#   ** add place for test buttons
#   *! look at goto for looping have done a task need to coordinate with an arduino prog and a list.
#   ** add command line second parm file like in ir terminal
#   ** makd a graphing only app, inc a gui = smart_terminal_graph
#   ** auto scroll off on
#   ** detect ports through trial try except, perhaps use the test string as well have list of ports to try
#           look for updates to python look for others code
#   *! continue to clean up prints and logging
#   ** add pylog to gui
#   ?? limit string length as option configure from parameters
#   ** works on PC and Pi
#   ** restart
#   ** some db parms
#   ?? gray out invalid buttons, open close or just use one with toggle
#   ** use names for db connect parameters  "none" for no database
#   !* redirect print to logging file
#   ** turn on task should it make sure port is closed wrong put in task list if you want it
#   !! add IR features   ir_gui  ir_processing
#   ** meta: no db if terminal mode
#   !! try ports and use one with correct response
#   !! set up a second thread
#   !! reboot pi as necessary
#   !! send emails
#   ** change text for send button in parameters
#   !! only probe if port is closed


# from __future__ import print_function

import logging
import importlib
import sys
import os
import time
import traceback
import queue
import threading
import datetime

# ----------- my code imports --------------------------


import db
import parameters

import gui
#import gui_in_kivy    # conditional import later

import smart_terminal_helper

from app_global import AppGlobal    # use see next lines
#self.parameters        = AppGlobal.parameters
#AppGlobal.parameters    = self

# ========================== Begin Class ================================
class SmartTerminal:
    """
    main and controller class for the Smart Terminal application
    see bottom of file for app startup
    """
    def __init__(self ):
        """
        try to get all declared here or restart
        """
        #global print
        # ------------------- basic setup --------------------------------
        print( "" )
        print( "=============== starting SmartTerminal ===============" )
        print( "" )
        print( "     -----> prints may be sent to log file !" )
        print( "" )

        AppGlobal.controller        = self
        self.app_name               = "SmartTerminal"
        self.version                = "Python3 Ver 2 2017 11 13.01"
        self.gui                    =  None
        self.no_restarts            =  -1

        # ----------- for second thread -------
        #self.helper_thread_manager  = None
        self.queue_to_gui           = None
        self.queue_from_gui         = None
        self.gui_recieve_lock       = threading.Lock()   # when locked the gui will process recieve, aquired released in helper
                                                         # how different from just a variable set?
        # self.org_print              = print  # save so can be reset this is the print function
        self.restart( )

    # --------------------------------------------------------
    def restart(self ):
        """
        use to restart the app without ending it
        parameters will be reloaded and the gui rebuilt
        args: zip
        ret: zip ... all sided effects
        """
        #global print
        self.no_restarts    += 1
        if self.gui is not None:

            self.logger.info( self.app_name + ": restart" )

            self.post_to_queue( "stop", None  , (  ) )
            self.helper_thread.join()

            self.close_driver()

            self.gui.close()
            try:
                importlib.reload( parameters )    # should work on python 3 but sometimes does not
            except Exception as ex_arg:
                reload( parameters )              # this is python 2 but seems to work sometimes

        self.is_first_gui_loop    = True
        self.ext_processing       = None          # built later frompermaters if specified
        self.logger               = None          # set later none value protects against call against nothing
        # ----- parameters

        self.parmeters_x          = "none"        # name without .py for parameters extension may be replaced by command line args
        self.get_args( )
        # command line might look like this:  # python smart_terminal.py    parameters=gh_paramaters

        self.parameters     = parameters.Parameters( )  #  std name -- open early may effect other
        
        # get parm extensions  !! will this work on a reload ??
        if self.parmeters_x != "none":
            self.parmeters_xx   =  self.create_class_from_strings( self.parmeters_x, "ParmetersXx" )
            self.parmeters_xx.modify( self.parameters )

        self.logger_id      = self.parameters.logger_id       # std name
        self.logger         = self.config_logger()            # std name

#        if self.parameters.print_to_log:
#            print               = self.logger.info    # redirect print to the logger

        self.db             = None   # define later if needed
        # module and class name for the communications driver.
        self.comm_mod       = self.parameters.comm_mod
        self.comm_class     = self.parameters.comm_class

        self.connect        = self.parameters.connect
        self.mode           = self.parameters.mode

        self.send_list_ix   = 0       # need to look into whole send array, may be obsolete  !!
        self.send_list      = None    # may be obsolete  !!
        # self.list_send    old from ir

        self.starting_dir   = os.getcwd()    # or perhaps parse out of command line
        self.prog_info()

        # some of this stuff might be controlled by mode parameters or the type of processing created
        if self.connect     != "none":
            self.db             = db.DBAccess( self, CSVMode = False )

        self.looping              = False   # for our looping operations # ?? no longer used

        # so that parameter file can specify dirver, perhaps to change comm protocols.
        self.com_driver           =  self.create_class_from_strings( self.parameters.comm_mod, self.parameters.comm_class )

#        import rs232driver2     # this needs fixing for variable drivers !!
#        self.com_settings         = rs232driver2.RS232Settings()
#        self.com_settings.set_from_parameters( self.parameters )

        self.com_driver.set_from_parameters( self.parameters )

        self.queue_to_helper      = queue.Queue( self.parameters.queue_length )   # send strings back to tkinker mainloop here
        self.queue_fr_helper      = queue.Queue( self.parameters.queue_length )
        #controller.request_to_pause       controller.paused

        # these may or may not be issue
#        self.request_to_pause     = False         # helper writes
#        self.paused               = False         # controller writes
        #self.logger.debug(  "end_helper( ) Helper interrupted" )

        self.helper_task_active   = False         # helper writes

        self.helper_thread        = smart_terminal_helper.HelperThread( )
        self.helper_thread.set_controller( self )

        if not ( self.parameters.ext_processing_module is None ):
            self.ext_processing =  self.create_class_from_strings( self.parameters.ext_processing_module,
                                                                   self.parameters.ext_processing_class  )
        if self.parameters.kivy:
            import gui_in_kivy
            self.gui                  = gui_in_kivy.GUI(  )
        else:
            self.gui                  = gui.GUI( )  # create the gui or view part of the program
#        self.loop_period        = self.parameters.loop_period   # !! may be obsolete
#        self.loop_ix            = 0    # counter down in task  !! may be obsolete

        self.exception_records     = []     # keep a list of  ExceptionRecord  add at end limit    self.ex_max

        self.task_tick          = 0        # tick in task for some timing, may not be great idea
        self.list_send          = False

        self.display_db_status()

        # --------------------------------------------------------

        # time.sleep( 10 )
        self.helper_fail     = False   # true means it failed, and will stop itself
        self.helper_thread.start()

        self.start_helper_after     = time.time() + self.parameters.start_helper_delay
        self.helper_start   = ( self.parameters.start_helper_delay  > 0 )
        self.polling_fail   = False  # is what
#        print( "starting mainloop" )
#        sys.stdout.flush()
        self.gui.run()

        self.com_driver.close()     # !! serial
        # end other thread here better than restart

#        print                   = self.org_print    # put back print function
        if self.connect     != "none":
            self.db.dbClose()

        self.post_to_queue( "stop", None  , (  ) )

        self.helper_thread.join()
        self.logger.info( self.app_name + ": all done" )

        return

    # --------------------------------------------------------
    def config_logger( self, ):
        """
        configure the logger in usual way using the current parameters

        args: zip
        ret:  the logger
        """
        logger = logging.getLogger( self.logger_id  )

        logger.handlers = []
        logger.setLevel( self.parameters.logging_level )     # DEBUG , INFO    WARNING    ERROR    CRITICAL

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
        log info about program and its argument/enviroment to the logger
        after logger is set up
        args: zip
        ret:  zip
        """
        if ( self.no_restarts == 0 ) :
            self.logger.info(  "" )
            self.logger.info(  "" )
            self.logger.info(  "============================" )
            self.logger.info(  "" )

            # !! add mode
            self.logger.info( "Running " + self.app_name + " version = " + self.version  + " mode = " + self.parameters.mode )
            self.logger.info(  "" )

        else:

            self.logger.info(  "======" )
            self.logger.info( "Restarting " + self.app_name + " version = " + self.version + " mode = " + self.parameters.mode )
            self.logger.info(  "======" )



#        self.logger.info(  "" )
#        self.logger.info(  "" )
#        self.logger.info(  "============================" )
#        self.logger.info(  "" )
#
#        self.logger.info( "Running " + self.app_name + " version = " + self.version  )
#        self.logger.info(  "" )
        # !! add mode

        if len( sys.argv ) == 0:
            self.logger.info( "no command line arg " )
        else:
            ix_arg = 0
            for aArg in  sys.argv:

                self.logger.info( "command line arg " + str( ix_arg ) + " = " + sys.argv[ix_arg])
                ix_arg += 1

        self.logger.info(  "current directory " +  os.getcwd() )
        self.logger.info(  "COMPUTERNAME "      +  str( os.getenv( "COMPUTERNAME" ) ) )  # may not exist in linux

        start_ts     = time.time()
        dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
        string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        self.logger.info( "Time now: " + string_rep )

        return

    #----------------------------------------------
    def get_args( self, ):
        """
        get the argument off the command line like ( and only so far )
        parameters=parameters_a
        this would cause the loading of parameters_a.py in the smart_terminal directory
        no spaces allowed around the = sign

        note: log file not yet open
        args: zip but looks at command line
        ret:  zip
        """
        for iarg in sys.argv[1:]:
            #print iarg
            argsplits   = iarg.split("=")
            parm_name   = argsplits[0]
            parm_value  = argsplits[1]

            # so far only one is captured
            if parm_name == "parameters":
                self.parmeters_x  =  parm_value   #
                print( "command line arg >> " + iarg  )  # log file not open

            else:
                print( "no parmeter extensions" )

        return

    # -------------------------------------------------------

    def create_class_from_strings( self, module_name, class_name):
        """
        this will load a class from string names
        this makes it easier to specify classes in the parameter file.
        believe it is used for both the comm drive and the "processor"
        args:  strings
        ret:   instance of the class
        """
        if not( self.logger is None ):
            self.logger.debug(  "create class "  +  module_name +  " " +  class_name )

        print( "create class "  + module_name + " " + class_name )
        
        a_class    = getattr(importlib.import_module(module_name), class_name)
        #instance   = a_class( self )
        instance   = a_class(  )
        return instance

    # ------------------------------------------
    def __start_helper_thread__xxx( self,  ):
        """
        bad name
        call from gui pooling, first pass thru i think, but try outside  -- may be obsolete or need to be modified and implemented
        # not currently used, should it be ??
        """
        self.logger.info( "try to start_object_thread" )
        self.queue_to_gui         = queue.Queue( self.parameters.queue_length )   # send strings back to tkinker mainloop here
        self.queue_from_gui       = queue.Queue( self.parameters.queue_length )   # send strings back to tkinker mainloop here

        self.helper_thread      = threading.Thread( target=self.backup_thread.run_backup , args=(  ) )  # wrong old code
        # self.worker_thread_run  = True  !! fix in app_state
        self.helper_thread.start()

    # -------------------------------------------------------
    def polling( self, ):
        """
        this is a private method
        polling task runs continually in the GUI
        reciving data is an important task. but is it in this thread  ??
        also auto tasks will be run from here
        polling frequency set via taskDelta, ultimately in parameters
        http://matteolandi.blogspot.com/2012/06/threading-with-tkinter-done-properly.html
        safely invoke the method tk.after_idle to actually schedule the update. That's it!
        """
        """
        queue protocol, data = ( action, function, function_args )
        action            = a string
        function          = a function
        function_args     = arguments to function which will be called  function( function_args ) This should be a tuple
        """

        # !! may be phasing out
#        if    self.request_to_pause:
#            self.paused               = True
#
#            while self.request_to_pause:  # think function part not used ??
#                time.sleep( .1 )
#
#            self.paused                   = False

#        if self.parameters.start_helper_delay  > 0:
#             helper_start  = True
#        else:
#             helper_start  = False
        # two bits here just used once, have a polling0 then swtch over to this

        if self.is_first_gui_loop:
            # should be moved to gui !! turn back on unless messing up whole app
            # print("lifting...")
#            self.gui.root.attributes("-topmost", True)  # seems to work
#            self.gui.root.lift()                        # did not work
            self.is_first_gui_loop    = False
#            self.gui.root.attributes("-topmost", False)  # seems to work
        try:
            if self.helper_start and ( self.start_helper_after < time.time() ):
            # if self.start_helper_after < time.time() :
                self.helper_start  = False

                msg = "We have an start_helper_function setting in the parmeter file = " + self.parameters.start_helper_function
                self.gui.print_info_string( msg )
                to_eval  = "self.ext_processing." + self.parameters.start_helper_function
                a_function   = eval( to_eval )
                self.post_to_queue( "call", a_function  , self.parameters.start_helper_args )

            if self.gui_recieve_lock.locked():
                self.receive()
            # self.start_helper_after  time to start helper if used
            # loop till queue empty
            ( action, function, function_args ) = self.__rec_from_queue__()
            while action != "":
                if action == "call":
                    #print( "controller making call" )
                    sys.stdout.flush()
                    function( *function_args )
                elif action == "rec":
                    self.gui.print_rec_string(  function_args[ 0 ] )
                elif action == "send":
                    # but where is it actually sent ??
                    self.gui.print_send_string( function_args[ 0 ] )
                elif action == "info":
                    self.gui.print_info_string( function_args[ 0 ] )

                ( action, function, function_args ) = self.__rec_from_queue__()

            self.task_tick  += 1    # for delay in list send

            if self.list_send:  # used for ir_processing and motor processing
                #self.loggerit( str( self.task_tick  %  self.parameters.send_array_mod )  )
                if ( ( self.task_tick % self.parameters.send_array_mod ) == 0 ):  # 5 might be in parms
                    #---
                    #print "send ix_array", self.send_list_ix
                    #self.send( "xxx\n" )
                    self.send( str(  self.send_list[ self.send_list_ix ] ) + "\n" )

                    self.send_list_ix  += 1
                    if ( self.send_list_ix  >= len( self.send_list ) ):
                        self.list_send  = False

        except Exception as ex_arg:
            self.logger.error( "polling Exception in smart_terminal: " + str( ex_arg ) )
            # ?? need to look at which we catch maybe just rsh
            (atype, avalue, atraceback)   = sys.exc_info()
            a_join  = "".join( traceback.format_list ( traceback.extract_tb( atraceback ) ) )
            self.logger.error( a_join )

            a_ex_record              = ExceptionRecord( time.time)     # add at end limit    self.ex_max
            self.exception_records.append( a_ex_record )
            if ( len( self.exception_records ) > self.parameters.ex_max ):
                msg     = "too many exceptions polling in smart terminal may die"
                print( msg )
                self.logger.error( msg )
                self.logger.error( "too many exceptions what to do???" )
                self.polling_fail  = True
                #raise Exception( "too many" )
                #self.restart()  # may leave return on stack ??
            # here we need to set the next task?? lets try, as function may not have returned
            # self.task_list.what_next    = self.task_list.advance_next

        finally:
            if  self.polling_fail:
                pass
            else:
                #print 'In finally block for cleanup'
                self.gui.root.after( self.parameters.gt_delta_t, self.polling )  # reschedule event

        return

    #-------------------------------------------
    def display_db_status( self ):
        """
        here or in gui
        #self.gui.lbl_db_status  = "DB: not connected"
        """

        if self.parameters.kivy:
            return
        spacer   = "                                              "
        lab_len  = 25

        lbl_text  = ( "ConnectName: " + self.parameters.connect    + spacer )[0:lab_len]
        #self.gui.lbl_db_connect.config(    text    =  lbl_text     )
        self.gui.show_item( "db_connect", lbl_text  )

        if self.db is None:
            lbl_text  = ( "Status: Not Connected" + spacer )[0:lab_len]
            #self.gui.lbl_db_status.config(  text    =  lbl_text     )
            self.gui.show_item( "db_status", lbl_text  )

            lbl_text  = ( "Host: None" + spacer )[0:lab_len]
            #self.gui.lbl_db_host.config(    text    =  lbl_text     )
            self.gui.show_item( "db_host", lbl_text  )

            lbl_text  = ( "DB: None" + spacer )[0:lab_len]
            #self.gui.lbl_db_db.config(      text    =  lbl_text     )
            self.gui.show_item( "db_db", lbl_text  )

            lbl_text  = ( "User: None" + spacer )[0:lab_len]
            #self.gui.lbl_db_user.config( text       =  lbl_text     )
            self.gui.show_item( "db_user", lbl_text  )

        else:

            if self.db.db_open:
                is_open = "Open"
            else:
                is_open = "Closed"

            lbl_text  = ( "Staus: " + is_open + spacer )[0:lab_len]
            #self.gui.lbl_db_status.config(  text    =  lbl_text     )
            self.gui.show_item( "db_status", lbl_text  )

            lbl_text  = ( "Host: " + self.parameters.db_host    + spacer )[0:lab_len]
            #self.gui.lbl_db_host.config(    text    =  lbl_text     )
            self.gui.show_item( "db_host", lbl_text  )

            lbl_text  = ( "DB: " + self.parameters.db_db    + spacer )[0:lab_len]
            #self.gui.lbl_db_db.config(    text    =  lbl_text     )
            self.gui.show_item( "db_db", lbl_text  )

            lbl_text  = ( "User: " + self.parameters.db_user    + spacer )[0:lab_len]
            #self.gui.lbl_db_user.config(    text    =  lbl_text     )
            self.gui.show_item( "db_user", lbl_text  )

    #-------------------------------------
    def open_com_driver( self ):
        """
        open the comm port driver
        updates gui , status available in driver
        !! add return True False
        """
        self.gui.print_info_string( "Opening comm port" )
        val   = self.com_driver.open()
        if val:
            status = "Open"
            self.gui.print_info_string( "Comm port open OK...." )
            self.logger.info( "open_driver, opened ok" )
            
        else:
            self.gui.print_info_string( "Comm port open NG" )
            status = "Open Failed"
            self.logger.info( "open failed, ignored" )

        self.gui.set_open( status )

        return

    #-------------------------------------------
    def close_driver( self ):
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
        beware using from ht
        """
        if self.parameters.echoSend:
            self.gui.print_send_string( adata )

        self.com_driver.send( adata )
        return

    # -------------------------------------------------------
    def receive( self,  ):   # combine with task?
        """
        call only from the helper, so no signaling ?? no could still be a problem
        receive data via the comm port
        display data
        return data   "" if no data
        -----
        receive only full strings ending with /n else
        accumulated in the driver /n is stripped
        """
        # for 232: breaks simulator

        data   = self.com_driver.getRecString( )
        # below but did not fix
#        if data == "":
#            pass
#        else:
#            #self.gui.print_rec_string( data )  # this post could be a problem, lets put back in helper ??
        return data

    # --------------------------------------------------
    def post_to_queue( self, action, function, args ):
        """
        self.post_to_queue( action, function, args )
        """
        loop_flag          = True
        ix_queue_max       = 10
        ix_queue          = 0
        while loop_flag:
            loop_flag      = False
            ix_queue  += 1
            try:
                #print( "try posting " )
                self.queue_to_helper.put_nowait( ( action, function, args ) )
            except queue.Full:

                # try again but give polling a chance to catch up
                print( "smart_terminal queue full looping" )
                self.logger.info( "queue to helper full looping" )
                # protect against infinit loop if queue is not emptied
                if self.ix_queue > ix_queue_max:
                    print( "too much queue looping" )
                    self.logger.info( "too much queue looping" )
                    pass
                else:
                    loop_flag = True
                    time.sleep( self.parameters.queue_sleep )

    # --------------------------------------------------
    def __rec_from_queue__( self, ):
        """
        take an item off the queue, think here for expansion may not be currently used.
        ( action, function, function_args ) = self.__rec_from_queue__()
        """
        try:
            action, function, function_args   = self.queue_fr_helper.get_nowait()
        except queue.Empty:
            action          = ""
            function        = None
            function_args   = None

        return ( action, function, function_args )

    #-------------------------------------------
    def do_send_list( self, a_list ):
        """
        this is out of date, need to generalize and move some of code to xxx_processing
        sends an list of data to update the uprocessor
        was for ir, probably no place in well monitor
        send arduino commands to load a new array of signals
        no still working for ir_processing see motor_processing where connected to button
        """
        # --- this needs to be moved to task some set up here then on there

        self.logger.info( "turn on sendList"  )
        self.send_list_ix     = 0

        #self.send_list  = [ 180, 920, 160, 1740, 160, 780,   160, 2840, 160, 1320, 160, 1340, 160, ] # 1180, 160, 2700, 160, 12780, 200, 920,   \
        #160, 2680, 160, 780, 160, 800, 160, 780, 160, 920, 160, 800, 140, 800,   \
        #  160 ]
        self.send_list        = a_list
        self.com_driver.send( "z\n" )
        self.list_send        = True    # if we were mult-threaded this would have to be here

        return

    # ----------------------------------------------
    def os_start_db( self,  ):
        """
        used as callback from gui button
        nice idea will not work in win run as admin.....
        """
        pass
#        from subprocess import Popen, PIPE  # since infrequently used ??
#
#        if self.parameters.start_db  == "": # no command to start db
#
#            pass # consider message box
#        else:
#            proc = Popen( [ self.parameters.start_db ] )

    # ----------------------------------------------
    def os_open_graph( self,  ):
        """
        used as/by callback from gui button.  Can be called form gt
        ?? do we want to sync the db both are using this would be nice
        could we integrate back into main app
        """
        print( "os_open_graph()" )
        from subprocess import Popen, PIPE  # since infrequently used ??
        proc = Popen( [ "python", self.parameters.grapher ] )

    # ----------------------------------------------
    def os_open_logfile( self,  ):
        """
        used as/by callback from gui button.  Can be called form gt
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
        open extended parameter file
        used as callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + self.parmeters_x + ".py"

        from subprocess import Popen, PIPE  # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

    # ------------------ callbacks for buttons cb_ -----------------
    # ----------------------------------------------
    def cb_test( self,  ):
        """
        call back for gui button -- this is for the test button, which
        may even be commented out
        code changes, may or may not work at any time
        """
        # this shows how to run stuff in the helper -- call thru queue, post to queue
        self.post_to_queue( "call", self.helper_thread.test_test_ports  , (  ) )

    # ----------------------------------------------
    def cb_gui_test_1( self,  ):
        """
        call back for gui button
        """
        print( "cb_gui_test_1" )
        self.helper_thread.toggle_lock()

    # ----------------------------------------------
    def cb_gui_test_2( self,  ):
        """
        call back for gui button
        """
        # TASK list is gone self.task_list.stop_auto( )

    # ----------------------------------------------
    def cb_gui_test_3( self,  ):
        """
        call back for gui button
        """
        #self.task_list.stop_auto( )
        #self.gh_graphing.testGraph()
        print( "cb_gui_test_3 commented out " )

    # ----------------------------------------------
    def ports( self,  ):
        """
        probe for ports, not finished  ??
        post to receive area
        windows 10 seems to break come back empty
        """
        ports   = self.com_driver.list_available()
        self.gui.print_info_string( "Reported Ports: \n" )
        if len( ports ) == 0:
            self.gui.print_info_string( "None \n" )
        else:
            for i_port in ports:
                self.gui.print_info_string( i_port[0] )
                self.gui.print_info_string( "\n" )

        self.close_driver()

        self.gui.print_info_string( "Probe Ports: \n" )
        ports  = self.com_driver.probe_available( self.parameters.port_list )
        ix_line = 0
        for i_port in ports:
            ix_line += 1
            self.gui.print_info_string( str( i_port ) )
            if ix_line == 10:
                ix_line = 0
                self.gui.print_info_string( "\n" )

# ----------------------------------------------
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
class ExceptionRecord():
    """
    use to keep a record of exceptions in app

    """
    def __init__(self, a_time ):
        # Set some exception infomation
        # keep track of where we are we increment on each access, this is how val are chosen

        self.ex_time      = a_time  #   on, off, repeats

        #print "self.max_x " + str( self.max_x )   print "self.max_y " + str( self.max_y )
        #sys.stdout.flush()
    # ----------------------------------------
    def get_next_send(self, ):
        """
        place holder
        """
        # increment first
        #print "get_next_send( )"
        #sys.stdout.flush()

        data = "no data in data "
        return data

# =========================== Class ATask =================================
if __name__ == '__main__':
    """
    run the app
    """
    a_app = SmartTerminal(  )
    #a_app.test()
    print( "here we are done with smart terminal " )
    sys.stdout.flush()
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



