#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2019, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo

import os
import random
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
	# Poll all of the states from the energy meter and pass new values to
	# Indigo Server.
	def _refreshStatesFromHardware(self, dev, logRefresh):
		# As an example here we update the current power (Watts) to a random
		# value, and we increase the kWh by a smidge.
		#
		# Note the states are automatically created based on the SupportsEnergyMeter
		# and SupportsPowerMeter device properties.
		#
		# The plugin instance property is updated by updating the states.
		keyValueList = []
		if "curEnergyLevel" in dev.states:
			simulateWatts = random.randint(0, 500)
			simulateWattsStr = "%d W" % (simulateWatts)
			if logRefresh:
				indigo.server.log(u"received \"%s\" %s to %s" % (dev.name, "power load", simulateWattsStr))
			keyValueList.append({'key':'curEnergyLevel', 'value':simulateWatts, 'uiValue':simulateWattsStr})

		if "accumEnergyTotal" in dev.states:
			simulateKwh = dev.states.get("accumEnergyTotal", 0) + 0.001
			simulateKwhStr = "%.3f kWh" % (simulateKwh)
			if logRefresh:
				indigo.server.log(u"received \"%s\" %s to %s" % (dev.name, "energy total", simulateKwhStr))
			keyValueList.append({'key':'accumEnergyTotal', 'value':simulateKwh, 'uiValue':simulateKwhStr})

		dev.updateStatesOnServer(keyValueList)

	########################################
	def runConcurrentThread(self):
		try:
			while True:
				for dev in indigo.devices.iter("self"):
					if not dev.enabled or not dev.configured:
						continue

					# Plugins that need to poll out the status from the meter
					# could do so here, then broadcast back the new values to the
					# Indigo Server.
					self._refreshStatesFromHardware(dev, False)

				self.sleep(2)
		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.

	########################################
	def validateDeviceConfigUi(self, valuesDict, typeId, devId):
		return (True, valuesDict)

	########################################
	def deviceStartComm(self, dev):
		# Called when communication with the hardware should be established.
		# Here would be a good place to poll out the current states from the
		# meter. If periodic polling of the meter is needed (that is, it
		# doesn't broadcast changes back to the plugin somehow), then consider
		# adding that to runConcurrentThread() above.
		self._refreshStatesFromHardware(dev, True)

	def deviceStopComm(self, dev):
		# Called when communication with the hardware should be shutdown.
		pass

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
			self._refreshStatesFromHardware(dev, True)

		###### ENERGY RESET ######
		elif action.deviceAction == indigo.kUniversalAction.EnergyReset:
			# Request that the hardware module (dev) reset its accumulative energy usage data here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "energy usage reset"))
			# And then tell Indigo to reset it by just setting the value to 0.
			# This will automatically reset Indigo's time stamp for the accumulation.
			dev.updateStateOnServer("accumEnergyTotal", 0.0)

		###### STATUS REQUEST ######
		elif action.deviceAction == indigo.kUniversalAction.RequestStatus:
			# Query hardware module (dev) for its current status here:
			# ** IMPLEMENT ME **
			self._refreshStatesFromHardware(dev, True)

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

