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
import objc, math
from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSEvent, NSPoint

def unitVector(B, A):
	x = A.x - B.x
	y = A.y - B.y
	length = math.sqrt(x**2 + y**2)
	return (x / length, y / length)


def offsetFrom3Points(n1, n2, n3):
	vectors = (
		unitVector(n1, n2),
		unitVector(n2, n3),
	)
	averageVector = NSPoint(
		sum([v[0] for v in vectors]) / len(vectors),
		sum([v[1] for v in vectors]) / len(vectors)
	)
	roundedCoordinates = [round(c) for c in unitVector(NSPoint(), averageVector)]
	return NSPoint(*roundedCoordinates)
	

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
		shiftKey = 131072
		optionKeyPressed = NSEvent.modifierFlags() & optionKey == optionKey
		shiftKeyPressed = NSEvent.modifierFlags() & shiftKey == shiftKey
		
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
					if shiftKeyPressed:
						offset = offsetFrom3Points(
							thisNode.prevNode.position,
							thisNode.position,
							thisNode.nextNode.position,
							)
						newNode.position = NSPoint(
							thisNode.position.x + offset.x,
							thisNode.position.y + offset.y,
							)
					else:
						newNode.position = thisNode.position
					newNode.smooth = thisNode.smooth
					thisPath.nodes.insert(nodeIndex+1, newNode)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
