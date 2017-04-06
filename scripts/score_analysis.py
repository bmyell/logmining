#!usr/bin/python2.7
#-*-coding:utf-8-*

import re #Regular Expression

import os

def get_file_in_dir(dir):
    filelist =[]
    filenames=os.listdir(dir)
    for fn in filenames:
        filelist.append(fn)
    fo = open("list.txt",'wb')
    for j in filelist:
        fo.write(str(j))
        fo.write('\n')

def get_infor_in_file_name(rclfile):
    team_expr = "\d{14}-*-vs-*"



if __name__=="__main__":
      dir='/home/rider/Desktop/Q_test/logs'
      get_file_in_dir(dir)





