# Traceable delivery
*This readme is during the development of the project used as a general project documentation*   
Often as a developer you are faced with the task of keeping track of specific build artifacts. This can be generated
documentation, compiled code, log-files, and other files that might be impossible to reproduce exactly. To be able to
deliver and keep rack of this kind of files this project strive to create a simple way to package these files together 
with information and hashes. This will allow each delivery to be checked for consistency and also allow it to be tracked
to its source (if for example git commits, build machine etc. is present in the information supplied).

## General idea
- The program should be controlled by a config file, but have the possibility to overrule this config by direct insertion
of parameters.
  
- The program should be an installable python package (setup.py and all that) with a CLI interface (click is a good
  candidate)
  
- The program shall be developed using a TDD approach.

- The program shall implement an architecture of a simple CLI layer calling internal API functions. This to ease the
testing using callable functions and to make all API functions usable from within the code (something not always)
  possible with CLI functions)