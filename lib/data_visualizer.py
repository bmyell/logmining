#!usr/bin/python3.4
#-*-coding:utf-8-*

import matplotlib.pyplot as plt
import numpy as np
from math import *

#Global variable which represents the color of the players
player_color = [
    "#010208",
    "#011E61",
    "#011E61",
    "#006E13",
    "#909000",
    "#906000",
    "#903D00",
    "#8E0007",
    "#700046",
    "#3A0161",
    "#4A7600"
]

def init_field(teams):
	"""Sets up the field on figure"""

	#Sets up limits
	plt.xlim(-60, 60)
	plt.ylim(-40, 40)

	#Draws field
	plt.plot([-52.5, 52.5], [-34, -34], color = "g", linestyle = "-", linewidth = 0.5)
	plt.plot([-52.5, 52.5], [34, 34], color = "g", linestyle = "-", linewidth = 0.5)
	plt.plot([-52.5, -52.5], [-34, 34], color = "g", linestyle = "-", linewidth = 0.5)
	plt.plot([52.5, 52.5], [-34, 34], color = "g", linestyle = "-", linewidth = 0.5)

	#Draws penalty area
	plt.plot([36, 52.5], [-20, -20], color = "k", linestyle = "-", linewidth = 0.5)
	plt.plot([36, 52.5], [20, 20], color = "k", linestyle = "-", linewidth = 0.5)
	plt.plot([36, 36], [-20, 20], color = "k", linestyle = "-", linewidth = 0.5)
	plt.plot([-36, -52.5], [-20, -20], color = "k", linestyle = "-", linewidth = 0.5)
	plt.plot([-36, -52.5], [20, 20], color = "k", linestyle = "-", linewidth = 0.5)
	plt.plot([-36, -36], [-20, 20], color = "k", linestyle = "-", linewidth = 0.5)

	#Writes teams' name
	plt.text(-58, 0, teams[0], color = "y", rotation = "vertical")
	plt.text(56, 0, teams[1], color = "r", rotation = "vertical")

def color_legend():
    """Add color's legend"""

    plt.text(-50 + (2 * 1), 36, '1', color = player_color[0])
    plt.text(-50 + (2 * 2), 36, '2', color = player_color[1])
    plt.text(-50 + (2 * 3), 36, '3', color = player_color[2])
    plt.text(-50 + (2 * 4), 36, '4', color = player_color[3])
    plt.text(-50 + (2 * 5), 36, '5', color = player_color[4])
    plt.text(-50 + (2 * 6), 36, '6', color = player_color[5])
    plt.text(-50 + (2 * 7), 36, '7', color = player_color[6])
    plt.text(-50 + (2 * 8), 36, '8', color = player_color[7])
    plt.text(-50 + (2 * 9), 36, '9', color = player_color[8])
    plt.text(-50 + (2 * 10), 36, '10', color = player_color[9])
    plt.text(-50 + (2 * 12), 36, '11', color = player_color[10])

def plot_ball_pos(ball_data, teams, path):
	"""Plot the given positions"""

	x = list()
	y = list()

	for elt in ball_data:
		x.append(elt[1])
		y.append(-elt[2])
	plt.plot(x, y)
	init_field(teams)
	if path != "":
		plt.savefig(path + "plot_position.png")
	plt.show()

def scatter_kick_pos(kick_data, teams, ball_possession, path):
	"""Scatter the given positions"""

	for elt in kick_data:
		if elt[1] == teams[0]:
			c = "y"
		else:
			c = "r"
		plt.scatter(elt[3], -elt[4], color = c)
	init_field(teams)
	plt.text(-40, -37, teams[0] + " : " + str(ball_possession[0]) + "%")
	plt.text(20, -37, teams[1] + " : " + str(ball_possession[1]) + "%")
	if path != "":
		plt.savefig("save/" + path + "scatter_position.png")
	plt.show()

def plot_kick_chains(kick_chains, teams, path):
    """Plot the given kick chains"""

    i = 0
    j = 0

    print kick_chains
    for elt in kick_chains:
        print elt[0]
        if elt[0][1] == teams[0]:
            for kc in range(1, len(elt)):
                x_origin = elt[kc - 1][3]
                y_origin = -elt[kc - 1][4]
                x_destination = elt[kc][3]
                y_destination = -elt[kc][4]
                if elt[kc - 1][5] == 0:
                    m = "^"
                else:
                    m = "o"
                plt.plot(x_origin, y_origin, x_destination, y_destination, marker = m, color = player_color[elt[kc - 1][2] - 1])
                plt.plot([x_origin, x_destination], [y_origin, y_destination], linestyle = '-', linewidth = 1, color = player_color[elt[kc - 1][2] - 1])
            init_field(teams)
            color_legend()
            plt.text(elt[0][3], -elt[0][4], elt[0][0])
            plt.text(-10, 36, teams[0])
            #if path != "":
                #plt.savefig("save/" + path + teams[0] + "_kick_actions_" + str(i) + ".png", dpi = 200)

            i = i + 1
            plt.show()
            plt.clf()
        else:
            for kc in range(1, len(elt)):
                x_origin = elt[kc - 1][3]
                y_origin = -elt[kc - 1][4]
                x_destination = elt[kc][3]
                y_destination = -elt[kc][4]
                if elt[kc - 1][5] == 0:
                    m = "^"
                else:
                    m = "o"
                plt.plot(x_origin, y_origin, x_destination, y_destination, marker = m, color = player_color[elt[kc - 1][2] - 1])
                plt.plot([x_origin, x_destination], [y_origin, y_destination], linestyle = '-', linewidth = 1, color = player_color[elt[kc - 1][2] - 1])
            init_field(teams)
            color_legend()
            plt.text(elt[0][3], -elt[0][4], elt[0][0])
            plt.text(-10, 36, teams[1])
            #if path != "":
                #plt.savefig("save/" + path + teams[1] + "_kick_actions_" + str(j) + ".png", dpi = 200)

            j = j + 1
            plt.show()
            plt.clf()

def plot_faults(fault_position, teams, path, name):
	"""Plots the given faults"""

	for elt in fault_position:
		if elt[1] == teams[0]:
			c = "y"
		else:
			c = "r"
		plt.scatter(elt[2], -elt[3], color = c)
		plt.text(elt[2] + 1, -elt[3] + 1, elt[0])
	init_field(teams)
	if path != "":
		plt.savefig("save/" + path + name + ".png")
	plt.show()
