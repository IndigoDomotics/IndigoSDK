#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo

import os
import sys

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = True

	########################################
	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	########################################
	# DeviceFactory methods (specified in Devices.xml):
	#
	# All device factory methods are passed a devIdList argument, which is
	# a list of device IDs in the current group being edited. Plugins add
	# and remove devices to/from the group by making indigo.device.create()
	# and indigo.device.delete(). On subsequent factory method calls the
	# devIdList will automatically be updated to reflect any changes.
	#
	# Plugins should set the main model type using dev.model, and the sub-
	# type using dev.subType, which is used for the tabbed UI. Be sure
	# and call dev.replaceOnServer() after modifying the .model and .subType
	# attributes to push those changes to the server.
	####################
	def getDeviceFactoryUiValues(self, devIdList):
		valuesDict = indigo.Dict()
		errorMsgDict = indigo.Dict()
		return (valuesDict, errorMsgDict)

	def validateDeviceFactoryUi(self, valuesDict, devIdList):
		errorsDict = indigo.Dict()
		return (True, valuesDict, errorsDict)

	def closedDeviceFactoryUi(self, valuesDict, userCancelled, devIdList):
		return

	####################
	def _getDeviceGroupList(self, filter, valuesDict, devIdList):
		menuItems = []
		for devId in devIdList:
			if devId in indigo.devices:
				dev = indigo.devices[devId]
				devName = dev.name
			else:
				devName = u"- device not found -"
			menuItems.append((devId, devName))
		return menuItems

	def _addRelay(self, valuesDict, devIdList):
		newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="myRelayType")
		newdev.model = "Example Multi-Device"
		newdev.subType = "Relay"		# Manually need to set the model and subType names (for UI only)
		newdev.replaceOnServer()
		return valuesDict

	def _addDimmer(self, valuesDict, devIdList):
		newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="myDimmerType")
		newdev.model = "Example Multi-Device"
		newdev.subType = "Dimmer"		# Manually need to set the model and subType names (for UI only)
		newdev.replaceOnServer()
		return valuesDict

	def _addX10MotionSensor(self, valuesDict, devIdList):
		# Not fully supported -- device groups currently should only contain
		# devices defined by the plugin. The UI doesn't properly handle showing
		# and editing X10 / INSTEON / etc. devices as part of the group.
		#
		# newdev = indigo.device.create(indigo.kProtocol.X10, deviceTypeId="Motion Detector")
		# newdev.model = "Example Multi-Device"
		# newdev.subType = "Motion"	# Manually need to set the model and subType names (for UI only)
		# newdev.replaceOnServer()
		return valuesDict

	def _addX10SprinklerDevice(self, valuesDict, devIdList):
		# Not fully supported -- device groups currently should only contain
		# devices defined by the plugin. The UI doesn't properly handle showing
		# and editing X10 / INSTEON / etc. devices as part of the group.
		#
		# newdev = indigo.device.create(indigo.kProtocol.X10, deviceTypeId="Rain8 (8 zone)")
		# newdev.model = "Example Multi-Device"
		# newdev.subType = "Sprinkler"	# Manually need to set the model and subType names (for UI only)
		# newdev.replaceOnServer()
		return valuesDict

	def _removeDimmerDevices(self, valuesDict, devIdList):
		for devId in devIdList:
			try:
				dev = indigo.devices[devId]
				if dev.deviceTypeId == "myDimmerType":
					indigo.device.delete(dev)
			except:
				pass	# delete doesn't allow (throws) on root elem
		return valuesDict

	def _removeRelayDevices(self, valuesDict, devIdList):
		for devId in devIdList:
			try:
				dev = indigo.devices[devId]
				if dev.deviceTypeId == "myRelayType":
					indigo.device.delete(dev)
			except:
				pass	# delete doesn't allow (throws) on root elem
		return valuesDict

	def _removeAllDevices(self, valuesDict, devIdList):
		for devId in devIdList:
			try:
				indigo.device.delete(devId)
			except:
				pass	# delete doesn't allow (throws) on root elem
		return valuesDict

	########################################
	def validateDeviceConfigUi(self, valuesDict, typeId, devId):
		return (True, valuesDict)

	########################################
	# Relay / Dimmer Action callback
	######################
	def actionControlDevice(self, action, dev):
		###### TURN ON ######
		if action.deviceAction == indigo.kDeviceAction.TurnOn:
			# Command hardware module (dev) to turn ON here:
			# ** IMPLEMENT ME **
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s" % (dev.name, "on"))

				# And then tell the Indigo Server to update the state.
				dev.updateStateOnServer("onOffState", True)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "on"), isError=True)

		###### TURN OFF ######
		elif action.deviceAction == indigo.kDeviceAction.TurnOff:
			# Command hardware module (dev) to turn OFF here:
			# ** IMPLEMENT ME **
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s" % (dev.name, "off"))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("onOffState", False)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "off"), isError=True)

		###### TOGGLE ######
		elif action.deviceAction == indigo.kDeviceAction.Toggle:
			# Command hardware module (dev) to toggle here:
			# ** IMPLEMENT ME **
			newOnState = not dev.onState
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s" % (dev.name, "toggle"))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("onOffState", newOnState)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "toggle"), isError=True)

		###### SET BRIGHTNESS ######
		elif action.deviceAction == indigo.kDeviceAction.SetBrightness:
			# Command hardware module (dev) to set brightness here:
			# ** IMPLEMENT ME **
			newBrightness = action.actionValue
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "set brightness", newBrightness))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("brightnessLevel", newBrightness)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "set brightness", newBrightness), isError=True)

		###### BRIGHTEN BY ######
		elif action.deviceAction == indigo.kDeviceAction.BrightenBy:
			# Command hardware module (dev) to do a relative brighten here:
			# ** IMPLEMENT ME **
			newBrightness = dev.brightness + action.actionValue
			if newBrightness > 100:
				newBrightness = 100
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "brighten", newBrightness))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("brightnessLevel", newBrightness)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "brighten", newBrightness), isError=True)

		###### DIM BY ######
		elif action.deviceAction == indigo.kDeviceAction.DimBy:
			# Command hardware module (dev) to do a relative dim here:
			# ** IMPLEMENT ME **
			newBrightness = dev.brightness - action.actionValue
			if newBrightness < 0:
				newBrightness = 0
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "dim", newBrightness))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("brightnessLevel", newBrightness)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "dim", newBrightness), isError=True)


	########################################
	# General Action callback
	######################
	def actionControlUniversal(self, action, dev):
		###### BEEP ######
		if action.deviceAction == indigo.kUniversalAction.Beep:
			# Beep the hardware module (dev) here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "beep request"))

		###### ENERGY UPDATE ######
		elif action.deviceAction == indigo.kUniversalAction.EnergyUpdate:
			# Request hardware module (dev) for its most recent meter data here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "energy update request"))

		###### ENERGY RESET ######
		elif action.deviceAction == indigo.kUniversalAction.EnergyReset:
			# Request that the hardware module (dev) reset its accumulative energy usage data here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "energy reset request"))

		###### STATUS REQUEST ######
		elif action.deviceAction == indigo.kUniversalAction.RequestStatus:
			# Query hardware module (dev) for its current status here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "status request"))

	########################################
	# Custom Plugin Action callbacks (defined in Actions.xml)
	######################
	def setBacklightBrightness(self, pluginAction, dev):
		try:
			newBrightness = int(pluginAction.props.get(u"brightness", 100))
		except ValueError:
			# The int() cast above might fail if the user didn't enter a number:
			indigo.server.log(u"set backlight brightness action to device \"%s\" -- invalid brightness value" % (dev.name,), isError=True)
			return

		# Command hardware module (dev) to set backlight brightness here:
		# ** IMPLEMENT ME **
		sendSuccess = True		# Set to False if it failed.

		if sendSuccess:
			# If success then log that the command was successfully sent.
			indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "set backlight brightness", newBrightness))

			# And then tell the Indigo Server to update the state:
			dev.updateStateOnServer("backlightBrightness", newBrightness)
		else:
			# Else log failure but do NOT update state on Indigo Server.
			indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "set backlight brightness", newBrightness), isError=True)

