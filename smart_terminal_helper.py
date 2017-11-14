# -*- coding: utf-8 -*-


#import stat
import time

import queue
import logging
import sys
#import datetime
import threading
from   app_global import AppGlobal

# try with subclassing of Thread
# or is this a thread   or just its manager
# In other words, only override the __init__() and run() methods of this class.
# class threading.Thread(group=None, target=None, name=None, args=(), kwargs={})
# If the subclass overrides the constructor, it must make sure to invoke the base class constructor (Thread.__init__()) before doing anything else to the thread.


class HelperThread( threading.Thread ):
    """
    run a second thread not blocked by the gui
    assume all methods run from the second thread unless otherwise stated
    this method will of course have to be called from the gui thread
    this object runs a polling thread looking at queue_to_helper to decide what
    to do
    """
    def __init__(                  self, group=None,  target=None,   name=None, args=(), kwargs=None, verbose=None ):
        """
        call: gt
        """
        threading.Thread.__init__( self, group=group, target=target, name=name,  )
        #threading.Thread.__init__( self, group=group, target=target, name=name, verbose=verbose )   # verbose not throwing an error   say what

        self.args     = args
        self.kwargs   = kwargs
        # see set controller for more instance var
        return

    # ------------------------------------------------
    def set_controller( self, controller ):
        """
        call from gui to finish set up of this object
        """
        # df1 default 1 this is for iomega usb on smithers
        self.controller        = controller
        self.parameters        = controller.parameters

        self.queue_to_helper   = self.controller.queue_to_helper
        print( self.queue_to_helper )
        self.queue_fr_helper   = self.controller.queue_fr_helper
        self.gui_recieve_lock  = self.controller.gui_recieve_lock

        self.logger            = logging.getLogger(  self.controller.logger_id + ".helper" )
        self.logger.info( "smart_terminal_helpe.HelperThread set controller" )        # info debug...

        self.ht_delta_t        = self.parameters.ht_delta_t
        #self.ix_queue_max        = "delete after search"

        #self.queue_length      = self.parameters.queue_length  not needed

        print( "smart_terminal_helpe.HelperThread set controller" )
#        self.change_function   = ( False, "a_function", "function_args" )   # for changing functions

    # ------------------------------------------------
    def run( self ):
        self.polling()   # just to match the names

    # ------------------------------------------------
    def polling(self):
        """
        started from gui this is an infinite loop monitoring the queue
        queue_to_helper
        """
        self.logger.debug(  "smart_terminal_helper.polling()  entered " )

        while True:
            #print( "polling" )
            #data   = self.rec_from_queue( )
            #if not( self.gui_recieve_lock.locked() ):
            data   = self.receive( )
            try:
                ( action, function, function_args ) = self.rec_from_queue()
                if action != "":
                    self.logger.debug(  "smart_terminal_helper.polling()  " + action + " " + str( function ) + " " + str( function_args) )  # ?? comment out
                if action == "call":
                    #print( "ht making call" )
                    sys.stdout.flush()
                    self.controller.helper_task_active  = True
                    function( *function_args )
                    self.logger.debug(  "smart_terminal_helper.polling() return running helper loop "  )  # ?? comment out
                    #self.print_helper_label( "return running helper loop " )
                    self.controller.helper_task_active  = False    # do we maintain this, or move to helper
                if action == "stop":
                    # this will kill the thread
                    self.controller.helper_task_active  = False
                    return
                if  AppGlobal.abc_processing != None:
                    AppGlobal.abc_processing.polling_ext()
            except HelperException as he:
                self.logger.info( "smart_terminal_helper.HelperThread throw execption from " + he.msg )        # info debug...
            
            #print( )

            time.sleep( self.ht_delta_t )  # ok here since it is the main pooling loop

        return

    # ------------------------------------------------
    def find_arduino( self, ):
        """
        try opening a list of ports and see if any respond with a string which contains
        send self.parameters.get_arduino_version and try to get self.parameters.arduino_string
        ret: tuple ( worked, port )
        call: ht

        """
        # lets make a list starting with the port in parameters, then the ports reported by ports found
        # then the ones in self.parameters.port_list
        #self.release_gui_for( .0 )
        # !!  looks like python report not used in driver  add this or not
        gui    = AppGlobal.gui
        
        self.print_info_string( "Looking for Arduino " + self.parameters.arduino_version )
        
        port_list  = []
        port_list.append( self.parameters.port )
        for i_port in self.parameters.port_list:
            if not( i_port in port_list ):
                port_list.append( i_port )

        a_result  = self.test_ports( port_list, self.parameters.get_arduino_version,  self.parameters.arduino_version )   # ( Boolean, port )
        #self.release_gui_for( .0 )
        return a_result

    # ------------------------------------------------
    def test_ports( self, a_port_list, a_get, a_valid_response ):
        """
        arg:  a_port_list
              a_get              string to send out port
              a_valid_response   string, must be a substring in the response to be valid
        ret: tuple ( boolean_worked, port_as_string )
        called from ht

        """
        self.logger.info( "smart_terminal_helper.test_ports()" ) # " + data  + "^^^",  )
        #gui    = self.controller.gui
        self.print_helper_label( "test_ports testing ports" )

        self.print_info_string(  "Probing Ports...." )    # rec send info
        #self.release_gui_for( .1 )
        # gui.set_open( status ) # set_port
        for i_port in a_port_list:
            # self.print_helper_label( "i_port " )
            is_ok  = self.test_port( i_port, a_get, a_valid_response )
            if is_ok:
                 # self.helper_label.config( text = "is_ok " )
                 self.print_helper_label( "is_ok " )
                 return ( True, i_port )

        return ( False, "" )

    # ------------------------------------------------
    def end_helper( self, ):
        """
        a function to interrupt the help thread and go back to polling
        function called to end the helper subroutine
        if another functin is running posting for this
        will cause it to throw an exception
        ends request_to_pause
        helper thread only
        """
        self.print_helper_label( "end_helper " )
        #self.helper_label.config( text = "test_ports testing ports" )
        #self.print_info_string( "Helper Stopped" )
        #self.post_to_queue(  "info", None, ( "Helper Stopped", ) )
        self.print_info_string( "Helper interrupted" )    # rec send info
        self.logger.debug(  "end_helper( ) Helper interrupted" )

    # ------------------------------------------------
    def test_port( self, a_port, a_get, a_valid_response ):
        """
        ?? just a start for a more complete function
        test port for presence of correct arduino, except for a_port use parms from parameters
        close port
        open port
        get version usina_valid_response as a substring
        validate
        close port
        call: ht
        args: a_port the port name, a_valid_response = string that needs to be in the arduino response.
        ret:  success = True if open and right version
        """
        gui    = self.controller.gui    # !! this may not be so good, direct interaction with gui


        self.print_info_string( "Testing Port " + a_port + "..." )
        test_good  = False

        #self.helper_label.config( text = "test_port " + a_port )
        self.print_helper_label( "test_port " + a_port )

        # ------- protected

        self.controller.com_driver.close( )

        self.sleep_ht_for( .2 )
        is_open    = self.controller.com_driver.open( a_port )
        if not ( is_open ) :
            #print( "port did not open" )
            self.post_to_queue(  "info", None, ( "Testing Port " + a_port + "..." ) )
            self.post_to_queue(  "info", None, ( "    did not open"               ) )
            return test_good

        self.print_helper_label( "test_port " + a_port + " open" )
        #self.print_info_string( a_port + " open"  )

        self.post_to_queue(  "info", None, ( a_port + " open" ) )
        #self.release_gui_for( .1 )
        self.sleep_ht_for( .2 )
        # print status to current ports
        gui.set_port( a_port )
        gui.set_open( "Open" )

        #self.release_gui_for( 10. )
        self.print_info_string(  "Port open, test for arduino...." )
        self.sleep_ht_for( 5. )
        data = self.send_receive( self.parameters.get_arduino_version, 10.  )    #  send_receive( self, send_data, for_time  ):

        ix  = data.find( a_valid_response, 0, len( data ) )

        if ix != -1:
            self.print_info_string( "Version good: " +  self.parameters.get_arduino_version )
            test_good = True
            #self.post_to_queue(  "call", self.controller.gui.showRecFrame, ( "Version good: \n" , ) )
            pass
        else:
            #self.controller.gui.print_info_string( "Version not so good: got " + data + "\n" )
            self.post_to_queue(  "info", None, ( "Version not so good: got " + data + "\n" ) )
            self.logger.info( "Version not so good:^^^" + data  + "^^^",  )
            self.controller.com_driver.close( )
            test_good = False
        # is_open  = self.controller.com_driver.open( a_port )

        # -------

        self.controller.request_to_pause = False
        self.controller.gui.show_item( "helper_info", "test_port done " )
        #self.helper_label.config( text = "test_port done " )
        return test_good

    # ------------------------------------------------
    def print_info_string( self, text ):
        """
        print info string using the queue, so thread safe

        helper thread only
        as an alternative use the queue which does not block the gui
        """
        self.post_to_queue(  "info", None, ( text ) )  # info gui.print_info_string goes to reciev area

        return

    # ------------------------------------------------
    def post_info_stringxxxxx( self, text ):
        """
        call from: helper only
        post info string for printing in gui, does not block the gui
        leaving unchanged
        helper thread only
        as an alternative use the queue which does not block the gui
        """
        "rec"
        gui    = self.controller.gui
        # self.release_gui_for( .01 )
        #self.helper_label.config( text = "end_helper " )
        #self.helper_label.config( text = "test_ports testing ports" )
        if self.controller.request_to_pause:
              gui.print_info_string( text )
        else:
            self.release_gui_for( .01 )
            gui.print_info_string( text )
            self.release_gui_for( .0 )

        return

    # ------------------------------------------------
    def print_helper_label( self, a_text ):
        """
        from helper thread, no need for lock   !! this may not be true, comment out now post to queue later -- did not fix my problem
        helper thread only
        """
        #self.helper_label.config( text = a_text )  # old bad way
        #self.controller.gui.show_item( "helper_info", a_text )
        # add a release untill   def release_gui_for_until

    # ------------------------------------------------
    def sleep_ht_with_msg_for( self, for_time,  msg, repeat_time, show_time ):
        """

        count down a time, with a message every repeat_time to gui
        """
        pass
        time_left  = for_time
        # message here
        while( True ):
            show_msg = msg + " ( time left: " + str( time_left) + ")"
            self.print_info_string( show_msg )
            if  time_left > repeat_time:
                 self.sleep_ht_for( repeat_time )
                 time_left   -= repeat_time
            elif time_left > 10.:
                 self.sleep_ht_for( time_left  )
                 time_left   = 0
            else:
                 return

    # ------------------------------------------------
    def sleep_ht_for( self, for_time ):
        """
        this is a way to pause action in the ht while keeping
        recieve active
        have it end if anything is recieved??
        args: for_time number of seconds to stay here
        """
        wait_till   = time.time( ) + for_time
        while ( time.time( ) < wait_till ):

             time.sleep( self.ht_delta_t  )
             data = self.receive()   # this data will be printed but lost to this thread

             if  ( self.queue_to_helper.empty() ):   # this is used to break out of loop
                 pass
             else:
                 self.logger.info( "raise HelperException",  )
                 raise HelperException( 'in sleep_ht_for - queue not empty breaking back to helper thread polling ...' ) #, queue_item )

        return

    # ------------------------------------------------
    def release_gui_untilxxxx( self, until_time ):
        """
        arg: until_time ( a time, like time.time() ) untill which the gui will be
        ret: zip
        throws: HelperException if anything comes in on queue

        released to run, if until_time = 0. then gui relaeased "forever"
        !! not implemented
        release for time, then relock, if for_time == 0.
        release "forever"
        release the main thead from its polling loop for time in float seconds
        can also call to get controller to pause again
        need to keep recieving, and keep eye on queue
        () = self.release_gui_for( time )
        also risk of lock up if controller does not respond
        have an exit with exception ??
        if exception will cause request_to_pause = False
        helper thread only
        """

        if until_time == 0.:
            self.controller.request_to_pause = False
            return

        wait_till   = until_time

        self.controller.request_to_pause = False

        while ( time.time( ) < wait_till ):

             time.sleep( .1 )
             data = self.controller.receive()  # !! FIX IS REINABLED

             if  ( self.queue_to_helper.empty() ):
                 pass
             else:
                 # ( action, function, function_args ) = self.rec_from_queue()

                 # queue_item  = self.rec_from_queue()
                 self.logger.info( "raise HelperException",  )
                 raise HelperException( 'in release_gui_for' ) #, queue_item )

        self.controller.request_to_pause = True

        if  not(   self.controller.paused ):
            time.sleep( .1 )

        return

    # ------------------------------------------------
    def release_gui_forxxxx( self, for_time ):
        """
        release for time, then relock, if for_time == 0.
        release "forever"
        release the main thead from its polling loop for time in float seconds
        can also call to get controller to pause again
        need to keep recieving, and keep eye on queue
        () = self.release_gui_for( time )
        also risk of lock up if controller does not respond
        have an exit with exception ??
        if exception will cause request_to_pause = False
        helper thread only
        """
        if for_time == 0.:
            self.controller.request_to_pause = False
            #print( "helper controller.request_to_pause = False" )
            return

        wait_till   = time.time( ) + for_time

        self.controller.request_to_pause = False

        while ( time.time( ) < wait_till ):

             time.sleep( .1 )
             data = self.controller.receive()   # fix if reenabled

             if  ( self.queue_to_helper.empty() ):
                 pass
             else:
                 # ( action, function, function_args ) = self.rec_from_queue()

                 # queue_item  = self.rec_from_queue()
                 self.logger.info( "raise HelperException",  )
                 raise HelperException( 'in release_gui_for' ) #, queue_item )

        self.controller.request_to_pause = True

        if  not(   self.controller.paused ):
            time.sleep( .1 )

        return

    # --------------------------------------------------
    def rec_from_queue( self, ):
        """
        call from helper only, is looked for in the method run when polling.
        get item from queue if any.
        ret: tuple as below, if action == "" then nothing rec from queue
        ( action, function, function_args ) = self.rec_from_queue()
        """

        # why not use Queue.empty() bool function ?? in code below have wrong kind of exception
        # got error  except Queue.Empty:  AttributeError: 'NoneType' object has no attribute 'Empty'
        is_empty = False
        try:
            action, function, function_args   = self.queue_to_helper.get_nowait()
        except queue.Empty:
            action          = ""
            function        = None
            function_args   = None
            is_empty        = True

        if not( is_empty ):
            self.logger.debug( "in helper, rec_from_queue  " + action + " " + str( function ) + " " + str( function_args) )  # ?? comment out

#        if action == "call":
#              self.change_function   = ( True, function, function_args  )   # why is return not good enough looks dead
#        if action = "rec":            # instead of this take over the recive task while active
#              pass
        return ( action, function, function_args )

    # ----------------------------------------------------------
    def parse_out_floats( self, line, ):
        """

        parse out a string with data in the form of numbers which will be returned as floating point numbers
        unit tests: yes
        call: ht
        args: line a string like:  "122 592"
        ret: tuple( success_flag,  list of floats )  if failure, failed number is put in list as a 0
        """
        ok       = True
        values   = []
        sdatas   = line.split()

        for  i_sdatas in sdatas:

            try:
                value = float( i_sdatas.strip() )
                values.append( value )
            except:
                #print "parse not float exception  ", ix_sdatas.strip()
                self.logger.error( "parse not float exception  " + str( i_sdatas.strip() ) )
                values.append( 0. )
                ok       = False

        return ( ok, values )

    # -------------------------------------------------------
    def open_port ( self, a_port ):
        """
        call:helper thread only
        arg: string with port name
        ret: boolean success
        seffect: will block the gui briefly
            will release any gui lock
        """
        self.controller.request_to_pause = True

        if  not(   self.controller.paused ):
            time.sleep( .1 )

        is_open  = self.controller.com_driver.open( a_port )

        self.controller.request_to_pause = False

        return is_open

    # -------------------------------------------------------
    def send_receive( self, send_data, for_time  ):
        """
        sends some data and waits for time to recieve a reply
        (       )

        ?? add flag to control throwing of exception  or message for exception
        sends a string, recieves a string, in meantime checks queue

        receive data via the comm port
        display data
        rec_data = helper.send_receive( send_data, for_time  )
        for_time is the max time else throw exception

        after timeout then throw exception
        call:    helper thread only
        args:    sends send_data, waits max time = for_time
        returns: recieved_data or  "" if times out  no throw exception if times out
        throws:  HelperException if queue is not empty
        -----
        receive only full strings ending with /n else
        accumulated in the driver /n is stripped
        call: ht
        ret:  non empt string or throws exception
        """
        #self.logger.info( "helper: send_receive() entered",  )
        wait_till   = time.time( ) + for_time

        # ?? note fix up
        #self.controller.send( send_data )      # causing a problem, post to queue ??
        self.controller.com_driver.send( send_data )
        self.post_to_queue(  "send", None, ( send_data, ) )   # ?? beware may not actually send so send above

        while ( time.time( ) < wait_till ):

             time.sleep( self.ht_delta_t  )  # ok because we are checkin recieve and queue
             # use of controller.recieve ng use only self.recieve     feb 2017
             # data = self.controller.receive()
             data = self.receive()
             if not( data == "" ):
                 return data

             if  ( self.queue_to_helper.empty() ):
                 pass
             else:
                 # ( action, function, function_args ) = self.rec_from_queue()
                 # queue_item  = self.rec_from_queue()
                 self.logger.info( "raise HelperException in send_receive",  )
                 raise HelperException( 'in send_receive' ) #, queue_item )
        self.logger.info( "send_receive() timeout",  )
        return ""  # timeout

    # -------------------------------------------------------
    def receive( self,  ):
        """
        call: helper thread only
        receive data via the comm port
        display data
        return data   "" if no data
        -----
        receive only full strings ending with /n else
        accumulated in the driver /n is stripped
        """

#       new implementation not blocking gui temp remove
        data = ""

#        if not( self.gui_recieve_lock.locked() ):
#            data = self.controller.receive()  # !! does NOT FIX  its own display, check this removed, helper should not make direct calls to gui

        data = self.controller.receive()
        if not(data == ""):
            self.post_to_queue(  "rec", None, ( data, ) )
        return data

    # --------------------------------------------------
    def post_to_queue( self, action, function, args ):
        """
                post args to the queue to the controller
        call from: helper thread
        args: action=string, function=a function, args=tuple of arguments to function
        ret: zip

        example uses:
        self.post_to_queue(  action, function, args_as_tuple )
        self.post_to_queue(  action, function, arg_a_string )   # ok will be converted to a tuple
        self.post_to_queue(  "call", function, args_as_tuple )
        self.post_to_queue(  "rec",  None, ( "print me", ) )    # rec send info
        self.post_to_queue(  "send", None, ( "print me", ) )
        self.post_to_queue(  "info", None, ( "print me", ) )    # rec send info
        """
        # convert to make calling more flexible esp
        if type( args ) is str:
            args = ( args, )

        loop_flag          = True
        ix_queue_max       = 100
        self.ix_queue      = 0   # why instance
        # self.release_gui_for( .0 )
        while loop_flag:
            loop_flag      = False
            self.ix_queue  += 1
            try:
                #print( "try posting " + action + " args= " + str( args ) )
                self.queue_fr_helper.put_nowait( ( action, function, args ) )
            except queue.Full:
                # try again but give polling a chance to catch up
                print( "helper queue full looping" )
                self.logger.error( "helper post_to_queue()  queue full looping: " +str( action ) )
                # protect against infinit loop if queue is not emptied
                if self.ix_queue > ix_queue_max:
                    #print "too much queue looping"
                    self.logger.error( "helper post_to_queue() too much queue looping: " +str( action )  )
                    pass
                else:
                    loop_flag = True
                    time.sleep( self.parameters.queue_sleep )   # ??

    # ------------------------------------------------
    def toggle_lockxxxxx(  self,  ):
        """
        gui thered call back from test button
        this is just a test function
        """
        # just for testing to see if can pass recieve back and forth
        if self.gui_recieve_lock.locked():
            self.gui_recieve_lock.release()
        else:
            self.gui_recieve_lock.acquire()

    # ------------------------------------------------
    def write_csv(  self, data_string  ):
        """
        write a string followed by data_string comma seperated values,
        args: data_string data to be written, should have commas in place ie: "123., 456., 10"
        call: helper thread only
        ret: nothing
        """
        a_line     =  data_string + "\n"
        outfile    = open(  self.parameters.csv_filename, 'a')
        outfile.write( a_line )
        outfile.close()
        return

# ================= Class =======================
# Define a class is how we crash out
class HelperException( Exception ):
    """
    raise if in call and get another item in queue
    """
    # ----------------------------------------
    def __init__(self, msg, ): # queue_item ):
        # call ancestor ??
        # Set some exception information
        # currently pretty much a test
        self.msg         = msg    # string message
        #self.queue_item  = queue_item


# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    print( "" )
    print( " ========== starting SmartTerminal from smart_terminal_helper.py ==============" )
    import smart_terminal
    a_app = smart_terminal.SmartTerminal(  )







