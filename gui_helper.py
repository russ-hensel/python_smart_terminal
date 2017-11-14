# -*- coding: utf-8 -*-
#
#plan is to have helper objects and functions to aid in building of gui's



class RowColumnCalc( object ):
    """
    called sequentially to help layout grids in a row and column format

    """
    def __init__(self, arg ):
        self.max_rows = arg
        self.ix_row   =  0
        self.ix_col   =  0
#        self._private              = 6
#        self.__mangled_private     = 9

#    def __repr__(self):
#          return "App Class __repr__"
#
#    # called by str( instance of AppClass )
#    def __str__(self):
#        return "App Class __str__" + " self.arg = " + str( self.arg )

    def foo( self,  ):
        """
        this is a function in the class
        """
        return self.arg




# =========================== eof =========================






