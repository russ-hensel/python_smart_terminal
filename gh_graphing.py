# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt     # plotting stuff
import pylab
import logging

class GraphDB:

    def __init__(self, controller   ):

        self.controller     = controller    # save a link to the controller
        self.parameters     = controller.parameters
        #self.myLogger       = aController.myLogger
        self.logger         = logging.getLogger( self.controller.logger_id + ".gh_graphing.GraphDB")
        self.logger.info("in .gh_graphing.GraphDB") # logger not currently used by here

        self.db             = controller.db

    def testGraph( self ):
        """
        fetch data from database print and do a simple graph
        """
        self.logger.info( "gh_graphing.GraphDB.testGraph", )

        timeData       = []
        y1Data         = []
        y2Data         = []

        sql    = "select * from pressure_history order by ph_timestamp desc"
        sql    = "select * from pressure_history order by ph_timestamp asc"

        sql    = "select * from gh_data_2 order by gh_time asc"

        #sql    = "select gh_time, temp_1, from gh_data_2 order by gh_time asc"

        sql    = "SELECT gh_time, temp_1 FROM gh_data_2 order by gh_time asc"
        sql    = "SELECT gh_time, humid_1 FROM gh_data_2 order by gh_time asc"

        sql    = "SELECT gh_time, temp_1, humid_1 FROM gh_data_2 order by gh_time asc"

        cur = self.db.db_connection.cursor()
        cur.execute( sql )
        #cur.execute("select * from pressure_history order by ph_timestamp asc")

        #print(cur.description)
        #print()

        print "fetch and print time and temp data"

        # get rows one at a time in loop
        while True:
           row   = cur.fetchone()
           if row is None:
               break
           timeData.append( row[0] )
           y1Data.append( row[1] )
           y2Data.append( row[2] )

           print row[0],
           print row[1]

        #print timeData
        #print pressureData
        # use row as itterator
        #for row in cur:
           #print(row)

        self.fig = plt.figure( figsize=(12, 12) )

        #self.axes = self.fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)

        self.axes = self.fig.add_subplot(111)  # to have multiple lines in the plot

        self.axes.set_xlabel( 'Time' )
        self.axes.set_ylabel( 'Temp-Humid' )           #

        self.axes.set_title( "Temp. and Humid. vs Time" )

        self.axes.set_ylim([ self.parameters.graph_min ,  self.parameters.graph_max ])

        self.axes.plot(  timeData, y1Data, linestyle='--', marker='o', color='b'  )
        self.axes.plot(  timeData, y2Data, linestyle='-',  marker='*', color='r'  )


        plt.show( self.fig )    # need to move to a window

        #self.myLogger.log( "GraphDB.testGraph end ",  1 )

        self.logger.info(  "gh_graphing.GraphDB.testGraph end " )

        return







