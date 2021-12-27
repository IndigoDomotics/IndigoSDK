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

	########################################
	# IOM logging methods
	####################
	def logListDivider(self, sectionName):
		indigo.server.log(u"===================================================")
		indigo.server.log(sectionName)
		self.logElemDivider()

	def logElemDivider(self):
		indigo.server.log(u"---------------------------------------------------")

	def logBaseElem(self, elem, folders):
		indigo.server.log(u"        INSTANCE: " + elem.__class__.__name__)
		if len(elem.description) > 0:
			indigo.server.log(u"     DESCRIPTION: " + elem.description)
		if folders and elem.folderId != 0:
			indigo.server.log(u"       IN FOLDER: " + folders.getName(elem.folderId))
		indigo.server.log(u"  REMOTE DISPLAY: " + str(elem.remoteDisplay))

	def logBaseFolder(self, elem):
		if len(elem.description) > 0:
			indigo.server.log(u"     DESCRIPTION: " + elem.description)
		indigo.server.log(u"  REMOTE DISPLAY: " + str(elem.remoteDisplay))

	########################################
	def logDeviceBase(self, elem):
		self.logBaseElem(elem, indigo.devices.folders)
		indigo.server.log(u"        PROTOCOL: " + str(elem.protocol))
		indigo.server.log(u"      MODEL NAME: " + str(elem.model))
		indigo.server.log(u"         ADDRESS: " + str(elem.address))
		if elem.protocol == indigo.kProtocol.Insteon and elem.buttonGroupCount > 0:
			indigo.server.log(u"    BUTTON COUNT: " + str(elem.buttonGroupCount))
		indigo.server.log(u"    LAST CHANGED: " + str(elem.lastChanged))

		supports = ""
		if elem.supportsAllLightsOnOff:
			supports += "AllLightsOnOff "
		if elem.supportsAllOff:
			supports += "AllOff "
		if elem.supportsStatusRequest:
			supports += "StatusRequest "
		if len(supports) == 0:
			supports = "--"
		indigo.server.log(u"        SUPPORTS: " + supports)

	####################
	def logDeviceSensor(self, elem):
		self.logDeviceBase(elem)
		indigo.server.log(u"           IS ON: " + str(elem.onState))

	####################
	def logDeviceRelay(self, elem):
		self.logDeviceBase(elem)
		indigo.server.log(u"           IS ON: " + str(elem.onState))

	####################
	def logDeviceDimmer(self, elem):
		self.logDeviceRelay(elem)
		indigo.server.log(u"      BRIGHTNESS: " + str(elem.brightness))

	####################
	def logDeviceMultiIO(self, elem):
		self.logDeviceBase(elem)
		if elem.analogInputCount > 0:
			indigo.server.log(u"   ANALOG INPUTS: " + str(elem.analogInputs))
		if elem.binaryInputCount > 0:
			indigo.server.log(u"   BINARY INPUTS: " + str(elem.binaryInputs))
		if elem.sensorInputCount > 0:
			indigo.server.log(u"   SENSOR INPUTS: " + str(elem.sensorInputs))
		if elem.binaryOutputCount > 0:
			indigo.server.log(u"  BINARY OUTPUTS: " + str(elem.binaryOutputs))

	####################
	def logDeviceSprinkler(self, elem):
		self.logDeviceBase(elem)
		indigo.server.log(u"      ZONE COUNT: " + str(elem.zoneCount))
		indigo.server.log(u"      ZONE NAMES: " + str(elem.zoneNames))
		indigo.server.log(u"   MAX DURATIONS: " + str(elem.zoneMaxDurations))
		if len(elem.zoneScheduledDurations) > 0:
			indigo.server.log(u" SCHEDULED DURA.: " + str(elem.zoneScheduledDurations))
		if elem.activeZone >= 0:
			indigo.server.log(u"     ACTIVE ZONE: " + elem.zoneNames[elem.activeZone])

	####################
	def logDeviceThermostat(self, elem):
		self.logDeviceBase(elem)
		indigo.server.log(u"       HVAC MODE: " + str(elem.hvacMode))
		indigo.server.log(u"        FAN MODE: " + str(elem.fanMode))
		indigo.server.log(u"   COOL SETPOINT: " + str(elem.coolSetpoint))
		indigo.server.log(u"   HEAT SETPOINT: " + str(elem.heatSetpoint))
		indigo.server.log(u"      TEMP COUNT: " + str(elem.temperatureSensorCount))
		indigo.server.log(u"           TEMPS: " + str(elem.temperatures))
		indigo.server.log(u"  HUMIDITY COUNT: " + str(elem.humiditySensorCount))
		indigo.server.log(u"        HUMIDITY: " + str(elem.humidities))
		indigo.server.log(u"      COOL IS ON: " + str(elem.coolIsOn))
		indigo.server.log(u"      HEAT IS ON: " + str(elem.heatIsOn))
		indigo.server.log(u"       FAN IS ON: " + str(elem.fanIsOn))

	####################
	def logDevice(self, elem):
		if isinstance(elem, indigo.DimmerDevice):
			self.logDeviceDimmer(elem)
		elif isinstance(elem, indigo.RelayDevice):
			self.logDeviceRelay(elem)
		elif isinstance(elem, indigo.SensorDevice):
			self.logDeviceSensor(elem)
		elif isinstance(elem, indigo.MultiIODevice):
			self.logDeviceMultiIO(elem)
		elif isinstance(elem, indigo.SprinklerDevice):
			self.logDeviceSprinkler(elem)
		elif isinstance(elem, indigo.ThermostatDevice):
			self.logDeviceThermostat(elem)
		else:
			self.logDeviceBase(elem)

	########################################
	def logEventBase(self, elem, folders):
		self.logBaseElem(elem, folders)
		indigo.server.log(u"         ENABLED: " + str(elem.enabled))
		indigo.server.log(u"          UPLOAD: " + str(elem.upload))
		if elem.suppressLogging:
			indigo.server.log(u"SUPPRESS LOGGING: True")
		# ToDo: Need to add conditional tree and action list traversal here.

	####################
	def logTrigger(self, elem):
		self.logEventBase(elem, indigo.triggers.folders)

		if isinstance(elem, indigo.DeviceStateChangeTrigger):
			indigo.server.log(u"          DEVICE: " + str(indigo.devices.getName(elem.deviceId)))
			indigo.server.log(u"     CHANGE TYPE: " + str(elem.stateChangeType))
			indigo.server.log(u"    SELECTOR KEY: " + str(elem.stateSelector))
			if elem.stateSelectorIndex > 0:
				indigo.server.log(u"  SELECTOR INDEX: " + str(elem.stateSelectorIndex))
			if len(elem.stateValue) > 0:
				indigo.server.log(u"     STATE VALUE: " + str(elem.stateValue))
		elif isinstance(elem, indigo.VariableValueChangeTrigger):
			indigo.server.log(u"        VARIABLE: " + str(indigo.variables.getName(elem.variableId)))
			indigo.server.log(u"     CHANGE TYPE: " + str(elem.variableChangeType))
			if len(elem.variableValue) > 0:
				indigo.server.log(u"  VARIABLE VALUE: " + str(elem.variableValue))
		elif isinstance(elem, indigo.InsteonCommandReceivedTrigger):
			indigo.server.log(u" INSTEON COMMAND: " + str(elem.command))
			indigo.server.log(u"     SOURCE TYPE: " + str(elem.commandSourceType))
			if elem.commandSourceType == indigo.kDeviceSourceType.DeviceId:
				indigo.server.log(u"          DEVICE: " + str(indigo.devices.getName(elem.deviceId)))
			indigo.server.log(u"       GROUP NUM: " + str(elem.buttonOrGroup))
		elif isinstance(elem, indigo.X10CommandReceivedTrigger):
			indigo.server.log(u"     X10 COMMAND: " + str(elem.command))
			indigo.server.log(u"     SOURCE TYPE: " + str(elem.commandSourceType))
			if elem.commandSourceType == indigo.kDeviceSourceType.DeviceId:
				indigo.server.log(u"          DEVICE: " + str(indigo.devices.getName(elem.deviceId)))
			elif elem.commandSourceType == indigo.kDeviceSourceType.RawAddress:
				indigo.server.log(u"         ADDRESS: " + str(elem.address))
			elif elem.command == indigo.kX10Cmd.AvButtonPressed:
				indigo.server.log(u"      A/V BUTTON: " + str(elem.avButton))
		elif isinstance(elem, indigo.EmailReceivedTrigger):
			indigo.server.log(u"    EMAIL FILTER: " + str(elem.emailFilter))
			if elem.emailFilter == indigo.kEmailFilter.MatchEmailFields:
				indigo.server.log(u"     FROM FILTER: " + str(elem.emailFrom))
				indigo.server.log(u"  SUBJECT FILTER: " + str(elem.emailSubject))

	####################
	def logSchedule(self, elem):
		self.logEventBase(elem, indigo.schedules.folders)
		indigo.server.log(u"       DATE TYPE: " + str(elem.dateType))
		indigo.server.log(u"       TIME TYPE: " + str(elem.timeType))
		if elem.dateType == indigo.kDateType.Absolute and elem.timeType == indigo.kTimeType.Absolute:
			indigo.server.log(u"   DATE AND TIME: " + str(elem.absoluteDateTime))
		elif elem.dateType == indigo.kDateType.Absolute:
			indigo.server.log(u"   ABSOLUTE DATE: " + str(elem.absoluteDate.date()))
		elif elem.timeType == indigo.kTimeType.Absolute:
			indigo.server.log(u"   ABSOLUTE TIME: " + str(elem.absoluteTime.time()))
		if elem.sunDelta > 0:
			indigo.server.log(u"       SUN DELTA: " + str(elem.sunDelta) + " seconds")
		if elem.randomizeBy > 0:
			indigo.server.log(u"    RANDOMIZE BY: " + str(elem.randomizeBy) + " seconds")
		indigo.server.log(u"  NEXT EXECUTION: " + str(elem.nextExecution))
		# ToDo: Need to log additional properties after they are implemented here.

	####################
	def logActionGroup(self, elem):
		self.logBaseElem(elem, indigo.actionGroups.folders)
		# ToDo: Need to add action list traversal here.

	####################
	def logControlPage(self, elem):
		self.logBaseElem(elem, indigo.controlPages.folders)
		indigo.server.log(u"     HIDE TABBAR: " + str(elem.hideTabBar))
		if len(elem.backgroundImage) > 0:
			indigo.server.log(u"BACKGROUND IMAGE: " + str(elem.backgroundImage))
		# ToDo: Need to log additional properties after they are implemented here.
		# ToDo: Need to add control list traversal here.

	####################
	def logVariable(self, elem):
		self.logBaseElem(elem, indigo.variables.folders)
		indigo.server.log(u"           VALUE: " + str(elem.value))
		if elem.readOnly:
			indigo.server.log(u"       READ ONLY: True")

	########################################
	# Actions defined in MenuItems.xml:
	####################
	def traverseDevices(self):
		self.logListDivider("DEVICES")
		for folder in indigo.devices.folders:
			indigo.server.log(u"          FOLDER: " + folder.name)
			self.logBaseFolder(folder)
		for elem in indigo.devices:
			self.logElemDivider()
			indigo.server.log(u"          DEVICE: " + elem.name)
			self.logDevice(elem)

	def traverseTriggers(self):
		self.logListDivider("TRIGGERS")
		for folder in indigo.triggers.folders:
			indigo.server.log(u"          FOLDER: " + folder.name)
			self.logBaseFolder(folder)
		for elem in indigo.triggers:
			self.logElemDivider()
			indigo.server.log(u"         TRIGGER: " + elem.name)
			self.logTrigger(elem)

	def traverseSchedules(self):
		self.logListDivider("SCHEDULES")
		for folder in indigo.schedules.folders:
			indigo.server.log(u"          FOLDER: " + folder.name)
			self.logBaseFolder(folder)
		for elem in indigo.schedules:
			self.logElemDivider()
			indigo.server.log(u"        SCHEDULE: " + elem.name)
			self.logSchedule(elem)

	def traverseActionGroups(self):
		self.logListDivider("ACTION GROUPS")
		for folder in indigo.actionGroups.folders:
			indigo.server.log(u"          FOLDER: " + folder.name)
			self.logBaseFolder(folder)
		for elem in indigo.actionGroups:
			self.logElemDivider()
			indigo.server.log(u"    ACTION GROUP: " + elem.name)
			self.logActionGroup(elem)

	def traverseControlPages(self):
		self.logListDivider("CONTROL PAGES")
		for folder in indigo.controlPages.folders:
			indigo.server.log(u"          FOLDER: " + folder.name)
			self.logBaseFolder(folder)
		for elem in indigo.controlPages:
			self.logElemDivider()
			indigo.server.log(u"    CONTROL PAGE: " + elem.name)
			self.logControlPage(elem)

	def traverseVariables(self):
		self.logListDivider("VARIABLES")
		for folder in indigo.variables.folders:
			indigo.server.log(u"          FOLDER: " + folder.name)
			self.logBaseFolder(folder)
		for elem in indigo.variables:
			self.logElemDivider()
			indigo.server.log(u"        VARIABLE: " + elem.name)
			self.logVariable(elem)

	####################
	def traverseDatabase(self):
		self.traverseDevices()
		self.traverseTriggers()
		self.traverseSchedules()
		self.traverseActionGroups()
		self.traverseControlPages()
		self.traverseVariables()

