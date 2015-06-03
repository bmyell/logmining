#!usr/bin/python3.4
#-*-coding:utf-8-*

import sys
sys.path.append("../lib")
import file_manager as fm
import data_visualizer as dv

if (len(sys.argv) == 2):
    file_list = fm.walking_tree(sys.argv[1])
    total_1 = 0
    total_2 = 0
    total_s_1 = 0
    total_s_2 = 0
    for file in file_list:
        rcg = fm.read_file(file[0])
        rcl = fm.read_file(file[1])

        teams = fm.find_teams(rcg)
        ball_data = fm.get_ball_data(rcg)
        corner_kicks = fm.get_corner_kicks(rcl, ball_data, teams)
        kick_data = fm.get_kick_data(rcl, ball_data)
        corner_kicks_chains = fm.get_corner_kicks_chains(kick_data, corner_kicks)
        success_corner_kicks = fm.get_success_corner_kicks(corner_kicks_chains)
        dv.plot_kick_chains(success_corner_kicks, teams, "")

        team1_corner_kicks = []
        team2_corner_kicks = []
        team1_success_corner_kicks = []
        team2_success_corner_kicks = []
        for ck in corner_kicks:
            if ck[1] == teams[0]:
                team1_corner_kicks.append(ck)
            else:
                team2_corner_kicks.append(ck)
        for sck in success_corner_kicks:
            if sck[0][1] == teams[0]:
                team1_success_corner_kicks.append(sck)
            else:
                team2_success_corner_kicks.append(sck)
        del corner_kicks
        del success_corner_kicks

        print str(file[0]) + ": "
        print "team: " + teams[0] + " " + str(len(team1_corner_kicks)) +\
              " corner kicks " + str(len(team1_success_corner_kicks)) +\
              " success"
        print "team: " + teams[1] + " " + str(len(team2_corner_kicks)) +\
              " corner kicks " + str(len(team2_success_corner_kicks)) +\
              " success"

        total_1 = total_1 + len(team1_corner_kicks)
        total_2 = total_2 + len(team2_corner_kicks)
        total_s_1 = total_s_1 + len(team1_success_corner_kicks)
        total_s_2 = total_s_2 + len(team2_success_corner_kicks)

    print teams[0] + ": " + str(total_1) + " corner kicks " + "(" +\
          str(total_s_1) + " success) "  "within " +\
          str(len(file_list)) + " matches."
    print teams[1] + ": " + str(total_2) + " corner kicks " + "(" +\
          str(total_s_2) + " success) "  "within " +\
          str(len(file_list)) + " matches."
else:
    print "Argv error. Please type:"
    print "python count_corner_kick.py log_path"
