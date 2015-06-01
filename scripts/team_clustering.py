#!usr/bin/python3.4
#-*-coding:utf-8-*

import sys
import os
sys.path.append("../lib")
import file_manager as fm

if (len(sys.argv) == 3):
    print "Incoming..."
else:
    print "Argv error. Please type:"
    print "python ball_trajectory.py log_path save_path/"
    print "or python ball_trajectory.py log.rcg log.rcl save_path/"
