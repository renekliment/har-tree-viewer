#!/usr/bin/python2
# -*- coding: utf-8 -*-

class HAReasyList:

	def __init__(self, fileName="./easylist.txt"):
		self.rules = None

		with open(fileName, 'r') as f:
			self.raw_rules = f.readlines()

		from adblockparser import AdblockRules
		self.rules = AdblockRules(self.raw_rules)