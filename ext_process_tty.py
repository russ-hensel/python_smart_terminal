# -*- coding: utf-8 -*-


#import sys
import logging
import time
import abc_def
import tkinter as Tk
import collections

#Person = collections.namedtuple('Person', 'name age gender')
#
#print 'Type of Person:', type(Person)
#
#bob = Person(name='Bob', age=30, gender='male')
#print '\nRepresentation:', bob
#
#jane = Person(name='Jane', age=29, gender='female')
#print '\nField by name:', jane.name
#
#print '\nFields by index:'
#for p in [ bob, jane ]:
#    print '%s is a %d year old %s' % p

# -------------- local libs ------------------

# sys.path.append( "../rshlib" )

#import misc_stuff
#import smart_terminal

#this does the data processing and csv file save for the green_house application
#some of operation comes from parameters

# ================= Class =======================
#
class TTYProcessing( abc_def.ABCProcessing ):
    """
    This extension takes in ascii and emits baudot ( or a veriant to an arduino )
    """
    # ------------------------------------------
    def __init__( self,  controller  ):
        """
        create processing class
        call: gui thread
        args: controller class the main app
        ret: zip
        """

        AppGlobal.abc_processing = self
        self.controller          = controller
        self.parameters          = controller.parameters
        self.helper_thread       = controller.helper_thread
        self.logger              = logging.getLogger( self.controller.logger_id + ".TTYProcessing")

        self.logger.debug( "in class TTYProcessing init" ) # logger not currently used by here

        self.time          = time.time() # set in set_time -- taken as same for all measurements
        self.next_csv_line = ""
        #self.last_time     = None
        self.last_time     = time.time()

        """
        need assci que
        need baduo queue
        need emit queus

        to tell arduino to send send ">baudot.......<cr>"  at least for now
        be able to make quueus signal to wait

        """
        baudot_queue  = queue.Queue( 20 ) # !! parm size




        Baudot = collections.namedtuple( 'Baudot', 'shift code')   # shift is shift state: l letter, n numeric, both

        # may need arg to be byte so can do num operations
        self.ascii_to_baudot_dict    = { "a": Baudot( shift = "l", code = 0 ), "b": Baudot( shift = "l", code = 0 ),
                                         "c": Baudot( shift = "l", code = 0 ), "d": Baudot( shift = "l", code = 0 ), }

#        "e" "f" "g" "h" "i" "j" "k" "l" "m" "n" "o" "p" "q" "r"
#
#                                        "s" "t" "u" "v" "w" "x" y z   }
        # not in parameters because not so easily changed these just validate recieved data
        # these are the numbers of measurements of each type.
        # not all are implemented


    # ----------------------------------------
    def add_gui( self, parent, ):
        """
        call: gui thread
        args: parent = the parent frame for this frame
        ret: the frame we have created.
        additional gui for this extension
        creates a couple of buttons with call backs to methods within this class, which
        also run in the GUI thread
        """
        self.button_var   = Tk.IntVar()   # must be done after root for Tkinter is created

        ret_frame         = Tk.Frame( parent, width = 600, height=200, bg = self.parameters.bk_color, relief = Tk.RAISED, borderwidth=1 )

        self.button_action_list    =  misc_stuff.ButtonActionList( )  # this is a gui construction helper that helps manage the call back functions
        # ------------------------------------------

        self.button_action_list.create_action( "Helper: Find and Monitor Arduino", self.cb_find_and_monitor_arduino )
        self.button_action_list.create_action( "Interrupt Helper", self.cb_end_helper )

        a_frame        = Tk.Frame( ret_frame, width = 600, height=200, bg = "gray", relief = Tk.RAISED, borderwidth=1 )
        a_frame.pack( side = Tk.LEFT)

        self.button_action_list.create_place_in_frame( a_frame )

        return ret_frame

    # ----------------------------------------
    def add_baudot_queue( self,  a_char ):
        """
        or is this where we convert, maybe later
        a_char should actually be a Baudot tuple
        """

        self.ascii_to_baudot_dict[]

        baudot_queue.q.put( a_char )





    # ----------------------------------------
    def add_baudot_queue( self,  a_char ):
        """
        """
        pass



    # ----------------------------------------
    def add_baudot_queue( self,  a_char ):
        """
        """
        pass


    # ----------------------------------------

    # ----------------------------------------


    # ----------------------------------------
    def monitor_arduino_loop( self ):
        """
        assumes port opened successfully
        infinite loop
        call: run in ht not controller
        ret: only on failure, probably should be exception
        """
        # typically stat functions with this sort of thing
        helper_thread    = self.controller.helper_thread
        # gui              = self.controller.gui
        # helper_label     = gui.helper_label  no direct access to gui
        #helper_thread.print_info_string( "Starting Arduino Monitoring..." )
        helper_thread.post_to_queue(  "info", None, "Starting Arduino Monitoring..." )    # rec send info
        #helper_thread.release_gui_for( 5 )
        # beware long v response wait a bit here say 10 sec
        helper_thread.sleep_ht_for( 10 )

        while True:
            self.set_time( )
            send_rec_wait  = 10.   # a long time should slow down only if a problem
            rec_data       = helper_thread.send_receive( "a", send_rec_wait  )  # throw except if times out
            ix  = rec_data.find( "ok", 0, len( rec_data ) )
            if ix == -1:
                msg = "failed to find ok got: >>>" + rec_data + "<<<"
                self.logger.error( msg )
                print( msg  )   # !! use log  print in recive area
                # need to inform gui and probably throw exception !!
                return   False   # probably should be infinite except

            #self.controller.send( "t\n" )
            rec_data       = helper_thread.send_receive( "t", send_rec_wait  )  # throw except if times out
            self.process_temp_line( rec_data )

            rec_data       = helper_thread.send_receive( "h", send_rec_wait  )  # throw except if times out
            self.process_humid_line( rec_data )

            helper_thread.sleep_ht_for( 10. )

    # ----------------------------------------
    def find_and_monitor_arduino( self ):
        """
        call: ht

        """
        # typically start with these 2 lines
        helper_thread    = self.controller.helper_thread
        #gui              = self.controller.gui
        #helper_label     = gui.helper_label

        helper_thread.sleep_ht_with_msg_for( 10, "Beginning find and Monitor Arduino... ", 5, True )

        ok, a_port = helper_thread.find_arduino( )

        #helper_thread.release_gui_for( 0 )
        if ok:
             #helper_label.config( text = "found arduino on " + a_port )    # helper_thread
             #self.controller.gui.show_item( "helper_info", "found arduino on " + a_port )
             helper_thread.print_info_string(  "found Arduino on " + a_port )
             self.monitor_arduino_loop()
        else:
             #helper_label.config( text = "arduino not found " )
             #self.controller.gui.show_item( "helper_info", "arduino not found " )
             helper_thread.print_info_string(   "Error: Arduino not found -- looked for " + self.parameters.arduino_version ) # + a_port )
             return


    # ------------------------------------------
    def set_time( self,  ):
        """
        set the aquisition time of the data init the csv line
        when is this ever called or updated: aquire data
        """
        self.time           = time.time()
        self.next_csv_line  = str( self.time )

    # ------------------------------------------


    #----------------------------------------------
    def cb_find_and_monitor_arduino( self, a_list ):
        """
        button call back from gui
        call: gui thread
        calls function in the helper thread by using the controller to post the function over to the helper thread
        """
        self.controller.post_to_queue( "call", self.find_and_monitor_arduino, (  ) )
#    # -------------------------------------------------
#    def cb_test_test_ports( self, ignore ):
#
#        self.controller.post_to_queue( "call", self.controller.helper_thread.find_arduino  , (  ) )
    # -------------------------------------------------
    def cb_end_helper( self, ignore ):

        self.controller.post_to_queue( "call", self.controller.helper_thread.end_helper  , (  ) )

# ----------------------------------------------------------

#import test_controller

if __name__ == '__main__':
    """
    call main app from this file
    """
    print( "" )
    print( " ========== starting SmartTerminal from gr_csv_processing.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )



# ======================= eof ======================================

