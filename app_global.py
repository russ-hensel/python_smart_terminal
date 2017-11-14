# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 21:06:50 2017

@author: Russ
"""
#typical use
#from app_global import AppGlobal
#
#self.parameters        = AppGlobal.parameters
#AppGlobal.parameters    = self 

class AppGlobal( object ):
    """
    manages parameter values for all of Smart Terminal app and its various data logging
    and monitoring applications
    generally available to most of the application through the Controllers instance variable
    from   app_global import AppGlobal
    AppGlobal.controller = self
    """

    controller              = None
    parameters              = None
    logger                  = None
    logger_id               = None
    #scheduled_event_list    = "None"
    #helper                  = "None"
    graphing                = None 
    db                      = None       # assigned in db.py ??
    
    abc_processing          = None

    def __init__(self,   ):
        """
        this is meant to be a singleton use class level only do not instatiante 
        """

        #self.__mandatory__( controller )  # should always be used, never ( almost? ) modified
        #self.__set_default__()            # this is not required in general but lets you ignore the setting of more advanced parameters
        pass





# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    print( "" )
    print( " ========== starting SmartTerminal from smart_terminal.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )



# ======================== eof ======================