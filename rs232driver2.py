# -*- coding: utf-8 -*-

"""
this driver is for rs232 comm ports
it returns only full lines
eol is expected to be a cr,
if newlines nl are present then they are deleted and ignored

has the ability to delete other charcters in a list, but now just used for nl
now uses standard loggging -- but not correctly configured !!
!! log port failure

"""

import  logging
#import antigravity
import serial
import sys
import serial.tools.list_ports

# ================= class ======================
class RS232Driver:


    def __init__(self,  controller  ):

        self.name          = "RS232Diver2  2016 Mar 03.1"

        self.controller   = controller

        self.parameters   = controller.parameters
        #self.myLogger       = aController.myLogger
        self.logger       = logging.getLogger( "RS232Driver" )   # assign to logger or get all the time does logger have aname or does this assign

        self.driver         = serial.Serial()

        self.isopen         = False

        self.recBuff        = ""    # buffer recieved data

        self.recData        = bytearray( "" )    # data that has been recieved.

        # this may be overengineering really only want to delete cr  -- us lf or nl \n as end of string marker
        self.delchars =  []
        #self.delchars.append( bytes( b'\x0D' ))      # 13	015	0D	00001101	CR
        self.delchars.append( bytes( b'\x0A' ))      #           0A	          LF

        #self.delchars.append( bytes( b'\x44' ))      # D and up start as  b'\x44'
        #self.delchars.append( bytes( b'\x45' ))
        #self.delchars.append( bytes( b'\x46' ))
        #self.delchars.append( bytes( b'\x20' ))     # space    b'\x20'

        '''
        this was for simulator  -- code moved, think it is another driver
        self.gotDataBuff    = ""   # simulated data for next recieve.
        self.gotDataIx      = 0
        self.gotDataData    = []
        self.gotDataData.append( "rec" )
        self.gotDataData.append( "eived" )
        self.gotDataData.append( "\n" )
        self.gotDataData.append( "666\n" )
        self.gotDataData.append( "3.1415" )
        self.gotDataData.append( "9\n" )
        self.gotDataData.append( "russ\n" )
        self.gotDataData.append( "xxy" )
        self.gotDataData.append( "y\n" )
        self.gotDataData.append( "rec" )
        self.gotDataData.append( "penultimate\n" )
        self.gotDataData.append( "end\n" )
        '''

# --------------------------------------
    def getName( self, ):

        return self.name

# --------------------------------------
    def getOpen( self, ):

               return self.isopen

    def close(self, ):

        #self.controller.log( "closing com", "print"  )
        self.driver.close()
        self.isopen  = False

        return

# --------------------------------------
    def open(self, port = None ):
        """
        tries to open port
        returns true if port opens
        gets parms itself see setParms
        """

        #self.controller.log( "opening com driver", "print"  )
        self.setParms()

        if port <> None:
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

        """

        self.send( send )

        #rec_time  = 2     # get from parameters
        #ts_start = time.time()
        ts_end   = rec_time + time.time()

        # give it a while to get the data, so loop for a bit

        while ( time.time() < ts_end ):


            new_data  = self.myDriver.getRecString( )
            if new_data <> "":
                 data   = data + new_data

        ret_val = ( data[0:len(rec)] == rec  )   # should compare have - 1

        return ret_val

# --------------------------------------
    def listAvailable( self, ports = None ):
        """
        how do we switch methods, ........
        *use the api from python serial
        *try to open them
        """
        if ports == None:
            return (list(serial.tools.list_ports.comports()))
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


    def setParms(self, ):
        """
        set the parameters of the port from Parameters instance
        todo   make sure port closed first?  set status to self.isopen = False

        """

        self.driver.port        =       self.parameters.port
        self.driver.baudrate    =       self.parameters.baudrate
        self.driver.parity      =       self.parameters.parity
        self.driver.stopbits    =       self.parameters.stopbits
        self.driver.bytesize    =       self.parameters.bytesize

        #ser = serial.Serial(0)
        #self.recTimeout          = self.parameters.recTimeout

        return self.name

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
        version 2 -- so far recieves some not all stuff

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
                    #rawData.remove( index3 )    failed
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

        return retval

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


 # ========================== eof ==============================

