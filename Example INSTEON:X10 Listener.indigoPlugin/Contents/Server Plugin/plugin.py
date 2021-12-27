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
		self.debugLog(u"startup called -- subscribing to all X10 and INSTEON commands")
		indigo.insteon.subscribeToIncoming()
		indigo.insteon.subscribeToOutgoing()
		indigo.x10.subscribeToIncoming()
		indigo.x10.subscribeToOutgoing()

	def shutdown(self):
		self.debugLog(u"shutdown called")

	########################################
	def insteonCommandReceived(self, cmd):
		self.debugLog(u"insteonCommandReceived: \n" + str(cmd))

	def insteonCommandSent(self, cmd):
		self.debugLog(u"insteonCommandSent: \n" + str(cmd))

	########################################
	def x10CommandReceived(self, cmd):
		self.debugLog(u"x10CommandReceived: \n" + str(cmd))

		if cmd.cmdType == "sec":	# or "x10" for power line commands
			if cmd.secCodeId == 6:
				if cmd.secFunc == "sensor alert (max delay)":
					indigo.server.log(u"SENSOR OPEN")
				elif cmd.secFunc == "sensor normal (max delay)":
					indigo.server.log(u"SENSOR CLOSED")

	def x10CommandSent(self, cmd):
		self.debugLog(u"x10CommandSent: \n" + str(cmd))

