#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os.path
import json

class HARhelperFile:

	def __init__(self, fileName):
		self.fileName = fileName
		self.data = {"highlightedEntries": []}

		if os.path.isfile(self.fileName):

			f = open(self.fileName, "r+")
			self.data = json.load(f)
			f.close()

	def save(self):

		f = open(self.fileName, "w")
		json.dump(self.data, f)
		f.close()