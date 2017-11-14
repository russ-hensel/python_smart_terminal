# -*- coding: utf-8 -*-




import sys

#import importlib
import sys
sys.path.append( "../rshlib" )


#import gui
import os
#from   time import sleep
#from   time import time
import time




import data_point
import db
import logger
import parameters
import moving_average




class TestDB:
    """
    test db, data point, average.........
    generally using csv or other file for input
    also tests data_point 

    """
    def __init__(self, CSVMode = None   ):

        """


        """

        self.myParameters   = parameters.Parameters( self ) # open early may effect other

        self.myLogger       = logger.Logger( self )
        self.myLogger.open()  # later should get file from parameters??

        self.name           = "TestDB"

        self.db             = db.DBAccess( self, CSVMode = True  )
        self.data_point     = data_point.DataPoint( )


    def logit( self, msg ):
        # self.logit( "msg" )

        self.myLogger.log( msg )


    def test_1( self, ):
        """
        """
        timex  = 100000.
        filein  = open( "filein.csv", "r"  )
        filein  = open( "pressure_data_2.csv", "r"  )
        data    = filein.readlines()

        app.db.dbConnect()

        for i_data in data:
            splits   = i_data.split( "," )
            pdata     = splits[0].strip()
            tdata     = splits[1].strip()
            #self.logit( tdata )

            self.data_point.parse_test( pdata, tdata )   # for testing time from file
            #self.data_point.parse( pdata )

            #self.logit( str(  self.data_point.pressure  ))
            app.db.dbNewValues( self.data_point.time,  self.data_point.pressure, 0 )
            #app.db.dbAddRow(    self.data_point.time,  self.data_point.pressure, 0 )

        app.db.dbClose()


if __name__ == '__main__':


        app = TestDB( CSVMode = True  )

        app.test_1()

        app.logit( app.name + ": all done" )
        app.myLogger.close()







# ============================= eof ===================