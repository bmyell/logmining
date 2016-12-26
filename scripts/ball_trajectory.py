#!usr/bin/python3.4
#-*-coding:utf-8-*

import sys
import os
sys.path.append("../lib")
import file_manager as fm
import data_visualizer as dv

if (len(sys.argv) == 3) or (len(sys.argv) == 4):
    #If user gave rcg and rcl
    if len(sys.argv) == 4:
        print sys.argv[1][:-4]
        if sys.argv[1][len(sys.argv[1]) -4:] == ".rcg":
            rcg = fm.read_file(sys.argv[1])
            rcl = fm.read_file(sys.argv[2])
        else:
            rcg = fm.read_file(sys.argv[2])
            rcl = fm.read_file(sys.argv[1])
        path = sys.argv[3]
    #If user gave a directory
    else:
        file_list = fm.walking_tree(sys.argv[1])
        for file in file_list:
            rcg = fm.read_file(file[0])
            rcl = fm.read_file(file[1])
            path = sys.argv[2]

    teams = fm.find_teams(rcg)
    ball_data = fm.get_ball_data(rcg)
    if os.path.isdir(path) is False:
    	os.mkdir(path)
    dv.plot_ball_pos(ball_data, teams, path)
else:
    print "Argv error. Please type:"
    print "python ball_trajectory.py log_path save_path/"
    print "or python ball_trajectory.py log.rcg log.rcl save_path/"
