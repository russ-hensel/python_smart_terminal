readme_rsh.txt for the smart_terminal application


======================= short term important temp notes

should times be passed to chime hr..... or use selr.xxxx now using self.

should chime and time have its own instance of parameters, for now using appglobal

.helper_thread     and .helper_thread_ext     think fixed


=============================== begin of real doc ===========

A smart terminal especially for use over a serial port with microcontrollers
last tested in Python 3.6 under windows 10
Author: Russ Hensel
github: https://github.com/russ-hensel/python_smart_terminal



======================================================
# History/ToDo  ** = when done   !! = planned or considerd ?? = think about
#   Copied from mcuterminal, perhaps update from there time to time ( aug 2015 )

    !! work on restart in polling
    !! add launch grapher
#   ?? give grapher access to terminal parameters
#
    !! add edit for comm log

    *! improve doc, structure clean up
#   *! look at goto for looping have done a task need to coordinate with an arduino prog and a list.
    *! continue to clean up prints and logging
    ** add pylog to gui
    ?? limit string length as option configure from parameters
    ?? gray out invalid buttons, open close or just use one with toggle
    !* redirect print to logging file
#   ** turn on task should it make sure port is closed wrong put in task list if you want it
#   !! add IR features   ir_gui  ir_processing
#   !! try ports and use one with correct response
#   !! set up a second thread
#   !! reboot pi as necessary
#   !! send emails
#   !! only probe if port is closed
    ** add comm logging -  still need a button to access

added spacer frame at bottom of the window, in parm file as well -- this to make ras pi ui more readable

extension modules
a   b   c

D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_ddc.py
D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_ddc_bak.py
D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_env_monitor.py
D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_example.py
D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_gh.py
D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_ir.py
D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_motor.py
D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_rc.py
D:\Russ\0000\python00\python3\_projects\SmartTerminal\Ver4\ext_process_tty.py



============ topic  fix  greenhouse, root celler for failures in the recive from arduino ===========

        step one, count fail and ignore for n times then reboot
        step two reboot, but count and do not go too crazy

            have a function in gui therad, to reboot do logging....


=================================================================================



=========================== ddclock =======================

dec 2018
    start adding processing for the led
    try a led_chime
        for now do the same thing for every hour, ... half hour.....
        a slow rise in brightness, dim down after the chime
















