# encoding: utf-8

###########################################################################################################
#
#
#	Filter with dialog Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#	For help on the use of Interface Builder:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *


# This is for compatiblity with Glyphs 2.4
try:
	from objc import python_method
except ImportError:
	def python_method(arg):
		return arg
	objc.python_method = python_method


class Rimmer(FilterWithDialog):
	
	# Definitions of IBOutlets
	dialog = objc.IBOutlet()
	paddingField = objc.IBOutlet()
	rimField = objc.IBOutlet()
	
	def settings(self):
		self.menuName = "Rimmer"
		
		# Word on Run Button (default: Apply)
		self.actionButtonLabel = Glyphs.localize({'en': u'Rim', 'de': u'Erweitern'})
		
		# Load dialog from .nib (without .extension)
		self.loadNib('IBdialog', __file__)
	
	# On dialog show
	def start(self):
		
		# Set default value
		Glyphs.registerDefault('com.mekkablue.Rimmer.padding', 15.0)
		Glyphs.registerDefault('com.mekkablue.Rimmer.rim', 10.0)
		
		# Set value of text field
		self.paddingField.setStringValue_(Glyphs.defaults['com.mekkablue.Rimmer.padding'])
		self.rimField.setStringValue_(Glyphs.defaults['com.mekkablue.Rimmer.rim'])
		
		# Set focus to text field
		self.paddingField.becomeFirstResponder()
		
	# Actions triggered by UI
	@objc.IBAction
	def setPadding_( self, sender ):
		Glyphs.defaults['com.mekkablue.Rimmer.padding'] = sender.floatValue()
		self.update()
	
	@objc.IBAction
	def setRim_( self, sender ):
		Glyphs.defaults['com.mekkablue.Rimmer.rim'] = sender.floatValue()
		self.update()
	
	# Actual filter
	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		# Set defaults
		padding = 15.0
		rim = 10.0
		
		if not inEditView:
			# Called on font export, get value from customParameters
			if 'padding' in customParameters:
				padding = float(customParameters['padding'])
			if 'rim' in customParameters:
				rim = float(customParameters['rim'])
		else:
			# Called through UI, use stored value
			padding = float(Glyphs.defaults['com.mekkablue.Rimmer.padding'])
			rim = float(Glyphs.defaults['com.mekkablue.Rimmer.rim'])
		
		# prepare inner part:
		layer.decomposeCorners()
		coreLayer = layer.copyDecomposedLayer()
		coreLayer.removeOverlap()
		coreLayer.addInflectionPoints()
		coreLayer.correctPathDirection()
		
		# prepare rim:
		rimLayer = coreLayer.copy()
		self.offsetLayer( rimLayer, padding, makeStroke=False, position=0.0, autoStroke=False )
		self.offsetLayer( rimLayer, rim, makeStroke=True, position=0.0, autoStroke=False )
		
		# clean out original layer, and add core+rim:
		layer.components = None
		layer.hints = None
		layer.paths = coreLayer.paths
		layer.paths.extend( rimLayer.paths )
		
	@objc.python_method
	def offsetLayer( self, thisLayer, offset, makeStroke=False, position=0.5, autoStroke=False ):
		offsetFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		offsetFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_(
			thisLayer,
			offset, offset, # horizontal and vertical offset
			makeStroke,     # if True, creates a stroke
			autoStroke,     # if True, distorts resulting shape to vertical metrics
			position,       # stroke distribution to the left and right, 0.5 = middle
			None, None )
	
	def generateCustomParameter( self ):
		return "%s; padding:%s; rim:%s" % (
			self.__class__.__name__, 
			Glyphs.defaults['com.mekkablue.Rimmer.padding'],
			Glyphs.defaults['com.mekkablue.Rimmer.rim'],
			)
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
