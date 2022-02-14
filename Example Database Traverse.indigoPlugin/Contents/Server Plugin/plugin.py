#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo

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
		self.logger.info("===================================================")
		self.logger.info(sectionName)
		self.logElemDivider()

	def logElemDivider(self):
		self.logger.info("---------------------------------------------------")

	def logBaseElem(self, elem, folders):
		self.logger.info(f"        INSTANCE: {elem.__class__.__name__}")
		if len(elem.description) > 0:
			self.logger.info(f"     DESCRIPTION:  {elem.description}")
		if folders and elem.folderId != 0:
			self.logger.info(f"       IN FOLDER:  {folders.getName(elem.folderId)}")
		self.logger.info(f"  REMOTE DISPLAY:  {elem.remoteDisplay}")

	def logBaseFolder(self, elem):
		if len(elem.description) > 0:
			self.logger.info(f"     DESCRIPTION:  {elem.description}")
		self.logger.info(f"  REMOTE DISPLAY:  {elem.remoteDisplay}")

	########################################
	def logDeviceBase(self, elem):
		self.logBaseElem(elem, indigo.devices.folders)
		self.logger.info(f"        PROTOCOL:  {elem.protocol}")
		self.logger.info(f"      MODEL NAME:  {elem.model}")
		self.logger.info(f"         ADDRESS:  {elem.address}")
		if elem.protocol == indigo.kProtocol.Insteon and elem.buttonGroupCount > 0:
			self.logger.info(f"    BUTTON COUNT:  {elem.buttonGroupCount}")
		self.logger.info(f"    LAST CHANGED:  {elem.lastChanged}")

		supports = ""
		if elem.supportsAllLightsOnOff:
			supports += "AllLightsOnOff "
		if elem.supportsAllOff:
			supports += "AllOff "
		if elem.supportsStatusRequest:
			supports += "StatusRequest "
		if len(supports) == 0:
			supports = "--"
		self.logger.info(f"        SUPPORTS:  {supports}")

	####################
	def logDeviceSensor(self, elem):
		self.logDeviceBase(elem)
		self.logger.info(f"           IS ON:  {elem.onState}")

	####################
	def logDeviceRelay(self, elem):
		self.logDeviceBase(elem)
		self.logger.info(f"           IS ON:  {elem.onState}")

	####################
	def logDeviceDimmer(self, elem):
		self.logDeviceRelay(elem)
		self.logger.info(f"      BRIGHTNESS:  {elem.brightness}")

	####################
	def logDeviceMultiIO(self, elem):
		self.logDeviceBase(elem)
		if elem.analogInputCount > 0:
			self.logger.info(f"   ANALOG INPUTS:  {elem.analogInputs}")
		if elem.binaryInputCount > 0:
			self.logger.info(f"   BINARY INPUTS:  {elem.binaryInputs}")
		if elem.sensorInputCount > 0:
			self.logger.info(f"   SENSOR INPUTS:  {elem.sensorInputs}")
		if elem.binaryOutputCount > 0:
			self.logger.info(f"  BINARY OUTPUTS:  {elem.binaryOutputs}")

	####################
	def logDeviceSprinkler(self, elem):
		self.logDeviceBase(elem)
		self.logger.info(f"      ZONE COUNT:  {elem.zoneCount}")
		self.logger.info(f"      ZONE NAMES:  {elem.zoneNames}")
		self.logger.info(f"   MAX DURATIONS:  {elem.zoneMaxDurations}")
		if len(elem.zoneScheduledDurations) > 0:
			self.logger.info(f" SCHEDULED DURA.:  {elem.zoneScheduledDurations}")
		if elem.activeZone:
			self.logger.info(f"     ACTIVE ZONE:  {elem.zoneNames[elem.activeZone]}")

	####################
	def logDeviceThermostat(self, elem):
		self.logDeviceBase(elem)
		self.logger.info(f"       HVAC MODE:  {elem.hvacMode}")
		self.logger.info(f"        FAN MODE:  {elem.fanMode}")
		self.logger.info(f"   COOL SETPOINT:  {elem.coolSetpoint}")
		self.logger.info(f"   HEAT SETPOINT:  {elem.heatSetpoint}")
		self.logger.info(f"      TEMP COUNT:  {elem.temperatureSensorCount}")
		self.logger.info(f"           TEMPS:  {elem.temperatures}")
		self.logger.info(f"  HUMIDITY COUNT:  {elem.humiditySensorCount}")
		self.logger.info(f"        HUMIDITY:  {elem.humidities}")
		self.logger.info(f"      COOL IS ON:  {elem.coolIsOn}")
		self.logger.info(f"      HEAT IS ON:  {elem.heatIsOn}")
		self.logger.info(f"       FAN IS ON:  {elem.fanIsOn}")

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
		self.logger.info(f"         ENABLED:  {elem.enabled}")
		self.logger.info(f"          UPLOAD:  {elem.upload}")
		if elem.suppressLogging:
			self.logger.info("SUPPRESS LOGGING: True")
		# TODO: Need to add conditional tree and action list traversal here.

	####################
	def logTrigger(self, elem):
		self.logEventBase(elem, indigo.triggers.folders)

		if isinstance(elem, indigo.DeviceStateChangeTrigger):
			self.logger.info(f"          DEVICE:  {indigo.devices.getName(elem.deviceId)}")
			self.logger.info(f"     CHANGE TYPE:  {elem.stateChangeType}")
			self.logger.info(f"    SELECTOR KEY:  {elem.stateSelector}")
			if elem.stateSelectorIndex > 0:
				self.logger.info(f"  SELECTOR INDEX:  {elem.stateSelectorIndex}")
			if len(elem.stateValue) > 0:
				self.logger.info(f"     STATE VALUE:  {elem.stateValue}")
		elif isinstance(elem, indigo.VariableValueChangeTrigger):
			self.logger.info(f"        VARIABLE:  {indigo.variables.getName(elem.variableId)}")
			self.logger.info(f"     CHANGE TYPE:  {elem.variableChangeType}")
			if len(elem.variableValue) > 0:
				self.logger.info(f"  VARIABLE VALUE:  {elem.variableValue}")
		elif isinstance(elem, indigo.InsteonCommandReceivedTrigger):
			self.logger.info(f" INSTEON COMMAND:  {elem.command}")
			self.logger.info(f"     SOURCE TYPE:  {elem.commandSourceType}")
			if elem.commandSourceType == indigo.kDeviceSourceType.DeviceId:
				self.logger.info(f"          DEVICE:  {indigo.devices.getName(elem.deviceId)}")
			self.logger.info(f"       GROUP NUM:  {elem.buttonOrGroup}")
		elif isinstance(elem, indigo.X10CommandReceivedTrigger):
			self.logger.info(f"     X10 COMMAND:  {elem.command}")
			self.logger.info(f"     SOURCE TYPE:  {elem.commandSourceType}")
			if elem.commandSourceType == indigo.kDeviceSourceType.DeviceId:
				self.logger.info(f"          DEVICE:  {indigo.devices.getName(elem.deviceId)}")
			elif elem.commandSourceType == indigo.kDeviceSourceType.RawAddress:
				self.logger.info(f"         ADDRESS:  {elem.address}")
			elif elem.command == indigo.kX10Cmd.AvButtonPressed:
				self.logger.info(f"      A/V BUTTON:  {elem.avButton}")
		elif isinstance(elem, indigo.EmailReceivedTrigger):
			self.logger.info(f"    EMAIL FILTER:  {elem.emailFilter}")
			if elem.emailFilter == indigo.kEmailFilter.MatchEmailFields:
				self.logger.info(f"     FROM FILTER:  {elem.emailFrom}")
				self.logger.info(f"  SUBJECT FILTER:  {elem.emailSubject}")

	####################
	def logSchedule(self, elem):
		self.logEventBase(elem, indigo.schedules.folders)
		self.logger.info(f"       DATE TYPE:  {elem.dateType}")
		self.logger.info(f"       TIME TYPE:  {elem.timeType}")
		if elem.dateType == indigo.kDateType.Absolute and elem.timeType == indigo.kTimeType.Absolute:
			self.logger.info(f"   DATE AND TIME:  {elem.absoluteDateTime}")
		elif elem.dateType == indigo.kDateType.Absolute:
			self.logger.info(f"   ABSOLUTE DATE:  {elem.absoluteDate.date()}")
		elif elem.timeType == indigo.kTimeType.Absolute:
			self.logger.info(f"   ABSOLUTE TIME:  {elem.absoluteTime.time()}")
		if elem.sunDelta > 0:
			self.logger.info(f"       SUN DELTA:  {elem.sunDelta} seconds")
		if elem.randomizeBy > 0:
			self.logger.info(f"    RANDOMIZE BY:  {elem.randomizeBy} seconds")
		try:
			self.logger.info(f"  NEXT EXECUTION:  {elem.nextExecution}")
		except:
			self.logger.info(f"  NEXT EXECUTION:  - none scheduled -")
		# TODO: Need to log additional properties after they are implemented here.

	####################
	def logActionGroup(self, elem):
		self.logBaseElem(elem, indigo.actionGroups.folders)
		# TODO: Need to add action list traversal here.

	####################
	def logControlPage(self, elem):
		self.logBaseElem(elem, indigo.controlPages.folders)
		self.logger.info(f"     HIDE TABBAR:  {elem.hideTabBar}")
		if len(elem.backgroundImage) > 0:
			self.logger.info(f"BACKGROUND IMAGE:  {elem.backgroundImage}")
		# TODO: Need to log additional properties after they are implemented here.
		# TODO: Need to add control list traversal here.

	####################
	def logVariable(self, elem):
		self.logBaseElem(elem, indigo.variables.folders)
		self.logger.info(f"           VALUE:  {elem.value}")
		if elem.readOnly:
			self.logger.info("       READ ONLY: True")

	########################################
	# Actions defined in MenuItems.xml:
	####################
	def traverseDevices(self):
		self.logListDivider("DEVICES")
		for folder in indigo.devices.folders:
			self.logger.info(f"          FOLDER:  {folder.name}")
			self.logBaseFolder(folder)
		for elem in indigo.devices:
			self.logElemDivider()
			self.logger.info(f"          DEVICE:  {elem.name}")
			self.logDevice(elem)

	def traverseTriggers(self):
		self.logListDivider("TRIGGERS")
		for folder in indigo.triggers.folders:
			self.logger.info(f"          FOLDER:  {folder.name}")
			self.logBaseFolder(folder)
		for elem in indigo.triggers:
			self.logElemDivider()
			self.logger.info(f"         TRIGGER:  {elem.name}")
			self.logTrigger(elem)

	def traverseSchedules(self):
		self.logListDivider("SCHEDULES")
		for folder in indigo.schedules.folders:
			self.logger.info(f"          FOLDER:  {folder.name}")
			self.logBaseFolder(folder)
		for elem in indigo.schedules:
			self.logElemDivider()
			self.logger.info(f"        SCHEDULE:  {elem.name}")
			self.logSchedule(elem)

	def traverseActionGroups(self):
		self.logListDivider("ACTION GROUPS")
		for folder in indigo.actionGroups.folders:
			self.logger.info(f"          FOLDER:  {folder.name}")
			self.logBaseFolder(folder)
		for elem in indigo.actionGroups:
			self.logElemDivider()
			self.logger.info(f"    ACTION GROUP:  {elem.name}")
			self.logActionGroup(elem)

	def traverseControlPages(self):
		self.logListDivider("CONTROL PAGES")
		for folder in indigo.controlPages.folders:
			self.logger.info(f"          FOLDER:  {folder.name}")
			self.logBaseFolder(folder)
		for elem in indigo.controlPages:
			self.logElemDivider()
			self.logger.info(f"    CONTROL PAGE:  {elem.name}")
			self.logControlPage(elem)

	def traverseVariables(self):
		self.logListDivider("VARIABLES")
		for folder in indigo.variables.folders:
			self.logger.info(f"          FOLDER:  {folder.name}")
			self.logBaseFolder(folder)
		for elem in indigo.variables:
			self.logElemDivider()
			self.logger.info(f"        VARIABLE:  {elem.name}")
			self.logVariable(elem)

	####################
	def traverseDatabase(self):
		self.traverseDevices()
		self.traverseTriggers()
		self.traverseSchedules()
		self.traverseActionGroups()
		self.traverseControlPages()
		self.traverseVariables()
