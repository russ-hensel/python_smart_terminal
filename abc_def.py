# -*- coding: utf-8 -*-
import abc

# ================= Class =======================
class ABCProcessing( object ):
    __metaclass__ = abc.ABCMeta

#    # ----------------------------------------
#    def __init__( self, ):
#        pass

    # ----------------------------------------

#    @abc.abstractmethod
    def load( self, input ):
        """Retrieve data from the input source and return an object."""
        return

    # ----------------------------------------
    @abc.abstractmethod
    def add_gui( self, parent, ):
        """
        make a frame for placement, or if no additional component return None
        """
        pass
    
        # ----------------------------------------
    @abc.abstractmethod
    def polling_ext( self, ):
        """
        an additional polling function if the processing wants to extend, can just be return None
        """
        pass


#    # ----------------------------------------
#    @abc.abstractmethod
#    def make_task_list( self ):
#        """
#
#        """
#        pass


    # ----------------------------------------






