#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2016, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo

import os
import sys
import random

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

# Plugin ID of the Example Custom Broadcaster plugin (taken from its Info.plist file):
kBroadcasterPluginId = "com.perceptiveautomation.indigoplugin.custom-broadcaster"

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = True

	########################################
	def startup(self):
		self.debugLog(u"startup called -- subscribing to messages from Example Custom Broadcaster plugin")
		# The Example Custom Broadcaster plugin defines three broadcast keys: broadcasterStarted,
		# broadcasterShutdown, and colorChanged. We subscribe to notifications of all three. The
		# second argument is the broadcast key used by the broadcasting plugin, the third argument
		# is the name of our callback method. In this case they are the same, but they don't have
		# to be.
		indigo.server.subscribeToBroadcast(kBroadcasterPluginId, u"broadcasterStarted", u"broadcasterStarted")
		indigo.server.subscribeToBroadcast(kBroadcasterPluginId, u"broadcasterShutdown", u"broadcasterShutdown")
		indigo.server.subscribeToBroadcast(kBroadcasterPluginId, u"colorChanged", u"colorChanged")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	########################################
	def broadcasterStarted(self):
		self.logger.info(u"received broadcasterStarted message")

	def broadcasterShutdown(self):
		self.logger.info(u"received broadcasterShutdown message")

	def colorChanged(self, arg):
		self.logger.info(u"received colorChanged message: %s" % (arg))
