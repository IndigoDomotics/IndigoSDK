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
		self.speedLabels = [u"off", u"low", u"medium", u"high"]

	########################################
	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	########################################
	def validateDeviceConfigUi(self, valuesDict, typeId, devId):
		return (True, valuesDict)

	########################################
	# Speed Control Action callback
	######################
	def actionControlSpeedControl(self, action, dev):
		###### TURN ON ######
		if action.speedControlAction == indigo.kSpeedControlAction.TurnOn:
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
		elif action.speedControlAction == indigo.kSpeedControlAction.TurnOff:
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
		elif action.speedControlAction == indigo.kSpeedControlAction.Toggle:
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

		###### SET SPEED INDEX ######
		elif action.speedControlAction == indigo.kSpeedControlAction.SetSpeedIndex:
			# Command hardware module (dev) to change the speed here to a specific
			# speed index (0=off, 1=low, ..., 3=high):
			# ** IMPLEMENT ME **
			newSpeedIndex = action.actionValue
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s to %s" % (dev.name, "set motor speed", self.speedLabels[newSpeedIndex]))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("speedIndex", newSpeedIndex)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s to %s failed" % (dev.name, "set motor speed", self.speedLabels[newSpeedIndex]), isError=True)

		###### SET SPEED LEVEL ######
		elif action.speedControlAction == indigo.kSpeedControlAction.SetSpeedLevel:
			# Command hardware module (dev) to change the speed here to an absolute
			# speed level (0 to 100):
			# ** IMPLEMENT ME **
			newSpeedLevel = action.actionValue
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s to %d" % (dev.name, "set motor speed", newSpeedLevel))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("speedLevel", newSpeedLevel)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s to %d failed" % (dev.name, "set motor speed", newSpeedLevel), isError=True)

		###### INCREASE SPEED INDEX BY ######
		elif action.speedControlAction == indigo.kSpeedControlAction.IncreaseSpeedIndex:
			# Command hardware module (dev) to do a relative speed increase here:
			# ** IMPLEMENT ME **
			newSpeedIndex = dev.speedIndex + action.actionValue
			if newSpeedIndex > 3:
				newSpeedIndex = 3
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s to %s" % (dev.name, "motor speed increase", self.speedLabels[newSpeedIndex]))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("speedIndex", newSpeedIndex)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s to %s failed" % (dev.name, "motor speed increase", self.speedLabels[newSpeedIndex]), isError=True)

		###### DECREASE SPEED INDEX BY ######
		elif action.speedControlAction == indigo.kSpeedControlAction.DecreaseSpeedIndex:
			# Command hardware module (dev) to do a relative speed decrease here:
			# ** IMPLEMENT ME **
			newSpeedIndex = dev.speedIndex - action.actionValue
			if newSpeedIndex < 0:
				newSpeedIndex = 0
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s to %s" % (dev.name, "motor speed decrease", self.speedLabels[newSpeedIndex]))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("speedIndex", newSpeedIndex)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s to %s failed" % (dev.name, "motor speed decrease", self.speedLabels[newSpeedIndex]), isError=True)

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

