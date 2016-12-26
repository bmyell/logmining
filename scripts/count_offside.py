#!usr/bin/python3.4
#-*-coding:utf-8-*

import sys
sys.path.append("../lib")
import file_manager as fm

if (len(sys.argv) == 2):
    file_list = fm.walking_tree(sys.argv[1])
    total_1 = 0
    total_2 = 0
    for file in file_list:
        rcg = fm.read_file(file[0])
        rcl = fm.read_file(file[1])

        teams = fm.find_teams(rcg)
        ball_data = fm.get_ball_data(rcg)
        offsides = fm.get_offsides(rcl, ball_data, teams)
        team1_offsides = []
        team2_offsides = []
        for o in offsides:
            if o[1] == teams[0]:
                team1_offsides.append(o)
            else:
                team2_offsides.append(o)
        del offsides
        print str(file[0]) + ": "
        print "team: " + teams[0] + str(len(team1_offsides)) +\
              " offsides"
        print "team: " + teams[1] + str(len(team2_offsides)) +\
              " offsides"

        total_1 = total_1 + len(team1_offsides)
        total_2 = total_2 + len(team2_offsides)

        for ck in team1_offsides:
            print ck
        for ck in team2_offsides:
            print ck
    print teams[0] + ": " + str(total_1) + " offsides within " +\
          str(len(file_list)) + " matches."
    print teams[1] + ": " + str(total_2) + " offsides within " +\
          str(len(file_list)) + " matches."
else:
    print "Argv error. Please type:"
    print "python count_corner_kick.py log_path"
