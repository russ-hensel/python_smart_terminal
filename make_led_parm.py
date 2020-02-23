# -*- coding: utf-8 -*-

"""

this help compute values fpr


       self.led_chime


related to but not part of (for smart_terminal.py )

"""


data      = {}

led       = 50
led       = 1
mulp      = 1.1



for ix in range( -20, 0 ):
        data[ ix ]     = led
        led            = led * mulp

#print( f"data   >>{data}<< " )
#print( "\n\n" )

for ix in range( 0, 20 ):
        data[ ix ]     = led
        led            = led / mulp

print( f"data   >>{data}<< " )