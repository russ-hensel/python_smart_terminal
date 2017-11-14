# -*- coding: utf-8 -*-


import data_feed
import data_point

def ex1():
    adata_feed    = data_feed.Data_feed( "pressure_data.txt" )
    
    for ix in range(0, 20):
            #print ix
            print adata_feed.next_feed()
            
#ex1()


def ex2():
    adata_feed    = data_feed.Data_feed( "pressure_data.txt" )
    adata_point   = data_point.Data_point( )
    for ix in range(0, 20):
            print ix
            data = adata_feed.next_feed()
            adata_point.parse( data )
            #adata_point.printt()
            print adata_point
            
            
            
#ex2()
            
#print float( "123" )

def ex3():
    adata_feed    = data_feed.Data_feed( "pressure_data.txt" )
    adata_point   = data_point.Data_point( )
    for ix in range(0, 20):
            print ix
            data = adata_feed.next_feed()
            adata_point.parse( data )
            #adata_point.printt()
            print adata_point
    adata_point.reset()       
    for ix in range(20, 40):
            print ix
            data = adata_feed.next_feed()
            adata_point.parse( data )
            #adata_point.printt()
            print adata_point
            
            
ex3()
