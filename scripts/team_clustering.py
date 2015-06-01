#!usr/bin/python3.4
#-*-coding:utf-8-*

import sys
import os
sys.path.append("../lib")
import file_manager as fm

if (len(sys.argv) == 3):
    print "Incoming..."
    #Get all match
    #For each match
        #Give a label to t1 and to t2
        #Get kick t1 et t2
        #EMD
        #Add value in distance matrix
    #Print dendogram

else:
    print "Argv error. Please type:"
    print "python team_clustering.py log_path/ save_path/"
