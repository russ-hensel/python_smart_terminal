# -*- coding: utf-8 -*-

"""
Purpose:
    support for SmartTerminal  smart_terminal.py  after testing add back to smart_plug
    provide rest of code with access to global variables and functions
    couple with care.
    for app smart_terminal

    typical use ------
    from app_global import AppGlobal

    self.parameters        = AppGlobal.parameters
    AppGlobal.parameters   = self
    for best version see: *>text D:\Russ\0000\python00\python3\_projects\readme_rsh.txt
"""

"""
 ** using os call seems to work ok for edit text.... in smart_terminal
"""

# import sys
import webbrowser
from   subprocess import Popen
from   pathlib import Path
import os
import psutil
from   tkinter import messagebox
import logging

# ----------------------------------------------
def addLoggingLevel( levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

     How to add a custom loglevel to Python's logging facility - Stack Overflow
     *>url  https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.__logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobbering of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       #raise AttributeError('{} already defined in logging module'.format(levelName))
       return   # assum already set up ok -- could cause error in contaminated environment

    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, *args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot )

# ------------------------
class NoLoggerLogger( object, ):
    """
    a temporary logger before we have a proper logger
    implement some of the methods of the logger
    just some of the protocol not all of this
    log(level, msg, *args, **kwargs)¶
    perhaps import module and use its constants which seem not to be
    CRITICAL 50 ERROR  40   WARNING 30  INFO  20  DEBUG 10 NOTSET 0

    """
    __log_later             = []         # tuples for logging after logger is set
    # ----------------------------------------------
    @classmethod
    def info( cls, msg ):
        """
        mirror logger.info in limited way
        """
        cls.log( logging.INFO, msg )

    # ----------------------------------------------
    @classmethod
    def debug( cls, msg ):
        """
        mirror logger.debug in limited way
        """
        cls.log( logging.DEBUG, msg )
    # ----------------------------------------------
    @classmethod
    def log( cls, level, msg, *args, **kwargs ):
        """
        mirror logger.log in limited way
        """
        arg_set  = ( level, msg, )  # not clear how to get rest, for now discard
        print( f"{arg_set[0]} >> {arg_set[1]}" )
        cls.__log_later.append( arg_set )

    # ----------------------------------------------
    @classmethod
    def log_saved_for_later( cls, logger ):
        """
        now have a logger so spit out the saved up stuff if any
        may or may not print
        ?? add some indent
        """
        for arg_set in cls.__log_later :
            print( f"log_saved_for_later {arg_set[ 0 ]} {arg_set[ 1 ]}" )
            logger.log( arg_set[ 0 ], arg_set[ 1 ] )

# ------------------------
class OSCall( object, ):
    """
    try to call os based on attempts with different utilities
    helps app be flexible across different operating systems or computers
    """
    #------------------------
    def __init__(self, command_list, ):
        """
        command list is the list of utilities to try, a list of strings


        """
        self.command_list = []     # all addition via function below
        self.add_command( command_list )

    # ----------------------------------------------
    def add_command( self, more_command_list ):
        """
        add a command(s)  ( more_command_list ) at the beginning of list and re init the list
        more_command_list may be None, a string, or list of strings
        call internally at init or externally ( parameters ) to add to list
        could add flag to add at either end ??
        return mutated state of self
        """
        print( f"adding {more_command_list}")
        if more_command_list is None:   # perhaps was here to reinit to zero length ?? for now a do nothing
            pass
            #self.command_list        = more_command_list     # [   r"D:\apps\Notepad++\notepad++.exe", r"gedit", r"xed", r"leafpad"   ]   # or init from parameters or put best guess first

        else:
            if type( more_command_list ) ==  str:
                more_command_list  = [ more_command_list ]
            # else we expect a list
            self.command_list = more_command_list + self.command_list

        self.ix_command          = -1
        self.working_command     = None
        print( f"command list now{self.command_list}")

    # ----------------------------------------------
    def get_next_command( self,  ):
        """
        what it says
        for internal use
        mutates self
        return item for list or None if cannot find one ( at end of list )
        """
        self.ix_command += 1
        if         self.ix_command >= len( self.command_list ):
            ret =  None
        else:
            ret =         self.command_list[ self.ix_command ]
#        print( f"command = { self.ix_command} {ret} ", flush = True )
        return ret

    # ----------------------------------------------
    def os_call( self, cmd_arg,  ):
        """
        make an os call, trying various utilities until one works
        this is the point of the whole class
        return nothing, may raise error
        """
        while True:   # will exit when it works or run out of editors
            a_command    = self.working_command
            if  a_command is None:
                a_command  = self.get_next_command( )

            if a_command is None:   # no commands left to try
                    msg = "Run out of editors to try"
#                   AppGlobal.__logger.error( msg )
                    raise RuntimeError( msg )   # or fail in some other where
                    break  # we are aread done
            try:
                if cmd_arg is None:
                    proc = Popen( [ a_command,  ] )
                else:
                    proc = Popen( [ a_command, cmd_arg ] )
                self.working_command  = a_command
                break  # do not get here if exception so command "worked "
            except Exception as excpt:  # this should let us loop ignoring exception
                pass
                msg     = ( f"os_call exception trying to use >{a_command}< with cmd_arg >{cmd_arg}< exception: {excpt}" )
                            # if exception proc not returned  f"\npopen returned {proc}" )
                AppGlobal.logger.debug( msg )

# ----------------------------------------------
class AppGlobal( object ):
    """
    Provides for global access to some application values.
    Singelton, implemented at class not instance level
    generally available to most of the application through the Controllers instance variable
    Use something like ( in controller )
    from   app_global import AppGlobal
    AppGlobal.controller = self
    """
    force_log_level         = 99    # value to force logging, high but not for errors
    fll                     = force_log_level   # shorthand
    # ----------------- set later, generally externally as objects check in
    controller              = None
    parameters              = None
    logger                  = None        # msg    = f"{}" AppGlobal.__logger.info( msg )
    logger_id               = None

    logger                  = NoLoggerLogger

    helper_thread           = None         # smart terminal helper  HelperThread
    helper_thread_ext       = None         # things like DDCProcessing depending on extension
    abc_processing          = None         # old helper_thread_ext phase thi one out

    graphing                = None
    db                      = None       # assigned in db.py ??
    gui                     = None

    clock_mode              = None       # for dd clock, init from parmeters


    # --- text editor
    text_editors            =  [ r"D:\apps\Notepad++\notepad++.exe", r"C:\apps\Notepad++\notepad++.exe", "notepad++.exe",
                                 r"gedit", r"xed", r"leafpad", r"mousepad", ]
    file_text_editor        = OSCall( text_editors,  )

    # --- file explorer
    # file_explorers  not in parmeters as yet
    file_explorers            = [ r"explorer", "nemo", "xfe", "pcmanfm", ]
    file_explorer           = OSCall( file_explorers ) #  add and parameters

    # time mode seems to need to be known only to ext_process_ddc clock, so not here, just there and init in parameters
    # this causes a problem if run twice from same shell .. !! work on this
    addLoggingLevel( "Notice", force_log_level, methodName = None)

    #--------------------------------
    def __init__(self,   ):
        """
        this is meant to be a singleton use class level only do not instantiate
        throw a exception if instantiated ??
        """
        y =1/0

    # ----------------------------------------------
    @classmethod
    def set_logger( cls, logger ):
        """
        set the system logger once setup, empty NoLoggerLogger

        """
        #print( "set logger" )
        cls.logger    = logger
        NoLoggerLogger.log_saved_for_later( logger )

    # ----------------------------------------------
    @classmethod
    def parameter_tweaks( cls,  ):
        """
        call if necessary at end of parameters -- may make init unnecessary
        AppGlobal.parameters needs to be populated
        """
        cls.file_text_editor.add_command( cls.parameters.ex_editor )
        print( f"parameter tweaks {cls.text_editors}" )  #

    # # ----------------------------------------------
    # could not get property decorator to work so will use set_logger at class level.
    # # must have property to use setter two for set and get, note name match
    # @classmethod
    # @property       # seems must be outer decorator


    # def logger( cls ):
    #     print( "********************************cls.__logger getter" )
    #     return cls.__logger

    # # ----------------------------------------------
    # @classmethod
    # @logger.setter

    # def logger( cls,  arg ):
    #     msg     = f"*****************************in setter for logger arg={arg}"
    #     cls.__logger   = arg
    #     if len( __log_later ) != 0:
    #         pass   # log all of old stuff

    #     return

    # ----------------------------------------------
    @classmethod
    def show_process_memory( cls, call_msg = "", log_level = None, print_it = False ):
        """
        log and/or print memory usage
        """
        process      = psutil.Process(os.getpid())    #  import psutil
        mem          = process.memory_info().rss
        # convert to mega and format
        mem_mega     = mem/( 1e6 )
        msg          = f"{call_msg}process memory = {mem_mega:10,.2f} mega bytes "
        if print_it:
            print( msg )
        if not ( log_level is None ):
            cls.__logger.log( log_level,  msg )
        msg           = f"{mem_mega:10,.2f} mega bytes "
        return ( mem, msg )

    # ----------------------------------------------
    @classmethod
    def log_if_wrong_thread( cls, id, msg = "forgot to include msg", main = True ):
        """
        debugging aid
        check if called by intended thread
        main thread must be set first
        ex:   AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )
        """
        on_main = ( id == cls.main_thread_id )

        if main:
            ok  = on_main
        else:
            ok = not( on_main )

        if not ok:
            msg    = f"In wrong thread = {cls.name_thread( id )}: + {msg}"
            cls.__logger.log( cls.force_log_level,  msg )

    # ----------------------------------------------
    @classmethod
    def name_thread( cls, id, ):
        """
        id is the threading id of the caller
        return thread name Main/Helper
        ex call:  AppGlobal.name_thread( threading.get_ident(),  )
        """
        if  cls.main_thread_id is None:
            y= 1/0   # cheap exception when main_thread not set up

        if id == cls.main_thread_id:
            ret = f"Main"
        else:
            ret = f"Helper"

        return ret

    # ----------------------------------------------
    @classmethod
    def thread_logger( cls, id, call_msg = "", log_level = None ):
        """
        debugging aid
        log a message, identifying which thread it came from
        ex call: AppGlobal.thread_logger( threading.get_ident(), "here we are", 50  )
        """
        thread_name   = cls.name_thread( id )
        msg           = f"in {thread_name} thread>> {call_msg}"

        if not ( log_level is None ):
            cls.__logger.log( log_level,  msg )

    # ----------------------------------------------
    @classmethod
    def about( cls,   ):
        """
		 show about box -- might be nice to make simple to go to url on it ( help button )
        """
        url   =  r"http://www.opencircuits.com/Python_Smart_Terminal"
        __, mem_msg   = cls.show_process_memory( )
        msg  = ( f"{cls.controller.app_name}  version:{cls.controller.version} \nmode: {cls.parameters.mode}"
                 f"\n  by Russ Hensel"
                 f"\nMemory in use {mem_msg} \nCheck <Help> or \n{url} \nfor more info." )
        messagebox.showinfo( "About", msg )

    # ----------------------------------------------
    @classmethod
    def os_open_txt_file( cls, txt_file ):
        """
        open a text file with system configured editor
        """
        cls.file_text_editor.os_call( txt_file )

     # ----------------------------------------------
    @classmethod
    def os_open_help_file( cls, help_file ):
        """
		what it says
        see parameters for different types of files and naming that will work with this
        """
        #help_file            = self.parameters.help_file
        if help_file.startswith( "http:" ) or help_file.startswith( "https:" ):
           ret  = webbrowser.open( help_file, new=0, autoraise=True )    # popopen might also work with a url
#           print( f"help http: {help_file} returned {ret}")
           return

        a_join        = Path(Path( help_file ).parent.absolute() ).joinpath( Path( help_file ).name )
#        print( f"a_join {type( a_join )} >>{a_join}<<" )

        #if a_join.endswith( ".txt" ):
        if a_join.suffix.endswith( ".txt" ):
            cls.os_open_txt_file( str(a_join) )
            return

        file_exists   = os.path.exists( a_join )
        print( f"file {a_join} exists >>{file_exists}<<" )
        #full_path     = Path( help_file ).parent.absolute()
#        print( f"a_join {a_join}" )
        help_file     = str( a_join )

        ret = os.popen( help_file )
#        print( f"help popopen  {help_file} returned {ret}")

    #--------------------------------
    @classmethod
    def state_info():
        """
        return some info as a list that might be diagnostic, print or log
        perhaps at end of app

        """
        info_list   = []
        #info_list   += AppGlobal.__dir__()
        info_list   += dir( AppGlobal )

        return info_list
        #AppGlobal.state_info( )

    #--------------------------------
    @classmethod
    def print_debug( cls, msg  ):  #
        """
        very temp   AppGlobal.print_debug( msg )
        all should be removed ??
        !! add a level or can the print output be added as a handler
        """
        if cls.__logger.getEffectiveLevel() <=  logging.DEBUG :
            print( msg, flush = True )
        cls.__logger.debug( msg )

# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching -- may not be good idea for a class level object
    """
    print( "" )
    print( " ========== starting SmartTerminal from smart_terminal.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )

# ======================== eof ======================