#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
HARtree

author: René Kliment < rene (at) renekliment.cz >
"""

import sys
import json
import os.path
import argparse
import tempfile

from operator import itemgetter

from HARtree.fetcher import HARfetcher
from HARtree.helperFile import HARhelperFile
from HARtree.easyList import HAReasyList
from HARtree.loadAndDisplay import *

try:
	from PyQt5.QtCore import *
	from PyQt5.QtGui import *
	from PyQt5.QtWidgets import *
except ImportError:
	sys.exit("PyQt5 not found!")

with open('config.json') as config_file:    
    config = json.load(config_file)

if not config['fetchEngines']['defaultHarStorage']:
	config['fetchEngines']['defaultHarStorage'] = tempfile.gettempdir()

def on_keyHighlightPressed():
	global helperFile

	id = int(view.selectionModel().currentIndex().sibling(view.selectionModel().currentIndex().row(), 0).data())

	if id in helperFile.data["highlightedEntries"]:

		helperFile.data["highlightedEntries"].remove(id)
		idToIdWidget[id].setBackground(QBrush(QColor("white")))

	else:

		helperFile.data["highlightedEntries"].append(id)
		idToIdWidget[id].setBackground(QBrush(QColor("gray")))

	helperFile.save()

class customQTreeView(QTreeView):
    keyHighlightPressed = pyqtSignal()

    def keyPressEvent(self, event):
        super(customQTreeView, self).keyPressEvent(event)
        if (event.key() == Qt.Key_Space):
			self.keyHighlightPressed.emit()

execfile("./HARtree/displayDetail.py")

if __name__ == '__main__':

	# command line arguments parsing
	parser = argparse.ArgumentParser()

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-f", "--file", help='path to a HAR file', default="")
	group.add_argument("-u", "--url", help='generate a HAR file, save it and display it', default="")
	group.add_argument('resource', nargs='?')

	parser.add_argument("-e", "--fetch-engine", help='engine for fetching HARs (ph, bs)', default="browsermobproxy+selenium")
	parser.add_argument("-b", "--engine-browser", help='browser for the engine (ff, ch)', default="firefox")
	parser.add_argument("-l", "--use-easy-list", help='use an easylist to highlight URLs', action="store_true")
	parser.add_argument("-d", "--save-directory", help='directory for saving HAR files, defaults to system temp directory or a configured directory (' + config['fetchEngines']['defaultHarStorage'] + ')', default=config['fetchEngines']['defaultHarStorage'])

	args = parser.parse_args()

	harFileName = ""
	if (args.resource):
		if os.path.isfile(args.resource):
			harFileName = args.resource
		elif args.resource.startswith("http://") or args.resource.startswith("https://"):
			if args.fetch_engine in HARfetcher.supportedEngines and args.engine_browser in HARfetcher.supportedBrowsers:
				harFileName = HARfetcher.fetch(args.resource, config, args.save_directory, args.fetch_engine, args.engine_browser)
			else:
				sys.exit("Unsupported engine.")
		else:
			sys.exit("Resource not recognized / found - use proper command line arguments.")

	elif (args.file):
		if (os.path.isfile(args.file)):
			harFileName = args.file
		else:
			sys.exit("File " + args.file + " does not exist!");

	elif (args.url):
		if (args.fetch_engine in HARfetcher.supportedEngines) and (args.engine_browser in HARfetcher.supportedBrowsers):
			harFileName = HARfetcher.fetch(args.url, config, args.save_directory, args.fetch_engine, args.engine_browser)
		else:
			sys.exit("Unsupported engine / browser.")

	if not harFileName:
		sys.exit("No HAR file. Use some params ...")

	useEasyList = args.use_easy_list

	# GUI
	app = QApplication(sys.argv)

	model = QStandardItemModel()
	model.setHorizontalHeaderLabels(['#', 'Status', 'MIME', 'URL', 'redirectURL', 'Referer'])

	view = customQTreeView()
	view.setSelectionBehavior(QAbstractItemView.SelectRows)
	view.setModel(model)
	view.setUniformRowHeights(True)

	layout = QSplitter()
	layout.addWidget(view)
	layout.setOrientation(Qt.Vertical)
	layout.setWindowTitle('HARtree')
	layout.showMaximized()

	# display data
	har = HARtree_loadFile(harFileName)
	sortedEntries = sorted(har['log']['entries'], key=itemgetter('startedDateTime'))
	idToIdWidget = {}

	easyList = None
	if (useEasyList):
		easyList = HAReasyList(config['adblockparser']['easylist_file'])

	HARtree_populateData(har, sortedEntries, model, idToIdWidget, useEasyList, easyList)

	helperFile = HARhelperFile(harFileName + ".hh")
	for id in helperFile.data['highlightedEntries']:
		idToIdWidget[id].setBackground(QBrush(QColor("gray")))

	view.expandAll()

	view.resizeColumnToContents(0)
	view.resizeColumnToContents(1)
	view.resizeColumnToContents(2)

	view.setColumnWidth(3, 300)
	view.setColumnWidth(4, 300)
	view.setColumnWidth(5, 300)

	selmod = view.selectionModel()

	detailModels = {}
	detailViews = {}

	detailParts = ("request", "response", "timings")
	for item in detailParts:
		detailModels[item] = QStandardItemModel()
		detailModels[item].setHorizontalHeaderLabels(['Name', 'Value'])

		detailViews[item] = QTreeView()
		detailViews[item].setModel(detailModels[item])

	responseContentWidget = QWidget()
	responseContentLayout = QHBoxLayout()
	responseContentWidget.setLayout(responseContentLayout)

	responseContentTreeModel = QStandardItemModel()
	responseContentTreeModel.setHorizontalHeaderLabels(['Name', 'Value'])
	responseContentTree = QTreeView()
	responseContentTree.setModel(responseContentTreeModel)

	responseContentLayout.addWidget(responseContentTree)

	tabs = QTabWidget()
	tabs.addTab(detailViews["request"], "Request")
	tabs.addTab(detailViews["response"], "Response")
	tabs.addTab(responseContentWidget ,"Response Content")
	tabs.addTab(detailViews["timings"], "Timings")

	layout.addWidget(tabs)

	layout.setStretchFactor(0, 1);
	layout.setStretchFactor(1, 0);

	selmod.currentRowChanged.connect(HARtree_displayDetail)
	view.keyHighlightPressed.connect(on_keyHighlightPressed)

	sys.exit(app.exec_())
