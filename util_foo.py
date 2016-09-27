# -*- coding: utf-8 -*-

 #  collection of utility functions, not for classes

import sys
import os
#import stat
import time
#import shutil
#import os,os.path
# import Queue
#import logging
import datetime

# --------------------------------------------

def prog_info( controller ):

    #logger_level( "util_foo.prog_info"  )
    logger  = controller.logger
    logger.info( "" )
    logger.info( "============================" )
    logger.info( "" )
    title       =   "Application: "  + controller.app_name + " " + controller.app_version
    logger.info( title )
    logger.info( "" )


    if len( sys.argv ) == 0:
        logger.info( "no command line arg " )
    else:
        ix_arg = 0
        for aArg in  sys.argv:   # enumerate probably the right way

            logger.info( "command line arg " + str( ix_arg ) + " = " + sys.argv[ix_arg])
            ix_arg += 1

    logger.info( "current directory " +  os.getcwd() )

    start_ts     = time.time()
    dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
    string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
    logger.info( "Time now: " + string_rep )
    # logger_level( "Parameters say log to: " + self.parameters.pylogging_fn ) parameters and controller not available can ge fro logger_level


    return


# --------------------------------------------

def prog_info_old( logger_level, title ):

    #logger_level( "util_foo.prog_info"  )

    logger_level( "" )
    logger_level( "============================" )
    logger_level( "" )

    logger_level( title )
    logger_level( "" )


    if len( sys.argv ) == 0:
        logger_level( "no command line arg " )
    else:
        ix_arg = 0
        for aArg in  sys.argv:   # enumerate probably the right way

            logger_level( "command line arg " + str( ix_arg ) + " = " + sys.argv[ix_arg])
            ix_arg += 1

    logger_level( "current directory " +  os.getcwd() )

    start_ts     = time.time()
    dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
    string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
    logger_level( "Time now: " + string_rep )
    # logger_level( "Parameters say log to: " + self.parameters.pylogging_fn ) parameters and controller not available can ge fro logger_level


    return

# ========================== eof =================================


# ========================== eof =================================
