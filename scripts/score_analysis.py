#!usr/bin/python2.7
#-*-coding:utf-8-*

import re  # Regular Expression
import os
import glob
# need sort


def get_file_in_dir(dir):
    filelist = []
    filenames = os.listdir(dir)
    # filenames = glob.glob(dir)
    for fn in filenames:
        filelist.append(fn)
    if(len(filelist) > 0):
        filelist.sort()
    fo = open("list.txt", 'wb')
    for j in filelist:
        if '.rcl' not in j:  # not surpport re...
            fo.write(str(j))
            fo.write('\n')
    fo.close()


def get_infor_of_on_line(line):
    str2 = line.split('-')
    time = str2[0]
    team_l = str2[1]
    team_r = str2[3].strip('.rcg')

    team_patten = re.compile('[a-zA-Z]+\_[a-zA-Z]+')
    num_patten = re.compile('[0-9]+')
    t_l = re.search(team_patten, team_l).group()
    t_r = re.search(team_patten, team_r).group()
    score_l = re.search(num_patten, team_l).group()
    score_r = re.search(num_patten, team_r).group()
    print(time + " " + t_l + "   " + t_r + "   " + score_l + "   " + score_r)


def handle_text():
    f = open("list.txt", 'r')
    line = f.readline()
    while line:
        get_infor_of_on_line(line)
        line = f.readline()
    f.close()


if __name__ == "__main__":
    dir = '/home/rider/Desktop/Q_test/logs'
    get_file_in_dir(dir)  # works
    handle_text()  # works
