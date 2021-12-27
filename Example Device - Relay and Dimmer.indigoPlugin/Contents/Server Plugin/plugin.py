#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2016, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo

import os
import sys
import time

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
	# deviceStartComm() is called on application launch for all of our plugin defined
	# devices, and it is called when a new device is created immediately after its
	# UI settings dialog has been validated. This is a good place to force any properties
	# we need the device to have, and to cleanup old properties.
	def deviceStartComm(self, dev):
		# self.debugLog(u"deviceStartComm: %s" % (dev.name,))

		props = dev.pluginProps
		if dev.deviceTypeId == 'myColorType':
			# Set SupportsColor property so Indigo knows device accepts color actions and should use color UI.
			props["SupportsColor"] = True

			# Cleanup properties used by other device types. These can exist if user switches the device type.
			if "IsLockSubType" in props:
				del props["IsLockSubType"]

			dev.replacePluginPropsOnServer(props)
		elif dev.deviceTypeId == 'myLockType':
			# Set IsLockSubType property so Indigo knows device accepts lock actions and should use lock UI.
			props["IsLockSubType"] = True

			# Cleanup properties used by other device types. These can exist if user switches the device type.
			if "SupportsColor" in props:
				del props["SupportsColor"]

			dev.replacePluginPropsOnServer(props)

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

		###### LOCK ######
		if action.deviceAction == indigo.kDeviceAction.Lock:
			# Command hardware module (dev) to LOCK here:
			# ** IMPLEMENT ME **
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s" % (dev.name, "lock"))

				# And then tell the Indigo Server to update the state.
				dev.updateStateOnServer("onOffState", True)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "lock"), isError=True)

		###### UNLOCK ######
		elif action.deviceAction == indigo.kDeviceAction.Unlock:
			# Command hardware module (dev) to turn UNLOCK here:
			# ** IMPLEMENT ME **
			sendSuccess = True		# Set to False if it failed.

			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s" % (dev.name, "unlock"))

				# And then tell the Indigo Server to update the state:
				dev.updateStateOnServer("onOffState", False)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s failed" % (dev.name, "unlock"), isError=True)

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

		###### SET COLOR LEVELS ######
		elif action.deviceAction == indigo.kDeviceAction.SetColorLevels:
			# action.actionValue is a dict containing the color channel key/value
			# pairs. All color channel keys (redLevel, greenLevel, etc.) are optional
			# so plugin should handle cases where some color values are not specified
			# in the action.
			actionColorVals = action.actionValue

			# Construct a list of channel keys that are possible for what this device
			# supports. It may not support RGB or may not support white levels, for
			# example, depending on how the device's properties (SupportsColor, SupportsRGB,
			# SupportsWhite, SupportsTwoWhiteLevels, SupportsWhiteTemperature) have
			# been specified.
			channelKeys = []
			usingWhiteChannels = False
			if dev.supportsRGB:
				channelKeys.extend(['redLevel', 'greenLevel', 'blueLevel'])
			if dev.supportsWhite:
				channelKeys.extend(['whiteLevel'])
				usingWhiteChannels = True
			if dev.supportsTwoWhiteLevels:
				channelKeys.extend(['whiteLevel2'])
			elif dev.supportsWhiteTemperature:
				channelKeys.extend(['whiteTemperature'])
			# Note having 2 white levels (cold and warm) takes precedence over
			# the use of a white temperature value. You cannot have both, although
			# you can have a single white level and a white temperature value.

			# Next enumerate through the possible color channels and extract that
			# value from the actionValue (actionColorVals).
			keyValueList = []
			resultVals = []
			for channel in channelKeys:
				if channel in actionColorVals:
					brightness = float(actionColorVals[channel])
					brightnessByte = int(round(255.0 * (brightness / 100.0)))
	
					# Command hardware module (dev) to change its color level here:
					# ** IMPLEMENT ME **

					if channel in dev.states:
						keyValueList.append({'key':channel, 'value':brightness})
					result = str(int(round(brightness)))
				elif channel in dev.states:
					# If the action doesn't specify a level that is needed (say the
					# hardware API requires a full RGB triplet to be specified, but
					# the action only contains green level), then the plugin could
					# extract the currently cached red and blue values from the
					# dev.states[] dictionary:
					cachedBrightness = float(dev.states[channel])
					cachedBrightnessByte = int(round(255.0 * (cachedBrightness / 100.0)))
					# Could show in the Event Log '--' to indicate this level wasn't
					# passed in by the action:
					result = '--'
					# Or could show the current device state's cached level:
					#	result = str(int(round(cachedBrightness)))

				# Add a comma to separate the RGB values from the white values for logging.
				if channel == 'blueLevel' and usingWhiteChannels:
					result += ","
				elif channel == 'whiteTemperature' and result != '--':
					result += " K"
				resultVals.append(result)
			# Set to False if it failed.
			sendSuccess = True

			resultValsStr = ' '.join(resultVals)
			if sendSuccess:
				# If success then log that the command was successfully sent.
				indigo.server.log(u"sent \"%s\" %s to %s" % (dev.name, "set color", resultValsStr))

				# And then tell the Indigo Server to update the color level states:
				if len(keyValueList) > 0:
					dev.updateStatesOnServer(keyValueList)
			else:
				# Else log failure but do NOT update state on Indigo Server.
				indigo.server.log(u"send \"%s\" %s to %s failed" % (dev.name, "set color", resultValsStr), isError=True)

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
