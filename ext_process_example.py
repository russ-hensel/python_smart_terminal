# -*- coding: utf-8 -*-


# for smart_terminal ( see mode Example )
#        This is an object that extends the function of the smart terminal to
#        do some special processing.
#        This one is just an example of how to code them if you want to make one of your own.
#        You should also look at other examples typically named xxx_processing.py
#        It extends the gui, the automatic tasks, and the data processing ( including db access )
#        Of the smart terminal.
#
#        Will try to give lots of comments in this file
#.
#


import logging
#from    Tkinter import *   # is added everywhere since a gui assume tkinter namespace
import sys
import Tkinter as Tk

import abc
import abc_def
# from abc_base import PluginBase

# ---------------------------

import smart_terminal

sys.path.append( r"../rshlib" )
sys.path.append( r"../irtools" )
sys.path.append( r"../ir_test_data" )
sys.path.append( r"../irtools/sony" )


def   test_func( a_string ):
    print( a_string )


class ButtonAction( object ):
    """
    this may become an asbstract class for plug in button actions in the smart terminal, a bit like processing add to the array
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


class ExampleProcessing( abc_def.ABCProcessing ):
    """
    add on for smart_termial
    implements abstract class
    """
    def __init__( self, controller ):    #iranalyzers ):

        self.controller         = controller
        self.parameters         = controller.parameters

        self.logger             = logging.getLogger( self.controller.logger_id + ".example" )   # assign to logger or get all the time does logger have aname or does this assign

        self.logger.info( "in class ExamplerProcessing init for the smart_terminal" )

        self.task_list          = None

        self.make_task_list()

        # ------------------------- this is a data driven way to do this but may not be a great method move to add_gui

        self.button_actions    = []        # list of ButtonAction  s define buttons both for gui and their actions
        # most of this could be down in the add_gui
        # use this to create buttons and define their actions, functions should take what for args, lists???

        self.button_var          = None    # needs to be created after root
        # self.controller.gui.root.button_var          = Tk.StringVar()
        # self.button_var.set( self.controller.parameters.rb_num_on )
        #------ constants for controlling layout ------

        #Button names
        # for the ir analizer pretty much dead
        self.BN_PRINT_SAMPLES     = "Send Array a"
        self.BN_PRINT_MAJORITY    = "MPMotor Print Majority"
        self.BN_PRINT_AVE         = "Print Average"
        self.BN_PRINT_FREQ        = "Print Freq"

        self.BN_COPY_SAMPLES      = "Copy Samples"
        self.BN_COPY_MAJORITY     = "Copy Majority"
        self.BN_COPY_AVE          = "Copy Average"
        self.BN_COPY_FREQ         = "Copy Freq"
        self.BN_CMP_MA            = "Cmp M<>A"

        self.BN_DN_MA             = "DnLd Majority"
        self.BN_DN_AV             = "DnLd Average"

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

        ret_frame        = Tk.Frame( parent, width = 300, height=200, bg = "gray", relief = Tk.RAISED, borderwidth=1 )




        button_actions      = []
        # ------------------------------------------
        the_steping  =  [ "z",     # coils go down phase across
                                   "a1 0 0 0",
                                   "a0 1 0 0",
                                   "a0 0 1 0",
                                   "a0 0 0 1",
                                   "c4",
                                   ]

        a_button_action         = ButtonAction( self, "Simple\nSteping", self.do_send_list )
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

        # ------------------------------------------
        the_steping  =  [ "z",     # coils go down phase across
                                   "a1 0 0 1",
                                   "a1 1 0 0",
                                   "a0 1 1 0",
                                   "a0 0 1 1",
                                   "c4",
                                   ]

        a_button_action         = ButtonAction( self, "Full\nSteping", self.do_send_list )
        a_button_action.set_args( the_steping )
        button_actions.append(   a_button_action )

        # self.iranalyzers         = button_actions   # phase out iraanalyzers

        self.button_actions      = button_actions  # controls creation and actions of additional buttons

        color          = "blue"
        a_frame        = Tk.Frame( ret_frame, width = 300, height=200, bg = "gray", relief = Tk.RAISED, borderwidth=1 )
        a_frame.pack(  side=Tk.TOP, expand = Tk.YES, ) #fill=Tk.Y ))
        for ix, i_button_action  in  enumerate( self.button_actions ):
                a_button = Tk.Button( a_frame, width=10, height=2, text = i_button_action.name, wraplength = 60 )
                a_button.bind( "<Button-1>", self.do_button_action )
                a_button.grid(  row = ( ix / 4 ) + 1, column = ix%4, sticky ='E' + "W" )
                a_frame.grid_columnconfigure( ix, weight=1 )
                i_button_action.set_button( a_button )
                # self.actButtons.append( a_button )
                #print buttonX.cget('bg')   # "SystemButtonFace"
        b_frame        = Tk.Frame( ret_frame, width = 300, height=200, bg = "blue", relief = Tk.RAISED, borderwidth=1 )
        b_frame.pack(  side=Tk.TOP, expand = Tk.YES, ) #fill=Tk.Y ))

        ix_value = 0
        rb0   =  Tk.Radiobutton( b_frame, text="off",              variable = self.button_var, value = ix_value )
        rb0.grid( row=0,  column = ix_value )

        ix_value += 1
        rb1   =  Tk.Radiobutton( b_frame, text="unformmated",      variable = self.button_var, value = ix_value )
        rb1.grid( row=0,  column = ix_value )

        ix_value += 1
        rb2   =  Tk.Radiobutton( b_frame, text="CAP",              variable = self.button_var, value = ix_value )
        rb2.grid( row=0,  column = ix_value )

        ix_value += 1
        self.lower_rb   = ix_value   # used in controller
        rbx   =  Tk.Radiobutton( b_frame, text="lower",            variable = self.button_var, value = ix_value )
        rbx.grid( row=0,  column=ix_value )

        ix_value += 1
        self.no_ws_rb    = ix_value
        rbx   =  Tk.Radiobutton( b_frame, text="No WS",             variable = self.button_var, value=ix_value )
        rbx.grid( row=0,  column = ix_value )

        ix_value += 1
        self.url_to_wiki   = ix_value   # used in controller
        rbx   =  Tk.Radiobutton( b_frame, text="url to wiki",       variable = self.button_var, value = ix_value )
        rbx.grid( row=0,  column=ix_value )

        ix_value += 1
        self.comma_sep_rb   = ix_value   # used in controller
        rbx   =  Tk.Radiobutton( b_frame, text="comma sep",        variable = self.button_var, value = ix_value )
        rbx.grid( row=0,  column=ix_value )

        ix_value += 1
        self.undent_rb      = ix_value
        rbx   =  Tk.Radiobutton( b_frame, text="undent",           variable = self.button_var, value = ix_value )
        rbx.grid( row=0,  column=ix_value )

        ix_value += 1
        rbx   =  Tk.Radiobutton( b_frame, text="test",             variable = self.button_var, value=ix_value )
        rbx.grid( row=0,  column=ix_value )

        return ret_frame

    #----------------------------------------
    def make_task_list( self ):
        """
        for now use old stuff

        """
        self.make_tasks_for_green_house( )

    # ----------------------------------------
    def make_tasks_for_green_house( self, ):
        """
        !! have tasks ready for test
        make tasks for green house, uses some stuff in
        parameters
        status, under development
        """
        print( "just a test make tasks for green house " )
        self.logger.debug( "motor_processing: make_tasks_for_green_house" )

        self.task_list    = smart_terminal.TaskList( self.controller )

        self.task_list.reset_tasks()

        # open port,
        need_me  = smart_terminal.ATask(   task_list  =  self.task_list,
                          task_trans       = self.task_list.task_open_trans,
                          task_rec         = self.task_list.task_open_rec,
                          task_special     = self.task_list.task_special_exception,
                          task_time_error  = self.task_list.task_special_exception,
                          repeats          = 1,
                          time_start       = 2,   time_delta = 5, time_error = 100  )
        # check version
        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
                          task_trans       = self.task_list.task_version_trans,
                          task_rec         = self.task_list.task_version_rec,
                          task_special     = self.task_list.task_special_exception,
                          task_time_error  = self.task_list.task_special_exception,
                          repeats          = 1,
                          time_start       = 5,   time_delta = 5, time_error = 10  )

        # print message
        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
                          task_trans       = self.task_list.task_print_trans,
                          task_rec         = self.task_list.task_print_rec,
                          task_special     = self.task_list.task_special_exception,
                          task_time_error  = self.task_list.task_special_exception,
                          repeats          = 1,
                          time_start       = 5,   time_delta = 5, time_error = 10  )
        need_me.set_msg( "this is message 1" )


        # print message
        need_me  = smart_terminal.ATask(      task_list  =  self.task_list,
                          task_trans        = self.task_list.task_print_trans,
                          task_rec          = self.task_list.task_print_rec,
                          task_special      = self.task_list.task_special_exception,
                          task_time_error   = self.task_list.task_special_exception,
                          repeats           = 1,
                          time_start        = 1,   time_delta = 5, time_error = 10  )
        need_me.set_msg( "this is message 2" )

        # print message
        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
                          task_trans       = self.task_list.task_print_trans,
                          task_rec         = self.task_list.task_print_rec,
                          task_special     = self.task_list.task_special_exception,
                          task_time_error  = self.task_list.task_special_exception,
                          repeats          = 1,
                          time_start       = 1,   time_delta = 5, time_error = 10  )
        need_me.set_msg( "this is message 3" )


        # aquire data  -- but wait after version
        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
                          task_trans       = self.task_list.task_gh_trans_aquire,
                          task_rec         = self.task_list.task_gh_rec_aquire,
                          task_special     = self.task_list.task_special_exception,
                          task_time_error  = self.task_list.task_special_exception,
                          repeats          = 1, # = 0 infinite loop
                          time_start       = 5,   time_delta = .1, time_error = 10  )

        # get temperature
        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
                          task_trans       = self.task_list.task_gh_trans_temp,
                          task_rec         = self.task_list.task_gh_rec_temp,
                          task_special     = self.task_list.task_special_exception,
                          task_time_error  = self.task_list.task_special_exception,
                          repeats          = 1, # = 0 infinite loop
                          time_start       = .1,   time_delta = .1, time_error = 10  )

        # get temperature
        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
                          task_trans       = self.task_list.task_gh_trans_humid,
                          task_rec         = self.task_list.task_gh_rec_humid,
                          task_special     = self.task_list.task_special_exception,
                          task_time_error  = self.task_list.task_special_exception,
                          repeats          = 1, # = 0 infinite loop
                          time_start       = .1,   time_delta = .1, time_error = 10  )

        # go back !!!!!!!!
        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
                          task_trans       = self.task_list.task_go_back_n,
                          task_rec         = self.task_list.task_go_back_n,
                          task_special     = self.task_list.task_special_exception,
                          task_time_error  = self.task_list.task_special_exception,
                          repeats          = 0, # = 0 infinite loop -- but not for go back
                          time_start       = .1,   time_delta = 5, time_error = 10  )
        need_me.set_msg( "task_go_back_n " )
        need_me.set_TVO( 3 )

        # ====================== end of loop ========================
#
#        # close port, this is normally the never occuring end
#        need_me  = smart_terminal.ATask( self, task_trans      = self.task_close_trans,    task_rec         = self.task_close_rec,
#                          task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
#                          repeats         = 1, # = 0 infinite loop
#                          time_start      = .1,   time_delta = 5, time_error = 10  )
#
#        # print message
#        need_me  = smart_terminal.ATask( self, task_trans      = self.task_print_trans,      task_rec         = self.task_print_rec,
#                          task_special    = self.task_special_exception,  task_time_error  = self.task_special_exception,
#                          repeats         = 1,
#                          time_start      = 5,   time_delta = 5, time_error = 10  )
#
#        need_me.set_msg( "this is message 999" )
#
        return  self.task_list

#    #----------------------------------------
#    # both the next 2 functions finall call doCurrent, they just set up the context
#    def doButtonIra( self, event):
#        """
#        easy to add functions that look at the button text
#        """
#        for ix, anal in  enumerate( self.iranalyzers ) :
#            text     = anal.name
#            btext    =  event.widget["text"]
#            if text ==  btext:
#                self.current_iranalyzer =  anal
#                use_anal = anal
#                break
#
#        for b  in ( self.gui_buttons ):
#            b.config( bg= "white"  )
#        event.widget.config( bg="gray" )
#
#        anal.copy_average()
#        #print "broke with ", btext
#        self.doCurrent(  )

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

#----------------------------------------
# does the current action set up by the prior 2 functins
# left over from IR Terminal, might be of use when reimplemented.
    def doCurrent( self ):
        """
        do current action on current data set
        with redirected output to my gui
        """
        # the download buttons
        if self.current_iranalyzer == None:
            return

        if   self.current_action == self.BN_DN_AV:
               self.controller.sendArray( self.current_iranalyzer.get_majority() )
               return

        elif self.current_action == self.BN_DN_MA:
               self.controller.sendArray( self.current_iranalyzer.get_average() )
               return

        # these buttons redirect sys out
        try:
            #sys.stdout.flush()
            #sys.stdout = self.save_redir

            if   self.current_action == self.BN_PRINT_SAMPLES:
                   self.current_iranalyzer.print_samples()
                   #sys.stdout.flush()

            elif self.current_action == self.BN_PRINT_MAJORITY :
                   self.current_iranalyzer.print_majority()
                   #sys.stdout = self.save_sys_stdout

            elif self.current_action == self.BN_PRINT_AVE:
                   self.current_iranalyzer.print_average()

            elif self.current_action == self.BN_PRINT_FREQ:
                   self.current_iranalyzer.print_freq()

            elif   self.current_action == self.BN_COPY_SAMPLES:
                   self.current_iranalyzer.copy_samples()
                   sys.stdout.flush()

            elif self.current_action == self.BN_COPY_MAJORITY :
                   self.current_iranalyzer.copy_majority()
                   sys.stdout.flush()

            elif self.current_action == self.BN_COPY_AVE:
                   self.current_iranalyzer.copy_average()

            elif self.current_action == self.BN_COPY_FREQ:
                   self.current_iranalyzer.copy_freq()

            elif self.current_action == self.BN_CMP_MA:
                   self.current_iranalyzer.compare_majority_to_average()

            else:
                   self.logger.error( "doCurrent() error, undefined action" )
        except Exception as ex:
                # perhaps really in finally, need to learn
                #print "putting back sys.out"
                #sys.stdout = self.save_sys_stdout
                raise
        finally:
                sys.stdout.flush()
                #print "putting back sys.out"
                #sys.stdout = self.save_sys_stdout
                #print "putting back sys.out done"

# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    print( "" )
    print( " ========== starting SmartTerminal from example_processing.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )
# ======================= eof ===========================



