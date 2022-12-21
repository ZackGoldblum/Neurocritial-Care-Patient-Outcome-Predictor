# by Ahmet Sacan.
# Modified by Zack Goldblum, Josh Miller, Kevin Ramirez Chavez
# This class contains functions for some cross-platform setup & configuration
# needed in some of my courses.
# See the README.txt file for instructions on making this file available in python.
# imports and Utility functions

import sys,os
from venv import create

class bmes:
    PROJECTNAME=None  #used for projdatadir()
    CUSTOMDATADIR=None  #datadir() will return a default datadir,if you are not happy with that, set this variable.
    CUSTOMDBFILE=None  #dbfile() will return a default file, if you are not happy with that, set this variable.
    CUSTOMTEMPDIR=None
    CUSTOMPATH=None
    db=None #we'll store the database connection here.
    
def mkdirif(dir):
	if not os.path.isdir(dir): os.mkdir(dir, 0o777 )
    
def tempdir():
	if bmes.CUSTOMTEMPDIR: return bmes.CUSTOMTEMPDIR;
	import tempfile
	ret=tempfile.gettempdir().replace("\\","/")+'/bmes';
	mkdirif(ret);
	return ret;