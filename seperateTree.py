# -*- coding: UTF-8 -*-

import os
from os import listdir, getcwd
from os.path import join
import sys
import json
import time
from PIL import Image 

def cutPic(x1, x2, y1, y2, picid, picname):
	box = (x1, y1, x2, y2)
	im = Image.open('snapshots/%s.png'%picid)
	region = im.crop(box)
	region.save('treePics/%s.png'%picname)

def recordTree(node, rootname, i):
	index = node["tag"] + str(time.time())
	node["index"] = index
	children = node["leaves"]
	length = len(children)
	if length == 0:
		return node
	if length == 1:
		recordTree(children[0], rootname, i)
		return node
	name = rootname + "," + index
	with open("trees/%s.json"%name, 'w') as f:
		jsonout = json.dumps(node, indent=4)
		f.write(jsonout)
	x1 = node["left"]
	x2 = node["left"] + node["width"]
	y1 = node["top"]
	y2 = node["top"] + node["height"]
	cutPic(x1, x2, y1, y2, i, name)
	for child in children:
		recordTree(child, rootname, i)

reload(sys)
sys.setdefaultencoding('utf-8')
if not os.path.exists('temp/'):
	os.makedirs('temp/')
if not os.path.exists('trees/'):
	os.makedirs('trees/')
if not os.path.exists('labels/'):
	os.makedirs('labels/')
if not os.path.exists('tmpPic/'):
	os.makedirs('tmpPic/')

start = 1490773350000
i = 1
jtitle = ""
while i <= 1000:
	if os.path.isfile('snapshots/%s.png'%start):
		jsonfile = open('temp/%s.json'%start, 'w')
		tempfile = open('snapshots/%s.json'%start)
		lines = tempfile.readlines()
		for j in range (0, len(lines)):
			if "}," in lines[j] and "]" in lines[j+1]:
				jsonfile.write('    }\n')
			else:
				jsonfile.write(lines[j])
		jsonfile.close()
		jsonfile = open('temp/%s.json'%start)
		try:
			root = json.load(jsonfile)
			jsonfile.close()
			if root["title"] != jtitle:
				print i, root["title"]
				jtitle = root["title"]
				recordTree(root["leaves"][0], root["url"].replace("https://", '').replace("http://", '').replace('/', '_'), start)
				i = i + 1
		except:
			jsonfile.close()
	if start == 1490774117000:
		start = 1499435231000
	else:
		start = start + 1000
	if i > 20:
		break
	if start > 1499481355000:
		break
