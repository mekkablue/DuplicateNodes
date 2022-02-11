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

class DuplicateNodes(FilterWithoutDialog):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Duplicate Nodes',
			'de': 'Punkte verdoppeln',
			'fr': 'Dupliquer nœuds',
			'es': 'Duplicar nodos',
			'pt': 'Duplicar nodos',
			# 'jp': '私のフィルター',
			# 'ko': '내 필터',
			# 'zh': '我的过滤器',
			})

	@objc.python_method
	def filter(self, thisLayer, inEditView, customParameters):
		for thisPath in thisLayer.paths:
			for i in reversed(range(len(thisPath.nodes))):
				thisNode = thisPath.nodes[i]
				if thisNode.selected and thisNode.type != OFFCURVE:
					newNode = GSNode()
					newNode.position = thisNode.position
					thisPath.nodes.insert(i+1, newNode)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
