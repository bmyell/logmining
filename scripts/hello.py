#!/usr/bin/python
#-*- coding: UTF-8 -*-
#hello.py
import re
str="20170328215444-Q_learn_4-vs-HELIOS_base_2.rcg"
str2=str.split('-')
time=str2[0]
team_l=str2[1]
team_r=str2[3].strip('.rcg')

team_patten=re.compile('[a-zA-Z]+\_[a-zA-Z]+')
num_patten=re.compile('[0-9]+')

t_l=re.search(team_patten,team_l).group()
t_r=re.search(team_patten,team_r).group()
score_l=re.search(num_patten,team_l).group()
score_r=re.search(num_patten,team_r).group()

