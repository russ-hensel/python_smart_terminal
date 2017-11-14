# -*- coding: utf-8 -*-

import logging
import abc_def
import Tkinter as Tk

# -------------- local imports  ------------------

import misc_stuff

# ================= Class =======================
#
class ControlinoProcessing( abc_def.ABCProcessing ):
    """
    This extension exerts control and logs interactions with Controlino
    there is little data processing involved, just read write to Controlino.
    """
    # ------------------------------------------
    def __init__( self,  controller  ):

        self.controller    = controller
        self.parameters    = controller.parameters
        self.helper_thread = controller.helper_thread

        self.logger        = logging.getLogger( self.controller.logger_id + ".ControlinoProcessing")
        self.logger.debug( "in class ControlinoProcessing init" )

    # -------------------------------------------------
    def add_gui( self, parent, ):
        """
        call: gui thread
        args: parent = a frame in the main gui
        make frame for motor control and return it
        add buttons for whatever we want to do.
        """
        ret_frame           = Tk.Frame( parent,    width = 600, height=200, bg = "blue", relief = Tk.RAISED, borderwidth=1 )
        a_frame             = ret_frame

        self.button_action_list    =  misc_stuff.ButtonActionList( )
        # ------------------------------------------

        a_button_action         = misc_stuff.ButtonAction( "Helper: Blink Arduino", self.cb_blink )
        self.button_action_list.add_action( a_button_action )

        a_button_action         = misc_stuff.ButtonAction( "Helper: Interrupt",     self.cb_end_helper )
        self.button_action_list.add_action( a_button_action )

        self.button_action_list.create_place_in_frame( a_frame )

        return ret_frame

    # ----------------------------------------
    def blink_loop( self ):
        """
        call: helper thread
        assumes port already opened successfully
        infinite loop
        """
        # typically start functions with this sort of thing
        helper_thread    = self.controller.helper_thread
        gui              = self.controller.gui
        helper_label     = gui.helper_label

        helper_thread.print_info_string(  "Starting Blink Loop...works if port is open......" )    # rec send info

        while True:
            # next line essentially prints in the gui thread
            helper_thread.print_info_string( "Blink Loop...100" )
            # next line sends first arg thru com port and waits up to on sec
            # for a response for up to 1 sec ( else throw exception )
            helper_thread.send_receive( "BlinkPin 7 100", 1. )
            # sleep for three seconds while watching comm recieve and queue
            helper_thread.sleep_ht_for( 3. )

            helper_thread.print_info_string( "Blink Loop...500" )
            helper_thread.send_receive( "BlinkPin 7 500", 1. )
            helper_thread.sleep_ht_for( 3. )

    # -------------------------------------------------
    def cb_end_helper( self, ignore ):
        """
        call: gui thread
        this is a button call back - it makes in indirect call to the helper thread via a queue
        """
        self.controller.post_to_queue( "call", self.controller.helper_thread.end_helper  , (  ) )

    # -------------------------------------------------
    def cb_blink( self, ignore ):
        """
        call: gui thread
        this is a button call back - it makes in indirect call to the helper thread via a queue
        """
        self.controller.post_to_queue( "call", self.blink_loop, (  ) )

# ----------------------------------------------------------

if __name__ == '__main__':
    """
    run smart terminal from this file just here for convenience
    """
    print( "" )
    print( " ========== starting SmartTerminal from co_processing.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )


# ======================= eof ======================================

