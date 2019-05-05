#Grupo 30, Antonio Santos 87632, Diogo Sa 87652
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:51:49 2018

@author: mlopes
"""

import numpy as np
np.set_printoptions(precision=4, suppress=True)

import itertools

class Node():
	def __init__(self, prob, parents = []):
		self.prob = prob
		self.parents = parents
		pass

	def computeProb(self, evid):
		pos = []
		for i in self.parents:
			pos.append(evid[i])

		x = self.prob
		for i in pos:
			x = x[i]

		if len(self.parents) == 0:
			x = self.prob[0]

		return [1-x,x]


class BN():
	def __init__(self, gra, prob):
		self.grap = gra
		self.prob = prob
		self.poss = []
		self.ev = []

	def computeJointProb(self, evid):
		x = 1
		for i in range(0,len(self.prob)):
			if evid[i] == 1:
				x = x * self.prob[i].computeProb(evid)[1]
			else:
				x = x * self.prob[i].computeProb(evid)[0]
		return x
	
	
	def computePostProb(self, evid):
			d = 0
			for i in range(0,len(evid)): 
				if evid[i] == []:
					d = d + 1
			
			self.poss = list(itertools.product([0,1], repeat=d))    
			cpPoss = self.poss.copy()	
	
			for i in range(0,len(evid)):
				if evid[i] == -1:
					evid = list(evid)
					evid[i] = 1
					self.ev = evid.copy()  # Hacks
					w = self.CalculaCenas(evid)
	
					self.poss = cpPoss  # recuperar possibilidades para []
					evid = self.ev  # recuperar estado inicial
					evid[i] = 0
					self.ev = evid.copy()  # Hacks
					z = self.CalculaCenas(evid)
					return w / (w + z)
			

	def CalculaCenas(self, evid):
			x = 0
			p = 0
			while len(self.poss) != 0:
				for j in range(0,len(evid)):
					if evid[j] == []:
						evid[j] = self.poss[0][x]
						x += 1
				
				p += self.computeJointProb(evid)
				evid = self.ev.copy()
				x=0
				del self.poss[0]

			return p
