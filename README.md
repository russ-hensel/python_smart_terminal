# python_smart_terminal
What:
    This is a line oriented rs232 terminal developed for interaction with micro controllers like the arduino.  
    It is highly configurable and may be quite easily extended.
    For much more documentations and info see the wiki at http://www.opencircuits.com/Python_Smart_Terminal
    Feel free to use and refer to the wiki here.
  
 Modifications for you to make:
  
     Much of the GUI of the program may be customized through a large number of parameters in the configuration file parameters.py.
     For example:
  	    The number of "send" areas, a send button with associate ( and often defaulted ) text.
  
    Extensions I have made:
  	These extensions, which are activated by the parameter file typically:
	    *Extend the GUI   
	    *Add a second thread which automatically runs some micro-controller peripheral (typically also running some
         specialized program ).
        *Extensions ( as modules ) include ( with the arduino code coming later or on request ):
            * Water well monitor ( pre alpha )
            * Greenhouse monitor ( in production for over a year )
            * Driver for an "Art Clock"
            * Servo motor tester 
            * Infrared timing and analysis program
        

Status: 
  Seems to be working well, actively working on parts of it for my dyslecic clock.
  as of Sept 2018 major revisions, contact me if you would like an update.
  Intended for those with some Python experience who can add the files to their Python development environment ( no install features for   this code ). Some dependencies will need to be installed, probably prompted by error messages. Editing of the parameter file 
  should be   easier for those with Python experience. Users should find some useful documentation in the code, this is still a work in     progress. Much code has been lifted from other projects of mine, some artifacts of the other projects remain.  Some unnecessary files
  left over from refactoring, will be removed soon.
      Testing:  I typically work on one extension at a time and do turn ins without much in the way of unit testing, so I may
      have broken something.  If you want some particular feature to work, feel free to message me, and I can probably give
      you a debugged release.
  
Enviroment: 
* Program should run on any OS supporting Python 3.6. ( this is new, to let me use f"" in particular )
* This should include Windows, Mac, Linux, and Raspberry Pi.  
* So far tested on:
** Windows 
** Raspberry Pi ( need retest for python 3.6 coming soon.
** More coming... ( I do not have a mac ) 

 
``` 
	Standard Disclaimer:
		If you have more than a casual interest in this project you should contact me 
		( no_spam_please_666 at comcast.net ) and see if the repository is actually in good shape.  
		I may well have improved software and or documentation.  
		I will try to answer all questions and perhaps even clean up what already exists.	
``` 		

Would You Like to Contribute??
	* Add other communication protocols?
	* Add live graph ( graph data as it is supplied by an attached device )
	
```	
	Note for contributers 
		Fixes would be great.
		Extensions would be great.
		Re write of current code would generally be discouraged... but you are free to create a fork of your own.
		( take a look at readme_rsh.txt for some additional notes on changes... )
	
```
