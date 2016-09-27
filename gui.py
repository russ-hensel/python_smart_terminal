# -*- coding: utf-8 -*-
#
# gui    for SmartTerminal  - this is a cleaned up ( somewhat ) new version
#
# this does not forward actions that do not effect the model to the controller
# otherwise it does
#
# status
#       !! drop down list for send area
#       ** scroll bar on recieve
#       ** auto scrolling for recieve
#       ** do it over with what I know now
#       *! fix colors
#       ?? make line single lines
#       ** make easy to have n entry/send lines - in parameters
#       ** must limit total content of gui so we do not have too much data - in parameters

import  logging
import  pyperclip
from    Tkinter import *   # is added everywhere since a gui assume tkinter namespace
import  sys

class RedirectText(object):
    """
    simple class to let us redirect console prints to our recieve area
    http://www.blog.pythonlibrary.org/2014/07/14/tkinter-redirecting-stdout-stderr/
    """
    #----------------------------------------------------------------------
    def __init__(self, text_ctrl):
        """Constructor
        text_ctrl text area where we want output to go
        """
        self.output = text_ctrl

    #----------------------------------------------------------------------
    def write(self, string):
        """"""
        self.output.insert( END, string )
        # add scrolling?
        self.output.see( END )

        #self.myRecText.insert( END, adata, )
        #self.myRecText.see( END )

    #--------------------------------
    def flush(self, ):
        """
        here to mimic the standard sysout
        does not really do the flush
        """
        pass

# ======================= begin new class ====================

class GUI:
    """
    gui for the application
    """
    def __init__( self, controller, parent ):

        self.parent             = parent
        self.controller         = controller
        self.parameters         = controller.parameters

        self.logger             = logging.getLogger( self.controller.logger_id + ".gui")

        self.logger.info("in class gui_new GUI init") # logger not currently used by here

        self.save_redir          = None

        self.save_sys_stdout     = sys.stdout

        self.myRecText           = None    # set later   # ?? rename globally later

        self.max_lines           = self.parameters.max_lines    # max lines in recieve area then delete fraction 1/2 now

        self.sends               = []
        self.sends_buttons       = []
        self.sends_data          = []

        self.max_lables          = 6   # number of lables, normally used for parameters
        self.lables              = []  # lables normally for parameters

        #------ constants for controlling layout ------
        self.button_width         = 6

        self.button_padx          = "2m"
        self.button_pady          = "1m"

        self.buttons_frame_padx   = "3m"
        self.buttons_frame_pady   = "2m"
        self.buttons_frame_ipadx  = "3m"
        self.buttons_frame_ipady  = "1m"

        #Button names -- this is a method I am not sure I will use in the future
        self.BN_PORTS             = "Ports"
        self.BN_CP_SELECTION      = "Copy Sel"
        self.BN_CVERT             = "Cvert"
        self.BN_CP_ALL            = "Copy All"
#        self.BN_SND_ARRAY         = "Send Array"
#
#        # for the ir analizer
#
#        self.BN_PRINT_SAMPLES     = "Print Samples"
#        self.BN_PRINT_MAJORITY    = "Print Majority"
#        self.BN_PRINT_AVE         = "Print Average"
#        self.BN_PRINT_FREQ        = "Print Freq"
#
#        self.BN_COPY_SAMPLES     = "Copy Samples"
#        self.BN_COPY_MAJORITY    = "Copy Majority"
#        self.BN_COPY_AVE         = "Copy Average"
#        self.BN_COPY_FREQ        = "Copy Freq"
#        self.BN_CMP_MA           = "Cmp M<>A"
#
#        self.BN_DN_MA            = "DnLd Majority"
#        self.BN_DN_AV            = "DnLd Average"
#
#        self.actButtons           = []
#        self.actions              = [ self.BN_PRINT_SAMPLES, self.BN_PRINT_AVE, self.BN_PRINT_MAJORITY, self.BN_PRINT_FREQ,
#                                      self.BN_COPY_SAMPLES, self.BN_COPY_AVE, self.BN_COPY_MAJORITY, self.BN_COPY_FREQ, self.BN_CMP_MA,
#                                      self.BN_DN_MA ,self.BN_DN_AV ]

        #self.current_action       = None
        #------ END constants for controlling layout ------

        next_frame = 0    # position row for frames
        # self.aParent -> self.root -> self.rec_frame

        self.root      = Frame( parent )   # this may be an extra unneded frame

        #self.root.grid( column=1, row=1 )  # this seems to set up the col grid in the root
        #self.root.pack( expand = True, sticky = E+W )  # this also works, why needed? sticky not an option here

        # this frame self.root may be rudundant with its parent
        self.root.grid(  column=0,row=0, sticky= E+W+N+S )
        self.parent.grid_columnconfigure( 0, weight=1 ) # final missing bit of magic
        self.parent.grid_rowconfigure(    0, weight=1 )

        if self.parameters.have_terminal:  #?? ever not have a terminal

                a_frame  = self.make_parm_frame( self.root,  )
                a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
                next_frame += 1

        if self.parameters.have_test_frame:
            a_frame = self.make_test_frame( self.root,  )
            a_frame.grid(row=next_frame, column=0, sticky=E + W + N)
            next_frame += 1

        if self.parameters.have_terminal:
             a_frame  = self.make_send_frame( self.root, )
             a_frame.grid( row=next_frame, column=0, sticky= E + W + N  )
             next_frame += 1

        # ------------ recieve frame ---------------------

        self.cb_scroll_var  = IntVar()  # for check box in reciev frame
        a_frame = self.rec_frame    = self.make_rec_frame( self.root, "green" )
        a_frame.grid( row=next_frame, column=0, sticky= E + W + N + S )
        next_frame += 1

        # ------------ end recieve frame ---------------------

        self.root.grid_columnconfigure( 0, weight=1 )
        self.root.grid_rowconfigure(    0, weight=0 )

        #print "self.next_frame configure", self.next_frame
        self.root.grid_rowconfigure( ( next_frame - 1 ), weight=1 )

        self.show_parms()   # may not be ideal placement

    #------ build frames  ------------------------
    # ------------------------------------------
    def make_parm_frame( self, parent, ):
            """
            make parameter frame
            open/close port show port parms
            """
            a_frame  = Frame( parent, width=600, height=200, bg ="gray", relief=RAISED, borderwidth=1 )

            buttonOpen = Button( a_frame , width=10, height=2, text = "Open" )
            buttonOpen.bind( "<Button-1>", self.doOpenButton )

            buttonClose = Button( a_frame , width=10, height=2, text = "Close" )
            buttonClose.bind( "<Button-1>", self.doCloseButton )

            buttonOpen.grid(  row = 0, column=0, sticky='E' )
            buttonClose.grid( row = 1, column=0, sticky='E' )

            for ix in range( self.max_lables ):
                    self.lables.append( Label( a_frame, text = "lbls" + str( ix ), relief = RAISED,  )  )

            lrow    = 0
            lcol    = 3
            for i_label in self.lables:
                 #print "label at ", lrow, lcol
                 i_label.grid( row=lrow, column=lcol, sticky=E + W  )    # sticky=W+E+N+S  )   # relief = RAISED)

                 lrow    += 1
                 if lrow >= 2:
                    lrow   =  0
                    lcol   += 1

            for ix in range(  2, lcol  ):
                 a_frame.grid_columnconfigure( ix, weight=0 )
                 #iframe.grid_rowconfigure(    0, weight=0 )

            return  a_frame

    # ------------------------------------------
    def make_test_frame( self, parent, ):
            """
            make a test frame place for test stuff esp. buttons
            """
            a_frame  = Frame( parent, width=300, height=200, bg=self.parameters.id_color, relief=RAISED, borderwidth=1 )

            a_button = Button( a_frame , width=10, height=2, text = "StartAuto" )
            a_button.config( command = self.cb_test_1 )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "StopAuto" )
            a_button.config( command = self.cb_test_2 )
            a_button.pack( side = LEFT )

#            a_button = Button( a_frame , width=10, height=2, text = "Graph" )
#            a_button.config( command = self.cb_test_3 )
#            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Edit Log" )
            a_button.config( command = self.controller.os_open_logfile )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Edit Parms" )
            a_button.config( command = self.controller.os_open_parmfile )
            a_button.pack( side = LEFT )

            if self.controller.parmeters_x  != "none":
                a_button = Button( a_frame , width=10, height=2, text = "Edit ParmsX" )
                a_button.config( command = self.controller.os_open_parmxfile )
                a_button.pack( side = LEFT )

#            a_button = Button( a_frame , width=10, height=2, text = "Cvert" )
#            a_button.bind( "<Button-1>", self.doButtonText )
#            a_button.pack( side = LEFT )

            #------- LIST PORTS
            a_button = Button( a_frame , width=10, height=2, text = self.BN_PORTS )
            a_button.bind( "<Button-1>", self.doButtonText )
            a_button.pack( side = LEFT )

#            #---------- Send array
#            a_button = Button( a_frame , width=10, height=2, text = self.BN_SND_ARRAY )
#            a_button.bind( "<Button-1>", self.doButtonText )
#            a_button.pack( side = LEFT )

            return a_frame

    # ------------------------------------------
    def make_send_frame( self, parent,  ):  # if this were a class then could access its variables later
            """
            make a new send frame containing little send frames
            """
            # print "make_send_frame"  color does not really work here as sends fill area

            send_frame  = Frame( parent, width=300, height=200, bg=self.parameters.id_color, relief=RAISED, borderwidth=1 )
            self.ix_send      = 0
            self.send_frames  = []
            ix_row            = 0
            ix_col            = 0
            ix_max_row        = self.parameters.max_send_rows

            for ix in range( self.parameters.gui_sends ):
                send_frame1    =  self.make_one_send_frame( send_frame, self.ix_send   )
                self.send_frames.append( send_frame1 )
                send_frame1.grid( row=ix_row,  column=ix_col, sticky= E + W + N  )

                self.ix_send   += 1
                ix_row         += 1
                if ix_row >= ix_max_row:
                    ix_row    = 0
                    ix_col    += 1

            return send_frame

    # ------------------------------------------
    def make_one_send_frame( self, parent, ix_send ):  # if this were a class then could access its variables later
            """
            make a new send frame, for just one button and text entry to send
            """
            # print "make_send_frame"  color does not really work here as sends fill area
            send_frame  = Frame( parent, width=300, height=200, bg=self.parameters.id_color, relief=RAISED, borderwidth=1 )

            a_text = Entry( send_frame , ) # width=50, ) # height=2 )
            a_text.configure( bg = "gray" )
            a_text.delete(0, END)    # this may be bad syntax when use eleswher

            if ix_send < len( self.parameters.send_strs ):
                send_str  = self.parameters.send_strs[ ix_send ]
            else:
                send_str  = ""

            a_text.insert(0, send_str )

            button0 = Button( send_frame , width=10, height=2, text = "Send" )
            button0.bind( "<Button-1>", self.doSendButton ) # function name no () which would call function then

            # position
            button0.pack( side = LEFT )
            a_text.pack(  side = LEFT, fill=BOTH, expand=1)  #  fill X Y BOTH but also need expand=1 ( or prehaps True )

            # save for send function
            self.sends.append( send_frame )
            self.sends_buttons.append( button0 )
            self.sends_data.append( a_text )

            return send_frame

    # ------------------------------------------
    def make_rec_frame( self, parent, color ):
        """
        make the recieve frame
        """
        iframe  = Frame( parent, width=300, height=800, bg ="blue", relief=RAISED, borderwidth=1,  )

        bframe  = Frame( iframe, bg ="black", width=30  ) # width=300, height=800, bg ="blue", relief=RAISED, borderwidth=1,  )
        bframe.grid( row=0, column=0, sticky = N + S )

        text0 = Text( iframe , width=50, height=20 )
        #text0.configure( bg = "red" )
        self.save_redir = RedirectText( text0 )

        s_text0 = Scrollbar( iframe  )  # LEFT left
        s_text0.grid( row=0, column=2, sticky = N + S )

        s_text0.config( command=text0.yview )
        text0.config( yscrollcommand=s_text0.set )

        text0.grid( row=0, column=1, sticky = N + S + E + W  )

        self.myRecText  = text0

        iframe.grid_columnconfigure( 1, weight=1 )
        iframe.grid_rowconfigure(    0, weight=1 )

        # now into the button frame bframe

        # spacer
        s_frame = Frame( bframe, bg ="green", height=20 ) # width=30  )
        s_frame.grid( row=0, column=0  )

        row_ix   = 0

        # --------------------
        b_clear = Button( bframe , width=10, height=2, text = "Clear" )
        b_clear.bind( "<Button-1>", self.doClearButton )
        b_clear.grid( row=row_ix, column=0   )
        row_ix   += 1

        #-----
        b_temp = Button( bframe , width=10, height=2, text = self.BN_CP_SELECTION )
        b_temp.bind( "<Button-1>", self.doButtonText )
        b_temp.grid( row=row_ix, column=0   )
        row_ix   += 1

        #-----
        b_copy = Button( bframe , width=10, height=2, text = self.BN_CP_ALL )
        b_copy.bind( "<Button-1>", self.doCopyButton )
        b_copy.grid( row=row_ix, column=0   )
        row_ix += 1

        # -------------
        a_widget = Checkbutton( bframe,  width=7, height=2, text="A Scroll", variable=self.cb_scroll_var,  command=self.do_auto_scroll )
        a_widget.grid( row=row_ix, column=0   )
        row_ix += 1

        self.cb_scroll_var.set( self.parameters.default_scroll )

        return iframe

    #-----  functions mostly for controller  ------------------------
    # ------------------------------------------
    def show_parms( self,  ) :  # show befor open, yes, but frist 2 parms are ini file and port status
        """
        get parms from Parameters and display
        """
        spacer   = "                                     "
        lab_len  = 20

        self.lables[ 0 ].config( text    = ("Port: Closed"                                      + spacer )[0:lab_len]   )

        self.lables[ 1 ].config( text    = ("Type: "       + self.parameters.getCommTypeAsStr() + spacer )[0:lab_len]   )

        self.lables[ 2 ].config( text    = ("PortID: "     + self.parameters.getPortAsStr()     + spacer )[0:lab_len]   )
        self.lables[ 3 ].config( text    = ("Baud: "       + self.parameters.getBaudrateAsStr() + spacer )[0:lab_len]   )

        self.lables[ 4 ].config( text    = ("StopBits: "   + self.parameters.getStopbitsAsStr() + spacer )[0:lab_len]   )
        self.lables[ 5 ].config( text    = ("Parity: "     + self.parameters.getParityAsStr()   + spacer )[0:lab_len]   )

        return

    # ------------------------------------------
    def printToSendArea( self, data ):
        """
        fix name !!
        add recieve tag to parameters ??
        """
        sdata = "# >>>" + data  + "\n"
        self.showRecFrame( sdata )   # or just use directly
        return

    # ---------------------------------------
    def showRecFrame( self, adata ):
        """
        fix name !!
        """
        self.myRecText.insert( END, adata, )

        numlines = int( self.myRecText.index( 'end - 1 line' ).split('.')[0] )
        if numlines > self.max_lines:
            cut  = numlines/2     # lines to keep/remove
            # remove excess text
            self.myRecText.delete( 1.0, str( cut ) + ".0" )

        if self.cb_scroll_var.get():
            self.myRecText.see( END )

        return

    # ------------------------------------------
    def set_open( self, status ):
        """
        set port parameter to open/closed
        """

        self.lables[ 0 ].config( text    = "Port: " + status  )

        return

    #----- buttons ------------------------
    # ------------------------------------------
    def cb_test_1( self ):
        """
        process test button 1
        """
        #print "cb_test_1"
        self.controller.cb_gui_test_1()

    # ------------------------------------------
    def cb_test_2( self ):
        """
        process test button 2
        """
        #print "cb_test_2"
        self.controller.cb_gui_test_2()

    # ------------------------------------------
    def cb_test_3( self ):
        """
        process test button
        """
        #print "cb_test_3"
        self.controller.cb_gui_test_3()

    def doOpenButton( self, event):
        self.controller.open_com_driver()
        return

    # ------------------------------------------
    def doCloseButton( self, event):

        self.controller.closeDriver()
        return

    # ------------------------------------------
    def doTest1Button( self, event):

        # next code when used for looping
        self.controller.log( "setting looping true", "print" )
        self.controller.looping = True
        return

    # ------------------------------------------
    def doTest2Button( self, event):

        self.controller.log( "setting looping false", "print" )
        self.controller.looping = False
        return

    # ------------------------------------------
    def doButtonText( self, event):
        """
        easy to add functions that look at the button text
        """
        btext =  event.widget["text"]

        if btext == self.BN_CP_SELECTION:
            #def doCopyButton( self, event ):
            # nogood if no selection put in try except
            try:
                data  = self.myRecText.get( "sel.first", "sel.last" )
                pyperclip.copy( data )
            except Exception, exception:  # if no selection
                pass

            return

        elif btext == "Copy All":

            # may be in do CopyButton
            #def doCopyButton( self, event ):
            """
            """
            data  = self.myRecText.get( 1.0, END )
            pyperclip.copy( data )
            return

        elif btext == "Cvert":
            # print btext
            adata   =  self.myRecText.get( 1.0, END )

            #bdata  = dataConvert1( adata )
            #self.text1.delete( 1.0, END )
            #adata = "this is the text called adata that is..... "
            #self.text1.insert( END, bdata, )
            #self.text1.see( END )

            data_splits   = adata.split( " " )

            cdata  = []
            for item in data_splits:

                try:
                    value = int( item )
                    item  = str( value/50 )  # needs to go back to string for join

                except ValueError:
                    pass
                cdata.append( item )

            sep = "\n"
            bdata   = sep.join( cdata )

            pyperclip.copy( bdata )
            self.myRecText.delete( 1.0, END )

        elif btext == self.BN_PORTS:
            self.controller.ports()
            pass

        elif btext == self.BN_SND_ARRAY:
            #self.text0.delete( 1.0, END )
            #print btext
            self.controller.sendArray()
            pass

        # for screwing around
        elif btext == "Add DB":
            self.controller.addDB()
            pass

        elif btext == "Graph":
            self.controller.graph()
            pass

        else:
            msg   = "no action defined for: " + btext
            self.logger.error( msg )
        return

    # ------------------------------------------
    def doClearButton( self, event):
        """
        for the clear button
        clear the recieve area
        """
        self.myRecText.delete( 1.0, END )
        return

    # ------------------------------------------
    def doCopyButton( self, event ):
        """
        copy all text to the clipboard
        """
        data  = self.myRecText.get( 1.0, END )
        pyperclip.copy( data )
        return

    # ------------------------------------------
    def do_auto_scroll( self,  ):
        """
        pass, not needed, place holder
        """
        # print "do_auto_scroll"
        # not going to involve controller
        pass
        return

    # ------------------------------------------
    def doSendButton( self, event ) :  # how do we identify the button
        """
        any send button
        for at least now do the send echo locally ( and crlf or always use locally )
        """
        #identify the control, one of mySendsButtons
        control_ix = -1
        for index, item in enumerate( self.sends_buttons ):

            if item == event.widget:
                control_ix = index
                break

        # now we get text out of the ajoining control

        # this is for a text not an entry
        #contents = self.mySendsData[control_ix].get(1.0, END)

        # for an entry
        contents = self.sends_data[control_ix].get()

        self.controller.send( contents )
        return

    # ---------------  end of button actions
# =======================================

# import test_controller # no longer used

if __name__ == '__main__':
        """
        run the app
        """
        # ------ with the test controller, needs a bit of maintance
#        a_app = test_controller.TestController(  )
#        a_app.test_run_gui()
#
#        print "====== test done =============="

        import smart_terminal
        a_app = smart_terminal.SmartTerminal(  )



