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

==================== DeerMe History/ToDo ==================================

!! check out auto start and detect, should work as in ddc 
!! more messages when ticktime is changed






==================== DDC History/ToDo ==================================


==================== General History/ToDo ==================================
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




============================= deer me ============================



trying to use status None for a fast test, but not working out
go back to strings, and if not fast enough do an emumeration, which is probably an over optinmizaition
see ext_process_dm tick timer  .....

How do i know when a tick time is done and time to move on ?

some status    init   --- not yet run
               run    --- running
               done   --- done and closed, may mean to move on or not



Need a way to schedule tick timers and the audo outs so for now use SetNextScare   set_next_scare



------------------------- some flash sequences


...... strobe

1 tenth on, 1 tenth off, 1 tenth on  .... off for 10 seconds


........ more strobes




......... out of sinc blink


lihgt A  1 sec on 1 sec off, one sec on 1 sec off....                              1000  0 1000 0
lihgt B  1 sec on 1.1 sec off, one sec on 1.1 sec off....   all for 20 seconds     1000  0 1100 0

then in python

       a_tick_timer.ix_cycle_max           = 1     # close out when reach this

        a_tick_timer.ix_tick_max           = 20    # roll over tick actions

        # set next as necessary -- add as necessary -- access as properties
        a_tick_timer.ix_tick_act_1         = -1
        a_tick_timer.ix_tick_act_2         = -1

        a_tick_timer.tick_strs_0            = ["i0", "l100 200 130 400", "i1", "l105 200 130 400", "s1" ]

























