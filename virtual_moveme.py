# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 18:20:54 2020

@author: Russ_2
"""

import sys

def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

if is_venv():
    print('inside virtualenv or venv')
else:
    print('outside virtualenv or venv')