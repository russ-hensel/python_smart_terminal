# -*- coding: utf-8 -*-

class ParmetersXx( object ):
    """
    command line might look like this
    python ir_terminal.py  parameters=paramaters_b

    """
    def __init__(self, controller  ):
        pass


    def modify( self, parameters ):

        print "modifying parameters in gh_paramaters.py"

        #parameters.port              = "COM6"   # /dev/ttyUSB0 on GNU/Linux or COM3 on Windows. Device name or port number number or None.
        #self.port              = "/dev/ttyUSB0"
        #self.port              = "/dev/ttyUSB1"
        #parameters.port              = "COM15"
        #parameters.port              = "COM99"


        # parameters.icon              = r"D:\Temp\ico_from_windows\terminal_red.ico"    #  blue red green yellow

        parameters.id_color          = "red"    #  in ir terminal but may not be in smart_terminal
        # parameters.win_geometry      = '1500x800+20+20'    # width x height position

        parameters.win_geometry      = '800x800+20+20'    # width x height position








