# -*- coding: utf-8 -*-

import moving_average

import sys

period   = 15

#mv    = moving_aveage.Movingaverage( period  )
mv    = moving_average.Movingaverage( period  )


# -*- coding: utf-8 -*-

filein_name    = "filein.csv"
filein_name    = "filein_2.csv"


fileout_name   = "fileout.csv"

print    "opening files"
filein  = open( filein_name, "r"  )

fileout = open( fileout_name, "w" ) #) "a" )  a for append

#data    = filein.read()     #  read( size )   size defaults to whole file 
data    = filein.readlines()


def new_loop():
    for i_data in data:
        #print i_data
        #print "=========", i_data, "-------------------"
       # print "len = ", len( i_data )
        ii_data   = i_data.strip("/r/n")    # 
 
        i_num     = int( ii_data )
        
        o_num  = mv.nextVal( float( i_num ) )
        
        fileout.write( str( o_num ) + "\r"  )
      

# data may still have nl on end 
def old_loop():
    for i_data in data:
        #print i_data
        print "=========", i_data, "-------------------"
        print "len = ", len( i_data )
        ii_data   = i_data.strip("/r/n")    # 
        #i#i_data   = ii_data[ 1: ]   # 
        print "ii_data = ", ii_data
        print "ord = ", ord( ii_data[0])
        print "len = ", len( ii_data )
        sys.stdout.flush()    # try not to let logged info linger
        
        #print "4"
        #iii_dat   = "1"
        #i_num     = int( iii_dat )    
        #i_num     = int( "4" )
        
        if ord( ii_data[0]) == 10:
            continue
        
  
        if len( ii_data ) < 1:   
            continue
        
        i_num     = int( ii_data )
        #fileout.write( str( ))
        fileout.write( str( i_num ) + "\r"  )
        #fileout.write( str( i_num ), "/r"  )
    
    #new_splits = new_splits + ( adata.split( "\n" ) )

#data_splits = new_splits
#print "data_splits", data_splits
#
## may want to get rid of the blank ones, do with list completion?
#
#for adata in data_splits:
#      # delete bad data   
#      
#
#      fileout.write( adata + "\n" )

#f.write("and can I get some pickles on that\n" )
#f.write("please\n" )
#f.close()


new_loop()

filein.close()
fileout.close()


print "we are done"