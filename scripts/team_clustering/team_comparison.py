#!usr/bin/python3.4
#-*-coding:utf-8-*

import os
import sys
import numpy as np
import scipy.cluster.hierarchy as hac
from cv2 import *
import matplotlib.pyplot as plt

def get_distribution(path):
    print path
    file = open(path, "r")
    content = file.read()
    file.close()
    content = content.split("\n")
    del content[-1]
    distribution = []
    for k in content:
        distribution.append(k.split(" "))
    for i in range(0, len(distribution)):
        distribution[i] = [float(distribution[i][0]),\
                           float(distribution[i][1]),\
                           float(distribution[i][2])]
    return distribution

def compute_signature(distribution):
    signature = cv.CreateMat(len(distribution), 3, cv.CV_32FC1)
    #Signature is defined as : {(length_kick_1, x_kick_1, y_kick_1), ...,
    #                           (length_kick_n, x_kick_n, y_kick_n)}

    for i in range(0, len(distribution)):
        cv.Set2D(signature, i, 0, distribution[i][0])
        cv.Set2D(signature, i, 1, distribution[i][1])
        cv.Set2D(signature, i, 2, distribution[i][2])

    return signature

if (len(sys.argv) == 2):
    file_list = []
    for root, subFolders, files in os.walk(sys.argv[1] + "distributions/"):
    	for file in files:
    		file_list.append(os.path.join(root, file))
    distance_matrix = np.empty([len(file_list), len(file_list)])
    for i in range(0, len(file_list)):
        j = 0
        while j <= i:
            distribution_team1 = get_distribution(file_list[i])
            distribution_team2 = get_distribution(file_list[j])
            print i
            print j
            print len(distribution_team1)
            print len(distribution_team2)
            signature_team1 = compute_signature(distribution_team1)
            signature_team2 = compute_signature(distribution_team2)
            emd = cv.CalcEMD2(signature_team1, signature_team2, cv.CV_DIST_L2)
            print emd
            distance_matrix[i][j] = emd
            distance_matrix[j][i] = emd
            j = j + 1
    print distance_matrix
    link_matrix = hac.linkage(distance_matrix, method='weighted')
    dendrogram = hac.dendrogram(link_matrix)
    plt.savefig(sys.argv[1] + "/dendro_full.png")
    l = dendrogram['leaves']
    dendrogram = hac.dendrogram(link_matrix, p=100,\
                                truncate_mode='level', show_contracted=True)
    plt.savefig(sys.argv[1] + "/dendro.png", dpi=300)
    link = link_matrix.tolist()
    fl = open(sys.argv[1] + "/link.txt", "w")
    for elt in link:
        fl.write(str(int(elt[0])) + " " + str(int(elt[1])) +\
                " " + str(elt[2]) + " " + str(int(elt[3])) + "\n")
    fl.close()
