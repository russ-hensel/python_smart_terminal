# -*- coding: utf-8 -*-

import logging
import Tkinter
import importlib
import sys
#import os
import time

# ----------- my code  --------------------------
sys.path.append( "../rshlib" )

import db
import parameters
#import gui
#import gui_new
#import graphing
import data_point
#import gh_processing
#import gh_graphing

# ========================== Begin Class ================================
class TestController:
    """
    test controller for app components
    feeds on test data, uses db
    """
    def __init__(self ):

        self.app_name       = "Test controller -- Test component that need a controller"
        self.version        = "2016 12 12.3"

        self.parameters     = parameters.Parameters( self ) # open early may effect other

        self.logger_id      = self.parameters.logger_id
        self.logger         = self.config_logger()
        self.logger.info(" ====================== begin TestController ===============================")

        # self.app_name       += " Mode: " + self.parameters.mode    # std name ??
        self.db             = None
        # module and class name for the communications driver.
        self.comm_mod       = self.parameters.comm_mod
        self.comm_class     = self.parameters.comm_class

        self.connect        = self.parameters.connect
        self.mode           = self.parameters.mode


        # self.list_send    old from ir

        #self.starting_dir   = os.getcwd()    # or perhaps parse out of command line
        #self.prog_info()

        # some of this stuff might be controlled by mode parameters or the type of processing created
#        if self.connect     != "none":
#            self.db             = db.DBAccess( self, CSVMode = False )

        # this is important so check !! change to dict
        self.motor_processing  = None
        self.gh_processing     = None

        if   self.mode == "Terminal":
            print( "parameter says " +  self.mode )

        elif self.mode == "GreenHouse":
            print( "create greenhous processing " )
            self.gh_processing  = gh_processing.GHProcessing( self )

        elif self.mode == "MotorDriver":
            print( "create MotorDriver processing " )
            self.motor_processing  = motor_processing.MotorProcessing( self )

        elif self.mode == "IR":
            import ir_processing
            print( "create IRPprocessing " )
            self.ir_processing  = ir_processing.IRProcessing( self )

        elif self.mode == "RootCellar":
            print( "parameter says " +  self.mode )

        else:
            print( "parameter says? " + self.mode )

        self.looping        = False   # for our looping operations

#        self.task_list      = TaskList( self )
#
#        self.task_send_list = None     # list of things to be send via tasks see send_list_task
#        self.task_send_ix1  = -1       # index for above, better packaged in an object -- yes later
#        self.task_send_ix2  = -1       # index for above, better packaged in an object -- yes later

        self.com_driver       =  self.create_comm_class( self.parameters.comm_mod, self.parameters.comm_class )



        #self.db             = db.DBAccess( self, CSVMode = False )
        #self.gh_processing  = gh_processing.GHProcessing( self )


        # add test reading of files

        # self.process_test_data()

        # grapher  = gh_graphing.GraphDB( self )
        # grapher.testGraph()

        #self.db.dbClose()

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

        #logger.info("Done config_logger gh_processing") #  .debug   .info    .warn    .error

        return logger

    # --------------------------------------------------------
    def process_test_data_xxx( self, ):
        """
        not sure currently broken
        """
        test_time    = time.time()
        delta_time   = 10.
        self.logger.info("time between samples: " + str( delta_time ))
        with open( 'gh_test_data.txt' ) as f:
             lines = f.readlines()
        #or with stripping the newline character:

        #lines = [line.strip() for line in open('filename')]

        ix_type    = 0
        for ix in range( 0,4 ):
            for ix_line, i_line in enumerate( lines ):

                #print line.strip()
                if    ix_type == 0:
                    self.gh_processing.set_time( test_time )
                    #print "humid " + i_line
                    self.gh_processing.process_temp_line( i_line )

                elif  ix_type == 1:
                    #print "temp " + i_line
                    self.gh_processing.process_humid_line( i_line )

                elif  ix_type == 2:
                    #print "light " + i_line
                    self.gh_processing.process_light_line( i_line )

                elif  ix_type == 3:
                    #print "door " + i_line
                    self.gh_processing.process_door_line( i_line )
                    self.gh_processing.save_data(  )
                    #print "done line"
                    test_time   += delta_time
                    self.gh_processing.set_time( test_time )

                ix_type  += 1
                if  ix_type >= 4:                   # or modulo
                    ix_type = 0

    # ---- called from a gui
    def send( self, contents ):
        pass
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

        print( module_name + " " + class_name )
        a_class    = getattr(importlib.import_module(module_name), class_name)
        instance   = a_class( self )

        return instance

    # ============ test cases ===============

    # ---------------------------------------
    def test_run_gui( self ):

        self.win            = Tkinter.Tk()    # this is the tkinter root for the GUI

        if self.parameters.os_win:
            # this is causing problem in linux
            print "in windows setting icon"
            self.win.iconbitmap( self.parameters.icon )

        self.win.title( self.app_name + " version: " + self.version )
        self.myGui          = gui_new.GUI( self, self.win, )  # create the gui or view part of the program


        # --------------------------------------------------------
        #print "starting mainloop"
        self.win.mainloop()
        # print " init and we are all over....  "



# =======================================

if __name__ == '__main__':
        """
        run the app
        """
        a_app = TestController(  )


        a_app.test_run_gui()

        print "====== test done =============="




# ======================= eof =======================
















