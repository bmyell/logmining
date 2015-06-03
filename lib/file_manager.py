#!usr/bin/python3.4
#-*-coding:utf-8-*

import re #Regular Expression
import sys
import os

"""Module which reads log files and extracts data"""

def walking_tree(path):
	"""Walks the given path and returns a list of all logs' path"""

	file_list = []

	for root, subFolders, files in os.walk(path):
		for file in files:
			if file[len(file) - 4:] == ".rcg":
				rcl = os.path.join(root, file[: -3] + "rcl")
				file_list.append((os.path.join(root, file), rcl))
	return file_list

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

def get_ball_data(rcg):
	"""Returns ball data for each cycle"""

	ball_data_expr = "[0-9]*[ ]\(\(b\)([ ][-]?[0-9]*(\.[0-9]*)?){4}\)"
	ball_data = list()

	for elt in rcg:
		ball = list()
		line = elt.split(" ")
		if re.search(ball_data_expr, elt) is not None:
			tmp = re.search(ball_data_expr, elt).group()
			tmp = tmp.split(" ")
			ball.append(int(tmp[0]))
			ball.append(float(tmp[2]))
			ball.append(float(tmp[3]))
			ball.append(float(tmp[4]))
			ball.append(float(tmp[5][:-1]))
			ball_data.append(ball) #cycle, x, y, ?, ?

	return ball_data

def get_kick_data(rcl, ball_data):
	"""Returns kick actions for each cycle"""

	kick_data_expr = "Recv [a-zA-Z0-9]+([-_]*[a-zA-Z0-9]*)*:" + \
	" \(kick([ ]?[-]?[0-9][.]?)*"
	cycle_expr = "^[0-9]*"
	kick_data = list()

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 2 and line[2] == "(kick":
			tmp_cycle = re.search(cycle_expr, elt).group()
			tmp = re.search(kick_data_expr, elt).group()
			tmp = tmp.split(" ")
			agent = tmp[1].split("_")
			kick_data.append([int(tmp_cycle), agent[0], int(agent[1][:-1]),\
			float(tmp[3]), float(tmp[4])]) #cycle, team, n°player, ?, ?
	for elt in kick_data:
		for b_p in ball_data:
			if elt[0] == b_p[0]:
				elt.insert(3, b_p[1])
				elt.insert(4, b_p[2]) #cycle, team, n°player, x, y, ?, ?

	return kick_data

def get_passes(kick_data):
	"""Returns passes from kick data"""

	last_kick = kick_data[0]
	passes = list()

	for elt in kick_data[1:len(kick_data)]:
		if elt[1] == last_kick[1] and elt[2] != last_kick[2]:
			passes.append(last_kick)
		last_kick = elt

	return passes

def get_dribbles(kick_data):
	"""Returns dribbles from kick data"""

	last_kick = kick_data[0]
	dribbles = list()

	for elt in kick_data[1:len(kick_data)]:
		if elt[1] == last_kick[1] and elt[2] == last_kick[2]:
			dribbles.append(last_kick)
		last_kick = elt

	return dribbles

def get_kick_chains(kick_data):
	"""Returns kick chains from kick data"""

	kick_chains = list()
	last_kick = kick_data[0]
	chain = list()
	chain.append(kick_data[0])

	for elt in kick_data:
		if elt[1] == last_kick[1]:
			kick = elt
			if elt[2] == last_kick[2]:
				kick.insert(5, 0) #insert "it's a dribble"
			else:
				kick.insert(5, 1) #insert "it's a pass"
			chain.append(elt)
		else:
			if len(chain) > 1:
				kick_chains.append(chain)
			chain = list()
		last_kick = elt

	return kick_chains

def get_success_kick_chains(kick_chains):
	"""Returns success kick chains from kick data"""

	success_kick_chains = list()

	for elt in kick_chains:
		#If the last kick of current chain is in penalty area
		if (elt[len(elt) - 1][3] >= 36 and elt[len(elt) - 1][3] <= 52.5) or \
		(elt[len(elt) - 1][3] <= -36 and elt[len(elt) - 1][3] >= -52.5):
			if elt[len(elt) - 1][4] >= -20 and elt[len(elt) - 1][4] <= 20:
				success_kick_chains.append(elt)

	return success_kick_chains

def get_corner_kicks_chains(kick_data, corner_kick):
	corner_kicks_chains = []
	tmp = []
	i = 0

	for ck in corner_kick:
		while i < len(kick_data):
			if kick_data[i][0] >= ck[0]:
				if kick_data[i][1] == ck[1]:
					for j in range(i, len(kick_data)):
						if kick_data[j][1] != ck[1]:
							break
						else:
							tmp.append(kick_data[j])
					corner_kicks_chains.append(tmp)
					tmp = []
					break
			i = i + 1

	return corner_kicks_chains

def get_success_corner_kicks(corner_kicks_chains):
	"""Returns success kick chains from kick data"""

	success_corner_kicks = list()

	for elt in corner_kicks_chains:
		if elt[0][1] == "HELIOS2014":
			print elt
		#If the last kick of current chain is in penalty area
		if (elt[len(elt) - 1][3] >= 36 and elt[len(elt) - 1][3] <= 52.5) or \
		(elt[len(elt) - 1][3] <= -36 and elt[len(elt) - 1][3] >= -52.5):
			if elt[len(elt) - 1][4] >= -20 and elt[len(elt) - 1][4] <= 20:
				success_corner_kicks.append(elt)

	return success_corner_kicks

def get_faults(rcl, ball_data, teams):
	"""Returns faults"""

	fault_expr = "\(referee foul_charge_[r|l]"
	cycle_expr = "^[0-9]*"
	faults = list()
	flag = False

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "foul_charge_":
			tmp = re.search(fault_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_fault = tmp[1].split("_")
			if(team_fault[2] == "r"):
				team_fault = teams[1]
			else:
				team_fault = teams[0]
			faults.append([int(cycle), team_fault])
	for elt in faults:
		for b in ball_data:
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the fault
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_fault, x, y
		flag = False

	return faults

def get_offsides(rcl, ball_data, teams):
	"""Returns offsides"""

	offside_expr = "\(referee offside_[r|l]"
	cycle_expr = "^[0-9]*"
	offsides = list()
	flag = False

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "offside_":
			tmp = re.search(offside_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_offside = tmp[1].split("_")
			if(team_offside[1] == "r"):
				team_offside = teams[1]
			else:
				team_offside = teams[0]
			offsides.append([int(cycle), team_offside])
	for elt in offsides:
		for b in ball_data:
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the offside
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_offside, x, y
		flag = False

	return offsides

def get_corner_kicks(rcl, ball_data, teams):
	"""Returns corners"""

	corner_expr = "\(referee corner_kick_[r|l]"
	cycle_expr = "^[0-9]*"
	corner_kicks = list()
	flag = False

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "corner_kick_":
			tmp = re.search(corner_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_corner = tmp[1].split("_")
			if team_corner[2] == "r":
				team_corner = teams[1]
			else:
				team_corner = teams[0]
			corner_kicks.append([int(cycle), team_corner])
	for elt in corner_kicks:
		for b in ball_data:
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the corner kick
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_corner, x, y
		flag = False

	return corner_kicks

def get_kick_in(rcl, ball_data, teams):
	"""Returns kick in"""

	kick_in_expr = "\(referee kick_in_[r|l]"
	cycle_expr = "^[0-9]*"
	kick_in = list()
	flag = False

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "kick_in_":
			tmp = re.search(kick_in_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_kick_in = tmp[1].split("_")
			if(team_kick_in[2] == "r"):
				team_kick_in = teams[1]
			else:
				team_kick_in = teams[0]
			kick_in.append([int(cycle), team_kick_in])
	for elt in kick_in:
		for b in ball_data:
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the kick in
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_kick_in, x, y
		flag = False

	return kick_in

def get_goal_kicks(rcl, ball_data, teams):
	"""Returns goal kicks"""

	goal_kick_expr = "\(referee goal_kick_[r|l]"
	cycle_expr = "^[0-9]*"
	goal_kicks = list()
	flag = False

	for elt in rcl:
		line = elt.split(" ")
		if len(line) > 1 and line[1][:-2] == "goal_kick_":
			tmp = re.search(goal_kick_expr, elt).group()
			tmp = tmp.split(" ")
			cycle = re.search(cycle_expr, elt).group()
			team_goal_kick = tmp[1].split("_")
			if(team_goal_kick[2] == "r"):
				team_goal_kick = teams[1]
			else:
				team_goal_kick = teams[0]
			goal_kicks.append([int(cycle), team_goal_kick])
	for elt in goal_kicks:
		for b in ball_data:
			if b[0] == elt[0] and flag == False:
				#It's not the true position of the goal kick
				#the true one is in the next line
				flag = True
			elif flag == True and len(elt) < 4:
				elt.append(b[1])
				elt.append(b[2]) #cycle, team_goal_kick, x, y
		flag = False

	return goal_kicks

def ball_possession(kick_chains, teams):
	"""Returns the percentage of ball possession for both teams"""

	t_left = 0
	t_right = 0
	t_total = 0

	for elt in kick_chains:
		if elt[0][1] == teams[0]:
			t_left += elt[len(elt) - 1][0] - elt[0][0]
		else:
			t_right += elt[len(elt) - 1][0] - elt[0][0]
	t_total = t_left + t_right
	t_left = float(t_left * 100) / float(t_total)
	t_right = float(t_right * 100) / float(t_total)
	tmp = str(t_left) #Rounds the results
	tmp = tmp.split(".")
	if int(tmp[1][0]) >= 5:
		t_left = int(tmp[0]) + 1
	else:
		t_left = int(tmp[0])
	tmp = str(t_right)
	tmp = tmp.split(".")
	if int(tmp[1][0]) >= 5:
		t_right = int(tmp[0]) + 1
	else:
		t_right = int(tmp[0])
	ball_possession = (t_left, t_right)

	return ball_possession
