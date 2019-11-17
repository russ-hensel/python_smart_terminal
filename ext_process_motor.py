# -*- coding: utf-8 -*-


#        This is an object that extends the function of the smart terminal to
#        do some special processing for the arduino MPMotor program
#        This is primarily an extension to the GUI, other extensions in the send area
#        are done by parameters, which might better be located here.
#        Pretty junk code, but works, lot left over from IR terminal
#        Does have a task list for auto processing, more of a demonstration than
#        useful.

# for smart_terminal
# drive this off of parameters, have a few special buttons for downloads


#       reset the motor driver
#       set the no of coils
#       set the no of steps in coil cycle  -- or let the arduino firgur it out from coil cycles
#       set the cycle values for coil n
#       set time delay for steps in cycle
#       set the cycle direction
#       go for some number of steps
#       report/versin/help


import logging
#from    Tkinter import *   # is added everywhere since a gui assume tkinter namespace
import sys
import tkinter as Tk

import abc
import abc_def
# from abc_base import PluginBase
from app_global import AppGlobal


# ---------------------------

import smart_terminal

#sys.path.append( r"../rshlib" )
#sys.path.append( r"../irtools" )
#sys.path.append( r"../ir_test_data" )
#sys.path.append( r"../irtools/sony" )


def   test_func( a_string ):
    print( a_string )


class ButtonAction( object ):
    """
    this may become an abstract class for plug in button actions in the smart terminal, a bit like processing add to the array
    need ref to my processing object probably
    hold info to implement a button in the gui
    looks like a struct so far
    """

    def __init__( self, a_processor, a_name, a_function ):
        self.processor       =  a_processor     # why this it is a mini controller where used?
        self.name            =  a_name
        self.function        =  a_function      # where are the arguments elswhere in the thing in function_args with set_args
        self.function_args   = [ self.name, "I am an argument", "and another " ]
        self.button          = None

    def set_button( self, a_button ):
        """
        use when button actually created ( or move a factory in here??)
        """
        self.button          = a_button

    def set_args( self, a_args ):
        self.function_args   = a_args


class MotorProcessing( abc_def.ABCProcessing ):

#class MotorProcessing( object):
    """
    add on for motor driver smart_termial
    implements abstract class
    class SubclassImplementation( PluginBase ):

    """
    def __init__( self,  ):    #iranalyzers ):

        self.controller         = AppGlobal.controller
        self.parameters         = AppGlobal.parameters

        self.logger             = logging.getLogger( self.controller.logger_id + ".motor" )   # assign to logger or get all the time does logger have aname or does this assign
        self.logger.info( "in class MotorProcessing init for the smart_terminal" )

        # ------------------------- this is a data driven way to do this but may not be a great method move to add_gui

        self.button_actions    = []        # list of ButtonAction  s define buttons both for gui and their actions
        # most of this could be down in the add_gui
        # use this to create buttons and define their actions, functions should take what for args, lists???

        self.button_var          = None    # needs to be created after root
        # self.controller.gui.root.button_var          = Tk.StringVar()
        # self.button_var.set( self.controller.parameters.rb_num_on )

        self.current_action       = None

    # -------------------------------------------------
    def do_send_list( self, a_list ):  #
        """
        test for now to make the terminal send a list  -- may be called an array elsewhere
        """
        self.controller.do_send_list( a_list )

    # -------------------------------------------------
    def add_gui( self, parent, ):  # if this were a class then could access its variables later
        """
        make frame for motor control and return it
        add buttons for different stepping now for unipolar in 3 modes, expand
        """
        self.button_var          = Tk.IntVar()   # must be done after root is created

        ret_frame        = Tk.Frame( parent, width = 600, height=400, bg = "gray", relief = Tk.RAISED, borderwidth=1 )

        button_actions      = []
        # ------------------------------------------
        the_steping  =  [ "z",     # coils go down phase across
                                   "a1 0 0 0",
                                   "a0 1 0 0",
                                   "a0 0 1 0",
                                   "a0 0 0 1",
                                   "c4",
                                   ]

        a_button_action         = ButtonAction( self, "Full Step\n1 Phase", self.do_send_list )
        a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )


        # ------------------------------------------
        the_steping  =  [ "z",     # coils go down phase across
                                   "a1 0 0 1",
                                   "a1 1 0 0",
                                   "a0 1 1 0",
                                   "a0 0 1 1",
                                   "c4",
                                   ]

        a_button_action         = ButtonAction( self, "Full Step\n2 Phase", self.do_send_list )
        a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # ------------------------------------------
        half_steping  =  [ "z",   "a1 1 0 0 0 0 0 1",
                                  "a0 1 1 1 0 0 0 0",
                                  "a0 0 0 1 1 1 0 0",
                                  "a0 0 0 0 0 1 1 1",
                                  "c4"
                                  ]

        a_button_action         = ButtonAction( self, "Half\nSteping", self.do_send_list )
        a_button_action.set_args( half_steping )
        button_actions.append(   a_button_action )

        # -------------------------
        a_button_action         = ButtonAction( self, "Start: Find Arduino Motor Processing", self.cb_find_arduino  )
        # a_button_action.set_args( ( "call", self.controller.helper_thread.test_test_ports  , (  ) ) )
        button_actions.append(   a_button_action )

        # -------------------------

        self.button_actions      = button_actions  # controls creation and actions of additional buttons

        color          = "blue"
        a_frame        = Tk.Frame( ret_frame, width = 600, height=200, bg = "gray", relief = Tk.RAISED, borderwidth=1 )

        a_frame.pack( side = Tk.LEFT)     # this seems pretty good
        for ix, i_button_action  in  enumerate( self.button_actions ):
                a_button = Tk.Button( a_frame, width=10, height=2, text = i_button_action.name, wraplength = 60 )
                a_button.bind( "<Button-1>", self.do_button_action )
                a_button.grid(  row = int( ix / 8 ) + 1, column = ix%8, sticky ='E' + "W" )
                a_frame.grid_columnconfigure( ix, weight=1 )
                i_button_action.set_button( a_button )
                # self.actButtons.append( a_button )
                #print buttonX.cget('bg')   # "SystemButtonFace"

        # push buttons, see copy for deleted code

#        b_frame        = Tk.Frame( ret_frame, width = 300, height=200, bg = "blue", relief = Tk.RAISED, borderwidth=1 )
#        b_frame.pack(  side=Tk.TOP, expand = Tk.YES, ) #fill=Tk.Y ))
#
#        ix_value = 0
#        rb0   =  Tk.Radiobutton( b_frame, text="off",              variable = self.button_var, value = ix_value )
#        rb0.grid( row=0,  column = ix_value )
#
#        ix_value += 1
#        rb1   =  Tk.Radiobutton( b_frame, text="unformmated",      variable = self.button_var, value = ix_value )
#        rb1.grid( row=0,  column = ix_value )
#
#        ix_value += 1
#        rb2   =  Tk.Radiobutton( b_frame, text="CAP",              variable = self.button_var, value = ix_value )
#        rb2.grid( row=0,  column = ix_value )
#
#        ix_value += 1
#        self.lower_rb   = ix_value   # used in controller
#        rbx   =  Tk.Radiobutton( b_frame, text="lower",            variable = self.button_var, value = ix_value )
#        rbx.grid( row=0,  column=ix_value )
#
#        ix_value += 1
#        self.no_ws_rb    = ix_value
#        rbx   =  Tk.Radiobutton( b_frame, text="No WS",             variable = self.button_var, value=ix_value )
#        rbx.grid( row=0,  column = ix_value )
#
#        ix_value += 1
#        self.url_to_wiki   = ix_value   # used in controller
#        rbx   =  Tk.Radiobutton( b_frame, text="url to wiki",       variable = self.button_var, value = ix_value )
#        rbx.grid( row=0,  column=ix_value )
#
#        ix_value += 1
#        self.comma_sep_rb   = ix_value   # used in controller
#        rbx   =  Tk.Radiobutton( b_frame, text="comma sep",        variable = self.button_var, value = ix_value )
#        rbx.grid( row=0,  column=ix_value )
#
#        ix_value += 1
#        self.undent_rb      = ix_value
#        rbx   =  Tk.Radiobutton( b_frame, text="undent",           variable = self.button_var, value = ix_value )
#        rbx.grid( row=0,  column=ix_value )
#
#        ix_value += 1
#        rbx   =  Tk.Radiobutton( b_frame, text="test",             variable = self.button_var, value=ix_value )
#        rbx.grid( row=0,  column=ix_value )

        return ret_frame

    #----------------------------------------------
    def do_button_action( self, event ):
        """
        think this works but is odd we can actually do function based on the widget, and this does not
        do a good job if invalid button is called
        easy to add functions that look at the button text but could actually use the button instance self.button_actions.
        """
        for ix, i_button_action in  enumerate( self.button_actions ):
            text     = i_button_action.name       # or i_button_action.button == event.widget  !! probably better
            btext    = event.widget[ "text" ]
            if event.widget == i_button_action.button:
                #event.widget.config( bg="gray" )   # this may blink the button when the action happens look into this
                i_button_action.function( i_button_action.function_args )
                # self.current_action =  act    # not sure what did look in old cod
                break

    #----------------------------------------------
    def cb_find_arduino( self, event ):
        # always post to queue to not call directly need to keep polling going
        # helper_thread   = self.controller.helper_thread
        #helper_thread.find_arduino()
        self.controller.post_to_queue( "call", self.controller.helper_thread.find_arduino  , (  ) )

# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    print( "" )
    print( " ========== starting SmartTerminal from motor_processing.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )
# ======================= eof ===========================



