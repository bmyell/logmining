#!usr/bin/python2.7
#-*-coding:utf-8-*
import webbrowser
import re #Regular Expression
import sys
import os
def read_file(path):
    """Reads the content of the specified file"""
    file = open(path, "r")
    content = file.read()
    file.close()
    content = content.split("\n")
    return content

def find_teams(rcg):
    """Determines the name of both teams"""

    team_expr = "^\(team[ ][1]*[ ][a-zA-Z0-9]*([-]*[_]*[a-zA-Z0-9]*)*" + \
                "[ ][a-zA-Z0-9]*([-]*[_]*[a-zA-Z0-9]*)*"

    for elt in rcg:
        if re.search(team_expr, elt) is not None:
            tmp = re.search(team_expr, elt).group()
            tmp = tmp.split(" ")
            return (tmp[2], tmp[3]) #team_left, team_right

    return ("not found", "not found")

def get_file_in_dir(dir):
    filelist =[]
    filenames=os.listdir(dir)
    for fn in filenames:
        filelist.append(fn)
    fo = open("list.txt",'wb')
    for j in filelist:
        fo.write(str(j))
        fo.write('\n')




if __name__=="__main__":
      dir='/home/rider/Desktop/Q_test/logs'
      get_file_in_dir(dir)





