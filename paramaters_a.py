# -*- coding: utf-8 -*-

# to have this file active in your SmartTerminal: 
# command line might look like this:  # python smart_terminal.py    parameters=paramaters_a

class ParmetersXx( object ):
    """
    this is an object which extends the setting in the normal parameter file 
    it is called after the parameter file is run.

    """
    def __init__(self,  ):
        pass


    def modify( self, parameters ):
        """
        in the parameter file we use self.xxx = .... here it is parameters.xxx = .....
        
        """
        
        print( "modifying parameters in paramaters_a" )

        parameters.port              = "COM3"   # /dev/ttyUSB0 on GNU/Linux or COM3 on Windows. Device name or port number number or None.
        #self.port              = "/dev/ttyUSB0"
        #self.port              = "/dev/ttyUSB1"
        #parameters.port              = "COM15"
        #parameters.port              = "COM99"


        parameters.icon              = r"D:\Temp\ico_from_windows\terminal_red.ico"    #  blue red green yellow

        parameters.id_color          = "blue"    #
        # parameters.win_geometry      = '1500x800+20+20'    # width x height position
        parameters.id_color          = "blue"

        parameters.win_geometry      = '800x800+20+20'    # width x height position

        self.send_strs         = [ "r", "p0", "n", "g400", "d-", "d+", "t2", "t8", "t16", "", "a5", "a10", "a20", ""    ]

        
# ================= eof ===============






