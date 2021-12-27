#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2021, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo

import os
import sys
import random

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
	def runConcurrentThread(self):
		try:
			while True:
				for dev in indigo.devices.iter("self"):
					if not dev.enabled or not dev.configured:
						continue

					# Plugins that need to poll out the status from the sensor
					# could do so here, then broadcast back the new values to the
					# Indigo Server via updateStateOnServer. For this example, we
					# could toggle the onOffState every 2 seconds. If the sensor
					# always broadcasts out changes (or is just 1-way), then this
					# entire runConcurrentThread() method can be deleted.
					if dev.deviceTypeId == u"myTempSensor":
						if dev.sensorValue is not None:
							exampleTempFloat = random.randint(560, 880) / 10.0		# random between 56.0 and 88.0 degrees F
							exampleTempStr = "%.1f °F" % (exampleTempFloat)

							keyValueList = []
							keyValueList.append({'key':'sensorValue', 'value':exampleTempFloat, 'uiValue':exampleTempStr})
							# Override the state icon shown (in Indigo Touch and client Main Window)
							# for this device to be the a temperature sensor:
							if dev.onState is not None:
								keyValueList.append({'key':'onOffState', 'value':not dev.onState})
								dev.updateStatesOnServer(keyValueList)
								if dev.onState:
									dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensorOn)
								else:
									dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)
							else:
								dev.updateStatesOnServer(keyValueList)
								dev.updateStateImageOnServer(indigo.kStateImageSel.TemperatureSensor)
						elif dev.onState is not None:
							dev.updateStateOnServer("onOffState", not dev.onState)
							dev.updateStateImageOnServer(indigo.kStateImageSel.Auto)
						else:
							dev.updateStateImageOnServer(indigo.kStateImageSel.Auto)
				self.sleep(2)
		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.

	########################################
	def validateDeviceConfigUi(self, valuesDict, typeId, devId):
		return (True, valuesDict)

	########################################
	def deviceStartComm(self, dev):
		# Called when communication with the hardware should be started.
		pass

	def deviceStopComm(self, dev):
		# Called when communication with the hardware should be shutdown.
		pass

	########################################
	# Sensor Action callback
	######################
	def actionControlSensor(self, action, dev):
		###### TURN ON ######
		# Ignore turn on/off/toggle requests from clients since this is a read-only sensor.
		if action.sensorAction == indigo.kSensorAction.TurnOn:
			indigo.server.log(u"ignored \"%s\" %s request (sensor is read-only)" % (dev.name, "on"))
			# But we could request a sensor state update if we wanted like this:
			# dev.updateStateOnServer("onOffState", True)

		###### TURN OFF ######
		# Ignore turn on/off/toggle requests from clients since this is a read-only sensor.
		elif action.sensorAction == indigo.kSensorAction.TurnOff:
			indigo.server.log(u"ignored \"%s\" %s request (sensor is read-only)" % (dev.name, "off"))
			# But we could request a sensor state update if we wanted like this:
			# dev.updateStateOnServer("onOffState", False)

		###### TOGGLE ######
		# Ignore turn on/off/toggle requests from clients since this is a read-only sensor.
		elif action.sensorAction == indigo.kSensorAction.Toggle:
			indigo.server.log(u"ignored \"%s\" %s request (sensor is read-only)" % (dev.name, "toggle"))
			# But we could request a sensor state update if we wanted like this:
			# dev.updateStateOnServer("onOffState", not dev.onState)

	########################################
	# General Action callback
	######################
	def actionControlUniversal(self, action, dev):
		###### BEEP ######
		if action.deviceAction == indigo.kUniversalAction.Beep:
			# Beep the hardware module (dev) here:
			# ** IMPLEMENT ME **
			indigo.server.log(u"sent \"%s\" %s" % (dev.name, "beep request"))

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

