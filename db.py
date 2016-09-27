# -*- coding: utf-8 -*-



# !! add some test stuff for connect and add row, run with test controller







#import mysql.connector
#from   mysql.connector import errorcode

import  logging
import  pymysql
import  os
import  time
#import  importlib
import sys


sys.path.append( "../rshlib" )
#sys.path.append( "./" )
#import logger

import  parameters


class DBAccess:
    """
    connect to db
    add data
    decide if data is new enough to be added
    not general purpose but for the well monitor app
    """

    def __init__(self, aController, CSVMode = False   ):
        """
        set up fro db connection, at least at some point
        also made the connection
        has a test mode
        """
        self.myName         = "DBAccess"
        self.version        = "2016 june 22"

        self.controller     = aController
        self.parameters     = aController.parameters
        # self.myllogger       = aController.myllogger
        self.logger        = logging.getLogger( self.controller.logger_id + ".DBAccess")
        self.logger.info("in class DBAccess init")

        #self.log = logging.getLogger( "well" )   # assign to logger or get all the time does logger have aname or does this assign
        #self.log = logging
        self.logger.info( "In DBAccess init ", )

        self.CSVMode        = CSVMode

        self.fileout        = None

        self.db_open        = False
        self.db_connection  = None       # another indicator of no connection

        # Initialize so that will need new value in db on first call
        # !! move to processing, delete all ref
        self.last_pa        = -1
        self.last_time      = 0
        self.last_on        = -1

        # !! move to processing, delete all ref
        self.db_delta_t     = 5      # max time between postings
        self.db_delat_p     = 5       # max pressure change between postings

        self.dbConnect(  )   # perhaps move out of init

        return

    #================================
    def dbConnect( self,  ):
        """
        connect to the db and save connection and state
        uses parameters for connection parameters
        !! need more error handeling
        """

        if self.CSVMode :
            self.fileout = open( "CSVMode.csv", "w" )
            return

        try:
            self.logger.info(  "DBAccess try a connection " )
            #conn = pymysql.connect( host='127.0.0.1', port=3306, user='root', passwd='FreeData99', db='well_monitor_1')

            conn = pymysql.connect(   host    = self.parameters.db_host,
                                      port    = self.parameters.db_port,
                                      db      = self.parameters.db_db,
                                      user    = self.parameters.db_user,
                                      passwd  = self.parameters.db_passwd,
                                          )

        except Exception, e:

            self.logger.error( "got exception on connect" )

            self.logger.error( self.parameters.db_host )
            self.logger.error( self.parameters.db_port )
            self.logger.error( self.parameters.db_db   )
            self.logger.error( self.parameters.db_user )
            self.logger.error( self.parameters.db_passwd )

            print "got exception on connect"
            print e

            self.db_open        = False

            return
#     except mysql.connector.Error as err:
#       if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#         print("Something is wrong with your user name or password")
#       elif err.errno == errorcode.ER_BAD_DB_ERROR:
#         print("Database does not exist")
#       else:
#         print(err)
#     else:
#       cnx.close()

        self.logger.info(   "dbConnect got connection " )
        self.db_connection  = conn
        self.db_open        = True

        # self.test_retrieve() for testing

    #================================
    def test_retrieve( self,  ):
        """
        just for fun and testing  do a fetch
        """

        cur = self.db_connection.cursor()
        cur.execute("select * from pressure_history")

        print(cur.description)
        print()

        for row in cur:
           print(row)

        #cur.close()
        #conn.close()

    #================================
    def dbClose( self,  ):
        """
        !! do we need to check if open?
        in fact it may not exist check against none??
        note early return
        """
        if self.CSVMode :
            self.fileout.close()
            self.db_open        = False
            self.db_connection  = None
            return

        if self.db_connection is None:
            self.db_open        = False
            return

        self.db_connection.close()
        self.db_open        = False
        self.db_connection  = None


    #================================
    def dbAddRow( self, ts, pressure, well_on ):
        """
        add a row to the pressure_history table
        !! may want some error checking
        return nothing??
        """
        log_msg  = "dbAddRow " +  str(ts) + " " + str( pressure )
        #print( log_msg )
        self.logger.info( log_msg )

        if self.CSVMode:
            db_string   = ( "insert into pressure_history, " +
                            str( ts ) + ", " +
                            str( pressure ) + ", " +
                            str( well_on ) )

#                            "( ph_timestamp, ph_pressure_a, ph_well_on ) " +
#                            "values (%s, %s, %s)" )
            #fileout.write( str( o_num ) + "\r"  )
            self.fileout.write( db_string + "\r"  )

            return

        add_ph       = (    "insert into pressure_history"
                            "( ph_timestamp, ph_pressure_a, ph_well_on ) "
                            "values (%s, %s, %s)"                         )
        print ( add_ph )

        data_ph       = ( ts, pressure, well_on )

        cursor        = self.db_connection.cursor()
        cursor.execute( add_ph, data_ph )

        self.db_connection.commit()

    #================================
    def dbNewValues( self, ts, pressure, well_on ):
        """
        update db if new values require it
        note early return
        """
        log_msg  = "dbNewValues data at ts " +  str(ts) + " " + str( pressure )
        # print( log_msg )
        self.logger.info( log_msg )

        need_update    = self.needUpdate( ts, pressure, well_on )

        if not( need_update ):
            return

        self.last_time      = ts
        self.last_pa        = pressure
        self.last_on        = well_on
        print " >>> add it "
        self.dbAddRow( ts, pressure, well_on )

    #================================
    def logit( self, adata ):
        """
        for compatibility with old code
        !! clean up
        """
        self.logger.info( adata )
        return

    # ---------------------------------------
    def log( self, adata, ato ):
        """
        just a call to logger
        is this needed/used, can component
        call directly?
        !! clean up
        """

        self.logger.info( adata  )

        return

    # ---------------------------------------
    def isDiff( self, another_point ):
       """
       compare vaues to see if this is significantly different
       a bit overdone, partly for future expansion
       """

       if self.time  is None :
               return False                # we must have no data

       if another_point is None:           # something is different than nothing
               return True

       if another_point.time  is None:
               return True                 # something is different from nothing

       if ( another_point.time        - self.time   )    > self.deltaTime:
               return True

       # next is done only if we have data

       if self.pressure is not None:
           if another_point.pressure is None:
               return True

       if abs( another_point.pressure   - self.pressure   ) > self.deltaP:
               return True

       return False

    # ---------------------------------------
    def needUpdate( self, ts, pressure, well_on ):
        """
        ! note early return
        !! dup with isfiff?
        """

        if ts >  self.last_time  +  self.db_delta_t:    # pre-compute ??
            return True

        #print "pressure"
        #print self.last_pa
        if abs( pressure - self.last_pa )  >  self.db_delat_p:
            return True

        if abs( self.last_on != - well_on ):
            return True

        return False


# ================================ eof =================================