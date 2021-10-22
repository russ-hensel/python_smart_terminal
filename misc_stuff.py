# -*- coding: utf-8 -*-

"""
use in extension for contolloring
missing for a long time added back in ver 6

"""





import tkinter as Tk
# import misc_stuff

##----------------------------------------------
#def do_button_action( self, event ):
#    """
#    think this works but is odd we can actually do function based on the widget, and this does not
#    do a good job if invalid button is called
#    easy to add functions that look at the button text but could actually use the button instance self.button_actions.
#    """
#    for ix, i_button_action in  enumerate( self.button_actions ):
#        text     = i_button_action.name       # or i_button_action.button == event.widget  !! probably better
#        btext    = event.widget[ "text" ]
#        if event.widget == i_button_action.button:
#            #event.widget.config( bg="gray" )   # this may blink the button when the action happens look into this
#            i_button_action.function( i_button_action.function_args )
#            # self.current_action =  act    # not sure what did look in old cod
#            break


# =================================
class ButtonActionList( object ):
    def __init__( self, ):
        self.action_list  = []

    # ----------------------------------------
    def add_action( self, a_button_action  ):
        """
        you can create externally but why not use create_action
        """
        self.action_list.append( a_button_action )

    # ----------------------------------------
    def create_action( self, title, function   ):
        """
        create the action and add to list
        """
        a_button_action         = ButtonAction( title, function )
        self.add_action( a_button_action  )

    # ----------------------------------------
    def create_place_in_frame( self, a_frame  ):
        """
        ret: the frame, which is really the same as passed in or zip
        """
        # loop thru button_actions and create and place the buttons
        for ix, i_button_action  in  enumerate( self.action_list ):
            # make button
            a_button = Tk.Button( a_frame, width = 35, height = 3, text = i_button_action.name, wraplength = 100 )
            a_button.bind( "<Button-1>", self.do_action )
            # 8 is number of buttons across
            a_row     =  0
            a_col     =  ix

            # print( a_row, a_col )
            a_button.grid(  row = a_row, column = a_col, sticky ='E' + "W" )
            a_frame.grid_columnconfigure( a_col, weight=1 )
            i_button_action.set_button( a_button )

    # ----------------------------------------
    def do_action( self, event  ):

        for i_button_action in self.action_list:
            #text     = i_button_action.name       # or i_button_action.button == event.widget  !! probably better
            #btext    = event.widget[ "text" ]
            if event.widget == i_button_action.button:
                #event.widget.config( bg="gray" )   # this may blink the button when the action happens look into this
                i_button_action.function( i_button_action.function_args )
                # self.current_action =  act    # not sure what did look in old cod
                break


# =================================
class ButtonAction( object ):
    """
    this is an object that may be used for a bunch of buttons to make creation and calling with arguments
    a bit easier
    in the future
    this may become an asbstract class for plug in button actions in the smart terminal, a bit like processing add to the array
    need ref to my processing object probably
    hold info to implement a button in the gui
    looks like a struct so far
    """
    def __init__( self, a_name, a_function ):
        #self.processor       =  a_processor     # why this it is a mini controller where used?
        self.name            =  a_name
        self.function        =  a_function      # where are the arguments elswhere in the thing in function_args with set_args
        self.function_args   = [ self.name, "I am an argument", "and another " ]   # change to tuple?
        self.button          = None
    # -------------------------------------------------
    def set_button( self, a_button ):
        """
        use when button actually created ( or move a factory in here??) may not be used
        """
        self.button          = a_button
    # -------------------------------------------------
    def set_args( self, a_args ):
        """
        set args, but unless list seems can only set one
        maybe make a tuple and use *() when calling to unback
        """
        self.function_args   = a_args




# ====================== EOF ===========================


