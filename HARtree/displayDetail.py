#!/usr/bin/python2
# -*- coding: utf-8 -*-

def HARtree_displayDetail_addSubTree(parent, data):

	global responseContentTreeModel, responseContentTree, responseContentLayout

	for key, value in data.iteritems():

		qkey = QStandardItem(str(key))

		if isinstance(value, list):

			parent.appendRow([qkey])

			if str(key) in ("headers", "queryString"):
				for item in value:
					name = QStandardItem(str(item['name']))
					value = QStandardItem(item['value'].encode("utf8"))

					qkey.appendRow([name, value])

			elif key == "cookies":

				for item in value:
					name = QStandardItem(str(item['name']))
					value = QStandardItem(item['value'].encode("utf8"))

					qkey.appendRow([name, value])

					HARtree_displayDetail_addSubTree(name, item)

			else:
				for i,item in enumerate(value):
					qi = QStandardItem(str(i))
					qkey.appendRow([qi])

					HARtree_displayDetail_addSubTree(qi, item)

		elif isinstance(value, dict):

			if (key == "content"):

				responseContentTreeModel.clear()

				for ckey, cvalue in value.iteritems():

					if ckey != "text":
						cqkey = QStandardItem(str(ckey))

						try:
							cvalue = cvalue.encode("utf8")
						except:
							if isinstance(cvalue, int):
								cvalue = str(cvalue)

						cqvalue = QStandardItem(cvalue)

						responseContentTreeModel.invisibleRootItem().appendRow([cqkey, cqvalue])

				responseContentTreeModel.setHorizontalHeaderLabels(['Name', 'Value'])
				responseContentTree.resizeColumnToContents(0)

				HARtree_displayDetail_contentPreview(value)

				responseContentLayout.setStretchFactor(responseContentTree, 50)
				responseContentLayout.setStretchFactor(HARtree_displayDetail_contentPreview.preview, 50)

			else:
				parent.appendRow([qkey])
				HARtree_displayDetail_addSubTree(qkey, value)
		else:
			if not value:
				value = ""

			if isinstance(value, int) or isinstance(value, float) or  isinstance(value, bool):
				value = str(value)
			else:
				try:
					value = value.encode("utf8")
				except:
					sys.exit("Variable -value- is somewhat weird. Check the encoding.")

			qvalue = QStandardItem(value)
			parent.appendRow([qkey, qvalue])

jsbeautifierAvailable = False
try:
	import jsbeautifier
	jsbeautifierAvailable = True
except ImportError:
	pass

def HARtree_displayDetail_contentPreview(value):

	global responseContentLayout

	if not HARtree_displayDetail_contentPreview.containers:
		HARtree_displayDetail_contentPreview.containers = {
			'label': QLabel(),
			'plainTextEdit': QPlainTextEdit()
		}

		responseContentLayout.addWidget(HARtree_displayDetail_contentPreview.containers['label'])
		responseContentLayout.addWidget(HARtree_displayDetail_contentPreview.containers['plainTextEdit'])
		HARtree_displayDetail_contentPreview.containers['plainTextEdit'].hide()
		HARtree_displayDetail_contentPreview.containers['label'].hide()

	else:
		HARtree_displayDetail_contentPreview.containers['label'].clear()
		HARtree_displayDetail_contentPreview.containers['plainTextEdit'].setPlainText('')

	mime = value["mimeType"]
	if not "encoding" in value.keys():
		if "text" in value.keys():
			if (mime in ("application/x-javascript", "application/javascript", "text/javascript")) and (jsbeautifierAvailable):
				HARtree_displayDetail_contentPreview.containers['plainTextEdit'].setPlainText(jsbeautifier.beautify(value['text']))
			else:
				HARtree_displayDetail_contentPreview.containers['plainTextEdit'].setPlainText(value['text'])

			HARtree_displayDetail_contentPreview.containers['label'].hide()
			HARtree_displayDetail_contentPreview.containers['plainTextEdit'].show()

			HARtree_displayDetail_contentPreview.preview = HARtree_displayDetail_contentPreview.containers['plainTextEdit']

	elif value['encoding'] == 'base64':

		images = {
			"image/jpeg": "JPEG",
			"image/png": "PNG",
			"image/gif": "GIF"
		}

		if (mime in images.keys()):

			by = QByteArray.fromBase64(str(value['text']))
			image = QImage()
			image.loadFromData(by, images[mime])

			HARtree_displayDetail_contentPreview.containers['label'].setPixmap(QPixmap.fromImage(image))
			HARtree_displayDetail_contentPreview.containers['plainTextEdit'].hide()
			HARtree_displayDetail_contentPreview.containers['label'].show()

			HARtree_displayDetail_contentPreview.preview = HARtree_displayDetail_contentPreview.containers['label']

	else:
		sys.exit("Unrecognized content encoding: " + value['encoding'])

HARtree_displayDetail_contentPreview.preview = None
HARtree_displayDetail_contentPreview.containers = None

def HARtree_displayDetail():

	global view, detailParts, detailModels, detailViews

	id = int(view.selectionModel().currentIndex().sibling(view.selectionModel().currentIndex().row(), 0).data())

	root = {}
	for item in detailParts:
		detailModels[item].clear()
		root[item] = detailModels[item].invisibleRootItem()

		HARtree_displayDetail_addSubTree(root[item], sortedEntries[id][item])

		detailModels[item].setHorizontalHeaderLabels(['Name', 'Value'])
		detailViews[item].resizeColumnToContents(0)