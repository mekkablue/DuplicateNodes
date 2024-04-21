# encoding: utf-8

###########################################################################################################
#
#
#	Filter without dialog plug-in
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSEvent

class DuplicateNodes(FilterWithoutDialog):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Duplicate Nodes',
			'de': 'Punkte verdoppeln',
			'fr': 'Dupliquer nœuds',
			'es': 'Duplicar nodos',
			'pt': 'Duplicar nodos',
			'it': 'Duplica nodi',
			# 'jp': '私のフィルター',
			# 'ko': '내 필터',
			# 'zh': '我的过滤器',
			})



	@objc.python_method
	def filter(self, thisLayer, inEditView, customParameters):
		optionKey = 524288
		optionKeyPressed = NSEvent.modifierFlags() & optionKey == optionKey
		
		selectedIndexes = []
		for pathIndex, thisPath in enumerate(thisLayer.paths):
			for nodeIndex, thisNode in enumerate(thisPath.nodes):
				if thisNode.selected:
					selectedIndexes.append( (pathIndex, nodeIndex) )
		
		appliedLayers = [thisLayer]
		if optionKeyPressed:
			thisGlyph = thisLayer.parent
			for thatLayer in thisGlyph.layers:
				if thatLayer != thisLayer and thisLayer.compareString() == thatLayer.compareString():
					appliedLayers.append(thatLayer)
		
		for thisLayer in appliedLayers:
			for pathIndex, nodeIndex in reversed(selectedIndexes):
				thisPath = thisLayer.paths[pathIndex]
				thisNode = thisPath.nodes[nodeIndex]
				if thisNode.type != OFFCURVE:
					newNode = GSNode()
					newNode.position = thisNode.position
					newNode.smooth = thisNode.smooth
					thisPath.nodes.insert(nodeIndex+1, newNode)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
