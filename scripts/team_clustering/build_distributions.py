#!usr/bin/python3.4
#-*-coding:utf-8-*

import sys
import os
sys.path.append("../../lib")
import file_manager as fm
import math

def distance(a, b):
    distance = math.sqrt(\
                math.pow((b[3] - a[3]), 2) + \
                math.pow((b[4] - a[4]), 2))

    return distance

if (len(sys.argv) == 3):
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
        os.makedirs(sys.argv[2] + "distributions/")
    files_path = fm.walking_tree(sys.argv[1])
    for path in files_path:
        #Getting kick data for each match
        rcg = fm.read_file(path[0])
        rcl = fm.read_file(path[1])
        teams = fm.find_teams(rcg)
        team1 = teams[0] + "_VS_" + teams[1]
        team2 = teams[1] + "_VS_" + teams[0]
        ball_data = fm.get_ball_data(rcg)
        kicks = fm.get_kick_data(rcl, ball_data)
        #Building distribution of team1
        kick_team1 = []
        for k in kicks:
            if k[1] == teams[0]:
                kick_team1.append(k)
        distribution_team1 = []
        i = 1
        while i < len(kick_team1):
            d = distance(kick_team1[i - 1], kick_team1[i])
            distribution_team1.append(str(d) + " " + \
                                      str(kick_team1[i][3]) + " " + \
                                      str(kick_team1[i][4]))
            i = i + 1
        #Saving distribution into a file corresponding to the team
        save_file = open(sys.argv[2] + "distributions/" + team1, "a")
        for d in distribution_team1:
            save_file.write(d + "\n")
        save_file.close()
        #Building distribution of team2
        kick_team2 = []
        for k in kicks:
            if k[1] == teams[1]:
                kick_team2.append(k)
        distribution_team2 = []
        i = 1
        while i < len(kick_team2):
            d = distance(kick_team2[i - 1], kick_team2[i])
            distribution_team2.append(str(d) + " " + \
                                      str(kick_team2[i][3]) + " " + \
                                      str(kick_team2[i][4]))
            i = i + 1
        #Saving distribution into a file corresponding to the team
        save_file = open(sys.argv[2] + "distributions/" + team2, "a")
        for d in distribution_team2:
            save_file.write(d + "\n")
        save_file.close()
else:
    print "Argv error. Please type:"
    print "python team_clustering.py log_path/ save_path/"
