#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2022, Perceptive Automation, LLC. All rights reserved.
# https://www.indigodomo.com

import indigo

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)

    ########################################
    # IOM logging methods
    ####################
    def log_list_divider(self, section_name):
        self.logger.info("===================================================")
        self.logger.info(section_name)
        self.log_elem_divider()

    def log_elem_divider(self):
        self.logger.info("---------------------------------------------------")

    def log_base_elem(self, elem, folders):
        self.logger.info(f"        INSTANCE: {elem.__class__.__name__}")
        if len(elem.description) > 0:
            self.logger.info(f"     DESCRIPTION:  {elem.description}")
        if folders and elem.folderId != 0:
            self.logger.info(f"       IN FOLDER:  {folders.getName(elem.folderId)}")
        self.logger.info(f"  REMOTE DISPLAY:  {elem.remoteDisplay}")

    def log_base_folder(self, elem):
        if len(elem.description) > 0:
            self.logger.info(f"     DESCRIPTION:  {elem.description}")
        self.logger.info(f"  REMOTE DISPLAY:  {elem.remoteDisplay}")

    ########################################
    def log_device_base(self, elem):
        self.log_base_elem(elem, indigo.devices.folders)
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
    def log_device_sensor(self, elem):
        self.log_device_base(elem)
        self.logger.info(f"           IS ON:  {elem.onState}")

    ####################
    def log_device_relay(self, elem):
        self.log_device_base(elem)
        self.logger.info(f"           IS ON:  {elem.onState}")

    ####################
    def log_device_dimmer(self, elem):
        self.log_device_relay(elem)
        self.logger.info(f"      BRIGHTNESS:  {elem.brightness}")

    ####################
    def log_device_multi_io(self, elem):
        self.log_device_base(elem)
        if elem.analogInputCount > 0:
            self.logger.info(f"   ANALOG INPUTS:  {elem.analogInputs}")
        if elem.binaryInputCount > 0:
            self.logger.info(f"   BINARY INPUTS:  {elem.binaryInputs}")
        if elem.sensorInputCount > 0:
            self.logger.info(f"   SENSOR INPUTS:  {elem.sensorInputs}")
        if elem.binaryOutputCount > 0:
            self.logger.info(f"  BINARY OUTPUTS:  {elem.binaryOutputs}")

    ####################
    def log_device_sprinkler(self, elem):
        self.log_device_base(elem)
        self.logger.info(f"      ZONE COUNT:  {elem.zoneCount}")
        self.logger.info(f"      ZONE NAMES:  {elem.zoneNames}")
        self.logger.info(f"   MAX DURATIONS:  {elem.zoneMaxDurations}")
        if len(elem.zoneScheduledDurations) > 0:
            self.logger.info(f" SCHEDULED DURA.:  {elem.zoneScheduledDurations}")
        if elem.activeZone:
            self.logger.info(f"     ACTIVE ZONE:  {elem.zoneNames[elem.activeZone]}")

    ####################
    def log_device_thermostat(self, elem):
        self.log_device_base(elem)
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
    def log_device(self, elem):
        if isinstance(elem, indigo.DimmerDevice):
            self.log_device_dimmer(elem)
        elif isinstance(elem, indigo.RelayDevice):
            self.log_device_relay(elem)
        elif isinstance(elem, indigo.SensorDevice):
            self.log_device_sensor(elem)
        elif isinstance(elem, indigo.MultiIODevice):
            self.log_device_multi_io(elem)
        elif isinstance(elem, indigo.SprinklerDevice):
            self.log_device_sprinkler(elem)
        elif isinstance(elem, indigo.ThermostatDevice):
            self.log_device_thermostat(elem)
        else:
            self.log_device_base(elem)

    ########################################
    def log_event_base(self, elem, folders):
        self.log_base_elem(elem, folders)
        self.logger.info(f"         ENABLED:  {elem.enabled}")
        self.logger.info(f"          UPLOAD:  {elem.upload}")
        if elem.suppressLogging:
            self.logger.info("SUPPRESS LOGGING: True")
        # TODO: Need to add conditional tree and action list traversal here.

    ####################
    def log_trigger(self, elem):
        self.log_event_base(elem, indigo.triggers.folders)

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
    def log_schedule(self, elem):
        self.log_event_base(elem, indigo.schedules.folders)
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
            self.logger.info("  NEXT EXECUTION:  - none scheduled -")
        # TODO: Need to log additional properties after they are implemented here.

    ####################
    def log_action_group(self, elem):
        self.log_base_elem(elem, indigo.actionGroups.folders)
        # TODO: Need to add action list traversal here.

    ####################
    def log_control_page(self, elem):
        self.log_base_elem(elem, indigo.controlPages.folders)
        self.logger.info(f"     HIDE TABBAR:  {elem.hideTabBar}")
        if len(elem.backgroundImage) > 0:
            self.logger.info(f"BACKGROUND IMAGE:  {elem.backgroundImage}")
        # TODO: Need to log additional properties after they are implemented here.
        # TODO: Need to add control list traversal here.

    ####################
    def log_variable(self, elem):
        self.log_base_elem(elem, indigo.variables.folders)
        self.logger.info(f"           VALUE:  {elem.value}")
        if elem.readOnly:
            self.logger.info("       READ ONLY: True")

    ########################################
    # Actions defined in MenuItems.xml:
    ####################
    def traverse_devices(self):
        self.log_list_divider("DEVICES")
        for folder in indigo.devices.folders:
            self.logger.info(f"          FOLDER:  {folder.name}")
            self.log_base_folder(folder)
        for elem in indigo.devices:
            self.log_elem_divider()
            self.logger.info(f"          DEVICE:  {elem.name}")
            self.log_device(elem)

    def traverse_triggers(self):
        self.log_list_divider("TRIGGERS")
        for folder in indigo.triggers.folders:
            self.logger.info(f"          FOLDER:  {folder.name}")
            self.log_base_folder(folder)
        for elem in indigo.triggers:
            self.log_elem_divider()
            self.logger.info(f"         TRIGGER:  {elem.name}")
            self.log_trigger(elem)

    def traverse_schedules(self):
        self.log_list_divider("SCHEDULES")
        for folder in indigo.schedules.folders:
            self.logger.info(f"          FOLDER:  {folder.name}")
            self.log_base_folder(folder)
        for elem in indigo.schedules:
            self.log_elem_divider()
            self.logger.info(f"        SCHEDULE:  {elem.name}")
            self.log_schedule(elem)

    def traverse_action_groups(self):
        self.log_list_divider("ACTION GROUPS")
        for folder in indigo.actionGroups.folders:
            self.logger.info(f"          FOLDER:  {folder.name}")
            self.log_base_folder(folder)
        for elem in indigo.actionGroups:
            self.log_elem_divider()
            self.logger.info(f"    ACTION GROUP:  {elem.name}")
            self.log_action_group(elem)

    def traverse_control_pages(self):
        self.log_list_divider("CONTROL PAGES")
        for folder in indigo.controlPages.folders:
            self.logger.info(f"          FOLDER:  {folder.name}")
            self.log_base_folder(folder)
        for elem in indigo.controlPages:
            self.log_elem_divider()
            self.logger.info(f"    CONTROL PAGE:  {elem.name}")
            self.log_control_page(elem)

    def traverse_variables(self):
        self.log_list_divider("VARIABLES")
        for folder in indigo.variables.folders:
            self.logger.info(f"          FOLDER:  {folder.name}")
            self.log_base_folder(folder)
        for elem in indigo.variables:
            self.log_elem_divider()
            self.logger.info(f"        VARIABLE:  {elem.name}")
            self.log_variable(elem)

    ####################
    def traverse_database(self):
        self.traverse_devices()
        self.traverse_triggers()
        self.traverse_schedules()
        self.traverse_action_groups()
        self.traverse_control_pages()
        self.traverse_variables()
