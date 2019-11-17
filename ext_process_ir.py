# -*- coding: utf-8 -*-

"""

# for smart_terminal
# !! clean up std names
# !! see if can get print function back
#
not working in version 3, I have made a quick effor and located most
of the missing ir code.  Needs more work.







"""
import  logging
#import  pyperclip
#from    Tkinter import *   # is added everywhere since a gui assume tkinter namespace
import sys
import tkinter as Tk
#import abc

# -------------- local libs ------------------

import abc_def
from   app_global import AppGlobal

#import misc_stuff
#import smart_terminal

sys.path.append( r"D:\Russ\0000\python00\python3\_projects\irtools" )
sys.path.append( r"D:\Russ\0000\python00\python3\_projects\irtools\ir_data" )
#sys.path.append( r"../irtools" )
#sys.path.append( r"../ir_test_data" )
#sys.path.append( r"../irtools/sony" )

class IRProcessing( abc_def.ABCProcessing ):
    """
    add on for IR
    """

    def __init__( self,  ):    #iranalyzers ):

        AppGlobal.abc_processing    = self
        self.controller             = AppGlobal.controller
        self.parameters             = AppGlobal.parameters

        self.helper_thread          = self.controller.helper_thread

        self.logger                 = logging.getLogger( self.controller.logger_id + ".ir" )   # assign to logger or get all the time does logger have aname or does this assign

        self.logger.info( "in class IRProcessing init for the ir_terminal" )

        # iranalyzers
        irList    = []

        import sony_toggle_pwr
        #irList.append( sony_toggle_pwr.ira )     # gives error
        irList.append( sony_toggle_pwr.ira_n )   # attempt to fix
        self.iranalyzers         = irList

        #self.tx_prefix_rec      = self.parameters.tx_prefix_rec
        #self.tx_prefix_send     = self.parameters.tx_prefix_send

        #self.save_redir         = None

        #self.save_redir          = sys.stdout
        #self.save_redir          = 5

        #self.save_sys_stdout     = sys.stdout

        #self.iranalyzers    = []
        #self.iranalyzers.append( irtools.IrAnalyzer( "Comcast _0 button"  ))


        self.iraButtons          = []

        self.current_iranalyzer  = None

        #------ constants for controlling layout ------
        self.button_width        = 6

        self.button_padx          = "2m"
        self.button_pady          = "1m"

        self.buttons_frame_padx   = "3m"
        self.buttons_frame_pady   = "2m"
        self.buttons_frame_ipadx  = "3m"
        self.buttons_frame_ipady  = "1m"

        #Button names
        # for the ir analizer
        self.BN_PRINT_SAMPLES     = "Print Samples"
        self.BN_PRINT_MAJORITY    = "Print Majority"
        self.BN_PRINT_AVE         = "Print Average"
        self.BN_PRINT_FREQ        = "Print Freq"

        self.BN_COPY_SAMPLES      = "Copy Samples"
        self.BN_COPY_MAJORITY     = "Copy Majority"
        self.BN_COPY_AVE          = "Copy Average"
        self.BN_COPY_FREQ         = "Copy Freq"
        self.BN_CMP_MA            = "Cmp M<>A"

        self.BN_DN_MA             = "DnLd Majority"
        self.BN_DN_AV             = "DnLd Average"

        self.actButtons           = []
        self.actions              = [ self.BN_PRINT_SAMPLES, self.BN_PRINT_AVE, self.BN_PRINT_MAJORITY, self.BN_PRINT_FREQ,
                                      self.BN_COPY_SAMPLES,  self.BN_COPY_AVE,  self.BN_COPY_MAJORITY,  self.BN_COPY_FREQ,
                                      self.BN_CMP_MA,        self.BN_DN_MA ,    self.BN_DN_AV ]
        self.current_action       = None

        # ------------------- end for ir
#    # ----------------------------------------
#    def make_task_list( self, ):
#        """
#                make tasks for green house, uses some stuff in
#        parameters
#        status, under development
#        """
#        self.logger.debug( "ir_processing: make_tasks_for_green_house" )
#
#        self.task_list    = smart_terminal.TaskList( self.controller )
#
#        self.task_list.reset_tasks()
#
#        # open port,
#        need_me  = smart_terminal.ATask(   task_list  =  self.task_list,
#                          task_trans       = self.task_list.task_open_trans,
#                          task_rec         = self.task_list.task_open_rec,
#                          task_special     = self.task_list.task_special_exception,
#                          task_time_error  = self.task_list.task_special_exception,
#                          repeats          = 1,
#                          time_start       = 2,   time_delta = 5, time_error = 100  )
#        # check version
#        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
#                          task_trans       = self.task_list.task_version_trans,
#                          task_rec         = self.task_list.task_version_rec,
#                          task_special     = self.task_list.task_special_exception,
#                          task_time_error  = self.task_list.task_special_exception,
#                          repeats          = 1,
#                          time_start       = 5,   time_delta = 5, time_error = 10  )
#
#        # print message
#        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
#                          task_trans       = self.task_list.task_print_trans,
#                          task_rec         = self.task_list.task_print_rec,
#                          task_special     = self.task_list.task_special_exception,
#                          task_time_error  = self.task_list.task_special_exception,
#                          repeats          = 1,
#                          time_start       = 5,   time_delta = 5, time_error = 10  )
#        need_me.set_msg( "this is message 1" )
#
#
#        # print message
#        need_me  = smart_terminal.ATask(      task_list  =  self.task_list,
#                          task_trans        = self.task_list.task_print_trans,
#                          task_rec          = self.task_list.task_print_rec,
#                          task_special      = self.task_list.task_special_exception,
#                          task_time_error   = self.task_list.task_special_exception,
#                          repeats           = 1,
#                          time_start        = 1,   time_delta = 5, time_error = 10  )
#        need_me.set_msg( "this is message 2" )
#
#
#        # print message
#        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
#                          task_trans       = self.task_list.task_print_trans,
#                          task_rec         = self.task_list.task_print_rec,
#                          task_special     = self.task_list.task_special_exception,
#                          task_time_error  = self.task_list.task_special_exception,
#                          repeats          = 1,
#                          time_start       = 1,   time_delta = 5, time_error = 10  )
#        need_me.set_msg( "this is message 3" )
#
#
#        # aquire data  -- but wait after version
#        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
#                          task_trans       = self.task_list.task_gh_trans_aquire,
#                          task_rec         = self.task_list.task_gh_rec_aquire,
#                          task_special     = self.task_list.task_special_exception,
#                          task_time_error  = self.task_list.task_special_exception,
#                          repeats          = 1, # = 0 infinite loop
#                          time_start       = 5,   time_delta = .1, time_error = 10  )
#
#        # get temperature
#        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
#                          task_trans       = self.task_list.task_gh_trans_temp,
#                          task_rec         = self.task_list.task_gh_rec_temp,
#                          task_special     = self.task_list.task_special_exception,
#                          task_time_error  = self.task_list.task_special_exception,
#                          repeats          = 1, # = 0 infinite loop
#                          time_start       = .1,   time_delta = .1, time_error = 10  )
#
#        # get temperature
#        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
#                          task_trans       = self.task_list.task_gh_trans_humid,
#                          task_rec         = self.task_list.task_gh_rec_humid,
#                          task_special     = self.task_list.task_special_exception,
#                          task_time_error  = self.task_list.task_special_exception,
#                          repeats          = 1, # = 0 infinite loop
#                          time_start       = .1,   time_delta = .1, time_error = 10  )
#
#        # go back !!!!!!!!
#        need_me  = smart_terminal.ATask( task_list  =  self.task_list,
#                          task_trans       = self.task_list.task_go_back_n,
#                          task_rec         = self.task_list.task_go_back_n,
#                          task_special     = self.task_list.task_special_exception,
#                          task_time_error  = self.task_list.task_special_exception,
#                          repeats          = 0, # = 0 infinite loop -- but not for go back
#                          time_start       = .1,   time_delta = 5, time_error = 10  )
#        need_me.set_msg( "task_go_back_n " )
#        need_me.set_TVO( 3 )

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
#        return  self.task_list


    def add_gui( self, parent, ):  # if this were a class then could access its variables later
            """
            make frame and place it
            open/close port
            show port pams
            test button for recieve simulation
            whole parm frame is managed by a grid inside the grid of the whole window
            """
            color        = "blue"
            iframe        = Tk.Frame( parent, width=300, height=200, bg ="gray", relief=Tk.RAISED, borderwidth=1 )

           # iframe.grid( row=self.next_frame, column=0, sticky = Tk.E + Tk.W + Tk.N + Tk.S )   # + N + S  )  # actually only expands horiz

            #iframe.grid( row = self.next_frame, column=0, sticky='EW' )
            #self.next_frame += 1
            #print "self.next_frame ", self.next_frame

            # looop thru analizers makeing a button for each

            for ix, anal in  enumerate( self.iranalyzers ) :
                    buttonX = Tk.Button( iframe , width=10, height=4, text = anal.name, wraplength = 60, bg="white" ) # relief=SUNKEN )
                    buttonX.bind( "<Button-1>", self.doButtonIra )
                    buttonX.grid(  row = 0, column=ix, sticky='E' + "W" )
                    iframe.grid_columnconfigure( ix, weight=1 )
                    self.iraButtons.append( buttonX )
                    #print buttonX.cget('bg')

            for ix, action  in  enumerate( self.actions ):
                    buttonX = Tk.Button( iframe , width=10, height=2, text = action, wraplength = 60 )
                    buttonX.bind( "<Button-1>", self.doButtonAction )
                    buttonX.grid(  row = ( ix / 4 ) +1, column=ix %4, sticky='E' + "W" )
                    iframe.grid_columnconfigure( ix, weight=1 )
                    self.actButtons.append( buttonX )
                    #print buttonX.cget('bg')   # "SystemButtonFace"

            return iframe
# both the next 2 functions finall call doCurrent, they just set up the context
    def doButtonIra( self, event):
        """
        easy to add functions that look at the button text
        """
        for ix, anal in  enumerate( self.iranalyzers ) :
            text     = anal.name
            btext    =  event.widget["text"]
            if text ==  btext:
                self.current_iranalyzer =  anal
                use_anal = anal
                break

        for b  in ( self.iraButtons ):
            b.config( bg= "white"  )
        event.widget.config( bg="gray" )

        anal.copy_average()
        #print "broke with ", btext
        self.doCurrent(  )

    #----------------------------------------------
    def doButtonAction( self, event):
        """
        easy to add functions that look at the button text
        """
        for ix, act in  enumerate( self.actions ) :
            text     = act
            btext    = event.widget["text"]
            if text == btext:
                self.current_action =  act
                break
        # appearance
        for b  in ( self.actButtons ):
            b.config( bg= "white"  )
        event.widget.config( bg="gray" )
        self.doCurrent(  )

#----------------------------------------
# does the current action set up by the prior 2 functins
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



# ======================= eof ===========================






