#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Regist params namespace"""

from optimizer import RegularOptimizer
from utils import Grid

import math

def CalMAD(moving, fixed):
	# NEED TO IMPLEMENTATION
	pass

def CalMADByGrid(moving, fixed, vgrid):
	# NEED TO IMPLEMENTATION
	pass

def CalLinearDeriv(moving, fixed, vgrad, vgrid):
	# NEED TO IMPLEMENTATION
	pass

def CalCubicDeriv(moving, fixed, vgrad, vgrid):
	# NEED TO IMPLEMENTATION
	pass

def CalLinearDerivAndMAD(moving, fixed, vgrad, vgrid):
	# NEED TO IMPLEMENTATION
	pass

def CalCubicDerivAndMAD(moving, fixed, vgrad, vgrid):
	# NEED TO IMPLEMENTATION
	pass

class RegularRegist(object):
	u'''Registration class'''

	def __init__(self, moving, fixed):
		u'''Init regist class with two images'''
		assert(moving.size == fixed.size)

		self.moving = moving
		self.fixed = fixed
		self.movgrad = None
		self.moved = None
		self.vgrid = Grid(moving.size, (4, 4))
		# Initialize optimizer with vgrid and dervgrid
		self.optimizer = RegularOptimizer(self.vgrid, Grid(moving.size, (4, 4)))

	def run(self):
		u'''Run to find vgrid'''
		self.optimizer.vdervgrid = CalLinearDeriv(self.moving, self.fixed, self.movgrad, \
			self.optimizer.vgrid)

		while self.optimizer.forward():
			self.optimizer.vdervgrid = CalLinearDeriv(self.moving, self.fixed, self.movgrad, \
				self.optimizer.vgrid)
			self.optimizer.cost = CalMADByGrid(self.moving, self.fixed, \
				self.optimizer.vgrid)

			# Or can call
			#self.optimizer.vdervgrid, self.optimizer.cost = \
			#	CalLinearDerivAndMAD(self.moving, self.fixed, self.movgrad, \
			#		self.optimizer.vgrid)

		self.vgrid = self.optimizer.vgrid

	def linear_transform(self):
		u'''Linear transform moving image by vgrid'''

		#self.vgrid = self.optimizer.vgridがあるとしてmovingからmovedに
		#self.moved.values[i, j]を取ってくる

		(row, col) = (self.moving.shape[0], self.moving.shape[1])

		#1. 飛び飛びの、移動量がわかっているGridから、間のGridの移動量を補完する
        #求めたいGridが元になるGrid4つに囲まれている時
        for i in range(row):
		    for j in range(col):
		        if (i % 2) == 0 and (j % 2) == 0:
		            self.vgrid[i,j] = (self.optimizer.vgrid[i+1, j+1] + self.optimizer.vgrid[i+1, j-1] \
		                + self.optimizer.vgrid[i-1, j+1] + self.optimizer.vgrid[i-1, j-1]) / 4

		        #上下にGrid2つに挟まれているとき
		        elif (i % 2) != 0 and (j % 2) == 0:
		        	self.vgrid[i,j] = (self.optimizer.vgrid[i, j+1] + self.optimizer.vgrid[i, j-1]) / 2

		        #左右にGrid2つに挟まれているとき
		        elif (i % 2) == 0 and (j % 2) != 0:
		        	self.vgrid[i,j] = (self.optimizer.vgrid[i+1, j] + self.optimizer.vgrid[i-1, j]) / 2

		        #求めたいGridが既に求まっているとき
		        else
		            self.vgrid[i,j] = self.optimizer.vgrid[i,j]

		#2. それぞれのGridの移動量よりmovingのそこのピクセルが10分前のmovedでどこにあったか推定する
        #movingにflowを足すことでmovedを出す
        for i in range(row):
		    for j in range(col):
                self.moved[i,j] = self.moving[i,j] + self.vgrid[i,j]

		#3. movedであったとされる点での値を加重平均的に求める
		for i in range(row):
		    for j in range(col):
				#求めたいmovedの座標を取り出す
				x = self.moved[i,j][0]
				y = self.moved[i,j][1]

				#movedの点を囲む4つのGridの座標を出す
		        x1 = math.floor(x)
		        x2 = math.cell(x)
		        y1 = math.floor(y)
		        y2 = math.cell(y)

		        #囲んでいる4つのGrifの値を出す
		        a = self.moved.values[x1, y1]
		        b = self.moved.values[x2, y1]
		        c = self.moved.values[x1, y2]
		        d = self.moved.values[x2, y2]

		        #加重平均的にその点のmovedの値を求める
		        self.moved.values[i,j] = (y2-y)*((x2-x)*a + (x-x1)*b) + (y1-y)*((x2-x)*c + (x-x1)*d)

		#4. 3で求めた値より画像を作る
		for i in range(row):
		    for j in range(col):
		        self.moving.values[i, j] = self.moved.values[i,j]

	def cubic_transform(self):
		u'''Linear transform moving image by vgrid'''
		# NEED TO IMPLEMENTATION
		pass
