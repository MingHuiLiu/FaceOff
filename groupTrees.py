# -*- coding: UTF-8 -*-

import os
from os import listdir, getcwd
from os.path import join
import sys
import json
import time
import zss
import shutil

if not os.path.exists('results/'):
	os.makedirs('results/')

length = 100
distance = [[0 for j in range(0, length)] for i in range(0, length)]
recall = open('treematrix.csv').readlines()
tmp = recall[0].split(' ')
ii = int(tmp[0])
jj = int(tmp[1])
relen = len(recall)
for i in range(1, relen):
	tmp = recall[i].split(',')
	for j in range(0, len(tmp)):
		distance[i-1][j] = int(tmp[j])

group = [[] for i in range (0, length)]
center = []
centerdis = []
group[0].append(0)
center.append(0)
centerdis.append(0)
groupcnt = 1

def updateCenter(index):
	mindis = 0xFFFFFF
	centerindex = 0
	for i in group[index]:
		dis = 0
		for j in group[index]:
			dis = dis + distance[i][j]
		if dis < mindis:
			mindis = dis
			centerindex = i
	center[index] = centerindex
	centerdis[index] = mindis


for i in range(1, length):
	mindis = 0xFFFFFF
	index = 0
	for j in range(0, groupcnt):
		centernode = center[j]
		if distance[i][centernode] < mindis:
			mindis = distance[i][centernode]
			index = j
	if mindis <= 10:
		group[index].append(i)
		updateCenter(index)
	else:
		group[groupcnt].append(i)
		center.append(i)
		centerdis.append(0)
		groupcnt = groupcnt + 1

nameset = open("nameset.txt").readlines()
for i in range(0, groupcnt):
	num = len(group[i])
	with open("results/group_%s.txt"%i, 'w') as f:
		for j in range(0, num):
			f.write(nameset[group[i][j]])
	dirpath = 'results/%s'%str(i)
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)
	for j in range(0, num):
		name = nameset[group[i][j]].replace('\n', '').replace('.json', '')
		shutil.copyfile('treePics/%s.png'%name, dirpath+'/%s.png'%name)

with open("results/centers.txt", 'w') as f:
	for i in range(0, groupcnt):
		name = nameset[center[i]].replace('\n', '').replace('.json', '')
		f.write(name + ' ' + str(centerdis[i]) + '\n')


