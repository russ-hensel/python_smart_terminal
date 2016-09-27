# -*- coding: utf-8 -*-

class ParmetersXx( object ):
    """


    """
    def __init__(self, controller  ):
        pass

        # parameters=paramaters_b


    def modify( self, parameters ):

        print "modifying parameters in paramaters_b"

        parameters.port              = "COM4"   # /dev/ttyUSB0 on GNU/Linux or COM3 on Windows. Device name or port number number or None.
        #self.port              = "/dev/ttyUSB0"
        #self.port              = "/dev/ttyUSB1"
        #parameters.port              = "COM15"
        #parameters.port              = "COM99"


        parameters.icon              = r"D:\Temp\ico_from_windows\terminal_red.ico"    #  blue red green yellow

        parameters.id_color          = "blue"    #

        parameters.id_color          = "blue"

        parameters.id_color          = "red"    #

        parameters.id_color          = "red"

        # parameters.win_geometry      = '1500x800+20+20'    # width x height position

        parameters.win_geometry      = '800x800+20+20'    # width x height position

        self.send_strs         = [ "r", "p0", "n", "g400", "d-", "d+", "t2", "t8", "t16", "", "a5", "a10", "a20", ""    ]







