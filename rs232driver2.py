# -*- coding: utf-8 -*-

"""
for support of (smart_terminal.py)
this driver is for rs232 comm ports
it returns only full lines
eol is expected to be a cr,
if newlines nl are present then they are deleted and ignored

has the ability to delete other charcters in a list, but now just used for nl
   ** now uses standard loggging
   !! log port failure

   !! this is a mess, should setting exist or not?? properties.... also mess where as_string
"""

import  logging
#import antigravity
import serial
import sys
import serial.tools.list_ports

from    app_global import AppGlobal

# ================= class ======================
class RS232Settingsxxxxx( object ):
    """
    struct to store rs232 settings
    ?? enhance for defaults
    ?? move other driver stuff here
    ?? how to use names
    not currently including status open closed or overun etc
    """
    def __init__(self, ):

        self.name               =       "rs232 settings, unnamed"

        self.port        =       None
        self.baudrate    =       None
        self.parity      =       None
        self.stopbits    =       None
        self.bytesize    =       None

        self.driver      =       None    # if assigned to a driver ?? may not use

    # --------------------------------------
    def set_from_values( port, baudrate = None, parity = None,   stopbits = None,   bytesize = None ):
        """
        set the parameters explicitly, optionally leaving some alone

        """
        self.port            =       port

        if ( baudrate is None ):
            self.baudrate    =       baudrate

        if not( parity   is None ):
            self.parity      =       parity

        if not( stopbits is None ):
            self.stopbits    =       stopbits

        if not( bytesize is None ):
            self.bytesize    =       bytesize

    # --------------------------------------
    def set_from_parameters( self, parameters ):
        """
        set the parameters of the port from Parameters instance

        """
        self.port        =       parameters.port
        self.baudrate    =       parameters.baudrate
        self.parity      =       parameters.parity
        self.stopbits    =       parameters.stopbits
        self.bytesize    =       parameters.bytesize


# --------------------------------------
    @property    # lets us get not set
    def port_as_string( self ):

        return str( self.port ) # str for None

# ================= class ======================
class RS232Driver( object ):

    def __init__(self,  ):

        self.name          = "RS232Diver2  2016 dec 30.1"

        self.controller    = AppGlobal.controller

        self.parameters    = self.controller.parameters

        self.logger        = logging.getLogger( self.controller.logger_id + ".232")
        self.driver        = serial.Serial()     # seems easy to have a driver

        self.isopen        = False
        self.recBuff       = ""    # buffer recieved data

        self.settings      = None   # set later

        self.ba_rec_buff     = bytearray( "", "utf-8" )    # data that has been recieved. py 2
        #self.rec_data       = ""

        # this may be overengineering really only want to delete cr  -- us lf or nl \n as end of string marker
        self.by_dels         =  []
        #self.delchars.append( bytes( b'\x0D' ))      # 13    015    0D    00001101    CR
        #self.delchars.append( bytes( b'\x0A' ))      #           0A  =    LF py 2
        #self.delchars.append( '\x0A' )
        #self.eol            =  "\r"    #  \n or \r
        self.by_eol          =  b'\x0D'          #  \n  =  '\x0A'  or \r   = '\x0D'  but do not delete it

        #self.delchars.append( bytes( b'\x44' ))      # D and up start as  b'\x44'  so
        #self.delchars.append( bytes( b'\x45' ))
        #self.delchars.append( bytes( b'\x46' ))
        #self.delchars.append( bytes( b'\x20' ))     # space    b'\x20'

        self.by_dels.append( bytes( b'\x11' ))   # x11 = dc1
        self.by_dels.append( bytes( b'\x0A' ))   # 0A  = LF
        # -----  utility values, use in utility functions below

        self.parity_to_strs      = {    serial.PARITY_EVEN : "Parity Even",
                                        serial.PARITY_NONE : "Parity None",
                                        serial.PARITY_ODD  : "Parity Odd",
                                        serial.PARITY_MARK : "Parity Mark",
                                        serial.PARITY_SPACE: "Parity Space"
                                    }
        # ------

        self.stopbits_to_strs    = {   serial.STOPBITS_ONE            : "1",
                                       serial.STOPBITS_ONE_POINT_FIVE : "1.5",
                                       serial.STOPBITS_TWO            : "2",
                                   }

#        '''
#        this was for simulator  -- code moved, think it is another driver
#        self.gotDataBuff    = ""   # simulated data for next recieve.
#        self.gotDataIx      = 0
#        self.gotDataData    = []
#        self.gotDataData.append( "rec" )
#        self.gotDataData.append( "eived" )
#        self.gotDataData.append( "\n" )
#        self.gotDataData.append( "666\n" )
#        self.gotDataData.append( "3.1415" )
#        self.gotDataData.append( "9\n" )
#        self.gotDataData.append( "russ\n" )
#        self.gotDataData.append( "xxy" )
#        self.gotDataData.append( "y\n" )
#        self.gotDataData.append( "rec" )
#        self.gotDataData.append( "penultimate\n" )
#        self.gotDataData.append( "end\n" )
#        '''

# --------------------------------------
    def getName( self, ):

        return self.name

# --------------------------------------
    def getOpen( self, ):

        return self.isopen

# --------------------------------------
    @property    # lets us get not set
    def demo_property( self ):
        print( " return self.__demo_property" )
        return self.__demo_property

# --------------------------------------
    def close(self, ):

        #self.controller.log( "closing com", "print"  )
        self.driver.close()
        self.isopen  = False

        return

# --------------------------------------
    def open( self, port = None ):
        """
        ( port=string_or_None, -> zip)
        call from controller port or ht, use a lock or luck
        tries to open port
        returns true if port opens
        gets parms itself see set_from_parameters
        """
        #self.controller.log( "opening com driver", "print"  )
        # self.set_from_parameters

        if port != None:
             self.driver.port  = port

        retval   = True

        try:
            self.driver.open()

        except Exception as excpt:
            #print type(inst)     # the exception instance
            #print inst.args      # arguments stored in .args
            #print inst           # __str__ allows args to printed directly
            #x, y = inst.args

            retval   = False

        self.isopen  = retval

        return  retval

# --------------------------------------
    def try_handshake( self, send, rec, rec_time ):
        """
        send send, compare to rec,
        where do we get parms
        use open port
        return true false
        is this in use, not clear to me function may be in the smart terminal but this may actually be a good idea.
        """
        self.send( send )

        #rec_time  = 2     # get from parameters
        #ts_start = time.time()
        ts_end   = rec_time + time.time()

        # give it a while to get the data, so loop for a bit

        while ( time.time() < ts_end ):

            new_data  = self.myDriver.getRecString( )
            if new_data != "":
                 data   = data + new_data

        ret_val = ( data[0:len(rec)] == rec  )   # should compare have - 1

        return ret_val

    # --------------------------------------
    def list_available( self, ports = None ):
        """
        how do we switch methods, ........
        *use the api from python serial
        *try to open them
        think only tried with ports = None
        """
        if ports == None:
            return ( list(serial.tools.list_ports.comports()) )
        else:

            got_ports = []

            #try_ports = [ "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", ]
            try_ports = ports
            for aport in try_ports:
                #print "trying ", aport
                if self.open( aport ):
                    #print "opened"
                    self.close()
                    got_ports.append( ( aport, "?", "?") )

            return got_ports

# --------------------------------------
    def probe_available( self, ports  ):
        """
        ports is a list of strings the names of the ports
        use this driver, save and restore, but will close current port if open
        if a tested port opens it will be closed again
        may reopen and close port in use.
        leave port settings alone ( so why did I create the settings )

        """
        results      = []      # list of tuples ( name, open_fg )
        self.close()
        save_port    = self.driver.port
        for i_port in ports:
            # skip if have an open port or perhaps just my port setting  self.isopen  but need to use the driver
            opened   = self.open( i_port )
            self.close()
            results.append( ( i_port, opened ) )

        self.driver.port    = save_port
        return results
    # --------------------------------------
    def set_from_parameters( self, parameters ):
        """
        set the parameters of the port from Parameters instance
        todo   make sure port closed first?  set status to self.isopen = False

        """

        self.driver.port        =       parameters.port
        self.driver.baudrate    =       parameters.baudrate
        self.driver.parity      =       parameters.parity
        self.driver.stopbits    =       parameters.stopbits
        self.driver.bytesize    =       parameters.bytesize

        #ser = serial.Serial(0)
        #self.recTimeout          = self.parameters.recTimeout

        return self.name

    # --------------------------------------
    def set_from_settingsxxxxx( self, settings ):
        """
        ( settings=instance_of_RS232Settings -> zip )
        set the parameters of the port from Parameters instance
        todo   make sure port closed first?  set status to self.isopen = False

        """
        self.settings           =       settings
        self.driver.port        =       settings.port
        self.driver.baudrate    =       settings.baudrate
        self.driver.parity      =       settings.parity
        self.driver.stopbits    =       settings.stopbits
        self.driver.bytesize    =       settings.bytesize

        return

    # --------------------------------------
    def save_to_settingsxxxx( self,  ):
        """
        create a settings and save to it, then return

        """
        a_setting                 =  RS232Settings( port        = self.driver.port,
                                                    baudrate    = self.driver.baudrate,
                                                    parity      = self.driver.parity,
                                                    stopbits    = self.driver.stopbits,
                                                    bytesize    = self.driver.bytesize,
                                                  )

        return a_setting

    # -------------------------------------
    def send( self, adata):
        """
        sends the data ( if port is open )
        return  nothing
        """
        # note early returns on error
        if self.isopen == False:
            return

        #self.controller.log( "sending >" + adata, "print" )
        data   = adata + self.parameters.serialAppend    # if configured

        self.driver.write( bytearray(data, 'utf8' ) )    # "ascii"  'utf8'

        return

    #----------------------------------------
    def getRecString( self, ):
        """
        version 3 -- revise for python 3 - start with byte arrays to support delete then convert to strings quickly
        serial may have a method that makes this dance obsolet
        just recognize one eol, cr as used with arduino, may include or not scrubbing
        may strips some special characters

        note: early return
        see  # https://stackoverflow.com/questions/1093598/pyserial-how-to-read-the-last-line-sent-from-a-serial-device
        return complete line or ""
        """
        if self.isopen == False:
            return ""

        no_waiting   = self.driver.inWaiting()

        if no_waiting == 0:
           # but may have an eol in the buffer already
           #retval = ""
           #return retval
           #   ========== clean up this code if all this i null
           pass
        else:
            # there is some recieved data, filter our cr not yet -- what does arduino send?

            ba_rec_delta    =  bytearray( self.driver.read(size = no_waiting) )
            # scrub as many char as desired do not delete eol if need to detect it later
            for i_del in self.by_dels:
                while True:

                    ix_del = ba_rec_delta.find( i_del )    # neither find or rfind
                    #print ix_del

                    if ix_del < 0:
                        break

                    del ba_rec_delta[ix_del:ix_del +1]    # delete the character

            self.ba_rec_buff   +=  ba_rec_delta    # concatinate or append

        # check that we have not got end of string marker what is it cr or lf /n
        ix = self.ba_rec_buff.find( self.by_eol )   #
        if ix  < 0:
            return ""

        #now finish up save some for buffer and return what have so far
        # have had error here, which kills app, seems based on bad data back, in that case we will retuns say ng ?
        # UnicodeDecodeError
        # may be a way to have function ignore as well
        try:

            ret_string          = ( self.ba_rec_buff[ 0: ix ] ).decode( encoding='UTF-8' )

        except UnicodeDecodeError as exception:
            self.logger.critical( "decode error " + str( exception  )  )
            #print( exception )
            ret_string           = "ng"
        # data past eol if any
        self.ba_rec_buff    = self.ba_rec_buff[ ix + 1: ]    # should be ok even if out of range should get rid of eol

        return ret_string

#----------------------------------------
    def getRecString_ver2( self, ):
        """
        version 2 -- so far recieves some not all stuff -- ng in python 3

        just recognize one eol, cr as used with arduino, may include or not scrubbing
        may strips some special characters

        note: early return
        see  # https://stackoverflow.com/questions/1093598/pyserial-how-to-read-the-last-line-sent-from-a-serial-device
        return complete line or ""
        """
        if self.isopen == False:
            return ""

        eol  =  bytes( b"\r" )   # move to instance  \n or \r

        #done = False
        no_waiting   = self.driver.inWaiting()

        if no_waiting == 0:
           # but may have an eol in the buffer already
           #retval = ""
           #return retval
           #   ========== clean up this code if all this i null
           pass
        else:
            # there is some recieved data, filter our cr not yet -- what does arduino send?
            rec_bytes = bytearray ( self.driver.read(size = no_waiting) ) # convert bytes to bytearray  why? scrub some char

            # scrub as many char as desired do not delete eol if need to detect it later

            for i_delchars in self.delchars:
                while True:

                    ix_del = rec_bytes.find( i_delchars )    # neither find or rfind
                    #print ix_del

                    if ix_del < 0:
                        break

                    del rec_bytes[ix_del:ix_del +1]    # delete the character


            self.recBuff = self.recBuff + rec_bytes    # concatinate or append
            #print self.recBuff

        #now look for \n
        ix = self.recBuff.find( eol )   #
        if ix  < 0:
            return ""

        #now finish up save some for buffer and return what have so far
        retval     = ""  + self.recBuff[ 0: ix ]
        self.recBuff    = self.recBuff[ ix + 1: ]    # should be ok even if out of range should get rid of eol

        # check that we have not got end of string marker what is it cr or lf /n

        return retval
#==============================================================================
#         # use in syntax when have figured out
#
#         if '\n' in self.recBuff:
#             lines = self.recBuff.split('\n') # Guaranteed to have at least 2 entries
#             last_received = lines[-2]
#             #If the Arduino sends lots of empty lines, you'll lose the
#             #last filled line, so you could make the above statement conditional
#             #like so: if lines[-2]: last_received = lines[-2]
#             self.recBuff = lines[-1]
#==============================================================================

    # -------------------------------------
    def getRecString1( self, ):
        """
        worked, but problematic, lets try more
        still messing with what I want this to do
        may not get the string untill completed
        strips some special characters
        note: early return
        """

        if self.isopen == False:
            return ""

        #define at instance level
        int_newline  =  ord( "\n" )
        int_cr       =  ord( "\r" )

        done = False
        no_waiting   = self.driver.inWaiting()
        if no_waiting > 0:
            rec_bytes = bytearray ( self.driver.read(size = no_waiting) ) # convert bytes to byte array
        else:
           retval = ""
           return retval
        # check that we have not got end of string marker what is it cr or lf /n
        # use in syntax when have figured out

        if  ( rec_bytes[-1 ] == int_newline ) or ( rec_bytes[-1] == int_cr ):
            # del rec_bytes[-1] do not strip crlf
            done = True
            #print "driver done = True"
        if len( rec_bytes ) > 0 and ( ( rec_bytes[-1 ] == int_newline ) or ( rec_bytes[-1] == int_cr ) ):
            #del rec_bytes[-1]
            pass # no delete above if want to get the crlf's

        self.recData =  self.recData + rec_bytes

        # for quicker recieve, no wait on crlf  --- need to think about this more
        #if len( self.recData )

        if done:
            retval = str( self.recData )
            self.recData = bytearray( "" )
            # save a prior copy??
        else:
            retval = ""

        return retval

    # -------- utility functions, mostly get parameters as strings

#        self.driver.port        =       self.parameters.port
#        self.driver.baudrate    =       self.parameters.baudrate
#        self.driver.parity      =       self.parameters.parity
#        self.driver.stopbits    =       self.parameters.stopbits
#        self.driver.bytesize
    # give argument instead of using self?

    # ---------------------
    def get_comm_type_as_str( self, a_value ):   # should get from driver and branch to right kind of parms
        if a_value is None:
            return "RS232"
        else:
            return a_value

    # ---------------------
    def get_parity_as_str( self, a_value ):
        if a_value is None:
             return self.parity_to_strs[ self.driver.parity ]  # not a function a dict lookup
        else:
             return self.parity_to_strs[ a_value ]

    # ---------------------
    def get_baudrate_as_str( self, a_value ):
        if a_value is None:
            return str( self.driver.baudrate )
        else:
            return str( a_value )

    # ---------------------
    def get_port_as_str( self, a_value ):

        if a_value is None:
            return str( self.driver.port )
        else:
            return str( a_value )

    # -----------------------------
    def get_stopbits_as_str( self, a_value ):

        if a_value is None:
            return str( self.stopbits_to_strs[ self.driver.stopbits ] )
        else:
            return str( self.stopbits_to_strs[ a_value ] )

    # -----------------------------
    # probably should just get the variable, more pythonic?

#    def getBaud( self, a_value ):
#        if a_value is None:
#            return str( self.baudrate )
#        else:
#            return str( a_value )


if __name__ == '__main__':
        """
        run a test with the test controller
        """
        import  test_controller
        a_app = test_controller.TestController(  )
        driver      = a_app.com_driver
        print( driver )
        portList          =  [ "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", ]
        results           = driver.probe_available( portList )

        print( results )
        for i_result in results:
            print( i_result )

        #a_app.test_run_gui()

        print( "====== test done ==============" )
 # ========================== eof ==============================



