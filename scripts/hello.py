#!/usr/bin/python
#-*- coding: UTF-8 -*-
#hello.py
import re
str="20170328215444-Q_learn_4-vs-HELIOS_base_2.rcg"
patten=re.compile('\d{14}')
match=re.match(patten,str)
print(match.group())