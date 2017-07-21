# -*- coding: UTF-8 -*-

import os
from os import listdir, getcwd
from os.path import join
import sys
import json
import time
import zss
import shutil
import multiprocessing

translator = {"p": "text", "span": "text", "li": "text", "img": "image", "ul": "list", "ol": "list", "table": "list", "em": "text", "a": "link", "div": "layout"}

def translate(k):
	k = k.lower()
	if k in translator:
		return translator[k]
	return 'unk'

try:
	from editdist import distance as strdist
except ImportError:
	def strdist(a, b):
		if a == b:
			return 0
		else:
			return 1

def weird_dist(A, B):
	return strdist(A, B)

class WeirdNode(object):
	def __init__(self, label):
		self.my_label = label
		self.my_children = list()
		self.hashcode = 0
		self.node_cnt = 1

	@staticmethod
	def get_children(node):
		return node.my_children

	@staticmethod
	def get_label(node):
		return node.my_label

	def addchild(self, node, before=False):
		if before:
			self.my_children.insert(0, node)
		else:
			self.my_children.append(node)
		return self

def buildTree(node):
	Node = WeirdNode(translate(node["tag"]))
	children = node["leaves"]
	hash_set = {}
	for child in children:
		node = buildTree(child)
		if node.hashcode not in hash_set:
			Node.addchild(buildTree(child))
			hash_set[node.hashcode] = True
	Node.my_children.sort(key=lambda x: x.hashcode)
	hash_str = Node.my_label
	for child in Node.my_children:
		hash_str += child.my_label
		Node.node_cnt += child.node_cnt
	Node.hashcode = hash(hash_str)
	return Node


reload(sys)
sys.setdefaultencoding('utf-8')
if not os.path.exists('temp/'):
	os.makedirs('temp/')
if not os.path.exists('trees/'):
	os.makedirs('trees/')

i = 1
nodeset = []
nameset = []
for groupnum in [1, 4, 13]:
	hashcodeset = {}
	for parent,dirnames,filenames in os.walk('labels/%s'%str(groupnum)):
		for filename in filenames:
			if filename.find("png") > 0:
				filename = filename.replace("png", "json")
				try:
					shutil.copyfile('trees/%s'%filename, 'labels/%s/%s'%(str(groupnum),filename))
					jsonfile = open('trees/%s'%filename)
					root = json.load(jsonfile)
					jsonfile.close()
					print i, filename
					node = buildTree(root)
					if node.hashcode not in hashcodeset:
						nodeset.append(node)
						hashcodeset[node.hashcode] = 1
					else:
						hashcodeset[node.hashcode] += 1
					nameset.append(filename)
					i = i + 1
					jsonfile.close()
				except Exception as e:
					print(e)
					continue
				# jsonfile.close()
			# if i > 100:
			# 	break
	with open("hashcodeset_%s.txt"%str(groupnum), 'w') as fout:
		for hashcode in hashcodeset:
			fout.write(str(hashcode) + ',' + str(hashcodeset[hashcode]) + '\n')
		print len(hashcodeset)
# exit()

# with open("nameset1.txt", 'w') as fout:
# 	for name in nameset:
# 		fout.write(name + '\n')

length = len(nodeset)
print length
distance = [[0 for i in range(0, length)] for i in range(0, length)]
for i in range(0, length):
	for j in range(0, i):
		print 'i = ', i, ', j = ', j
		distance[i][j] = zss.simple_distance(nodeset[i], nodeset[j], WeirdNode.get_children, WeirdNode.get_label, weird_dist)
		distance[i][j] = float(distance[i][j]) / (nodeset[i].node_cnt + nodeset[j].node_cnt)
		distance[j][i] = distance[i][j]


with open('matrix.csv', 'w') as fout:
	# fout.write(str(i) + ' ' + str(j) + '\n')
	for k in range(0, length):
		fout.write(str(distance[k][0]))
		for l in range(1, length):
			fout.write(',' + str(distance[k][l]))
		fout.write('\n')


