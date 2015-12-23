#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import json

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def HARtree_loadFile(fileName):

	f = open(fileName, 'r')
	return json.load(f)

def HARtree_populateData(har, sortedEntries, model, idToIdWidget, useEasyList, easyList):

	invi = model.invisibleRootItem()

	urlToId = {}
	urlToParent = {}
	locationOrigin = {}

	for i, entry in enumerate(sortedEntries):
		qindex = QStandardItem( str(i) )
		idToIdWidget[i] = qindex

		statusCode = str(entry['response']['status'])
		qstatusCode = QStandardItem( statusCode )
		qstatusCode.setToolTip(entry['response']['statusText'])

		mime = ""
		if 'mimeType' in entry['response']['content'].keys():
			mime = entry['response']['content']['mimeType']
		qmime = QStandardItem( mime )

		url = entry['request']['url'].encode("utf8").replace(":443/", "/") # TODO: replace with a regexp
		qurl = QStandardItem(url)
		qurl.setToolTip(url)

		redirectUrl = entry['response']['redirectURL'].encode("utf8")
		qredirectUrl = QStandardItem(redirectUrl)
		qredirectUrl.setToolTip(redirectUrl)

		if (statusCode != "200"):
			font = QFont()
			font.setBold(True)
			qstatusCode.setFont(font)

		if useEasyList:
			if easyList.rules.should_block(url):
				qurl.setBackground(QBrush(QColor("yellow")))


		referer = ''
		for header in entry['request']['headers']:
			if (header['name'].lower() == 'referer'):
				referer = header['value']

		qreferer = QStandardItem(referer)
		qreferer.setToolTip(referer)

		row = [qindex, qstatusCode, qmime, qurl, qredirectUrl, qreferer]

		urlToId[url] = i
		urlToParent[url] = row[0]

		if redirectUrl:
			locationOrigin[redirectUrl] = url

		if (url in locationOrigin.keys()):
			urlToParent[locationOrigin[url]].appendRow(row)
		elif (referer) and (referer in urlToId):
			urlToParent[referer].appendRow(row)
		else:
			invi.appendRow(row)