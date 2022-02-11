#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2022, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo

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
		self.debugLog("startup called -- subscribing to messages from Example Custom Broadcaster plugin")
		# The Example Custom Broadcaster plugin defines three broadcast keys: broadcasterStarted,
		# broadcasterShutdown, and colorChanged. We subscribe to notifications of all three. The
		# second argument is the broadcast key used by the broadcasting plugin, the third argument
		# is the name of our callback method. In this case they are the same, but they don't have
		# to be.
		indigo.server.subscribeToBroadcast(kBroadcasterPluginId, "broadcasterStarted", "broadcasterStarted")
		indigo.server.subscribeToBroadcast(kBroadcasterPluginId, "broadcasterShutdown", "broadcasterShutdown")
		indigo.server.subscribeToBroadcast(kBroadcasterPluginId, "colorChanged", "colorChanged")

	def shutdown(self):
		self.logger.debug("shutdown called")

	########################################
	def broadcasterStarted(self):
		self.logger.info("received broadcasterStarted message")

	def broadcasterShutdown(self):
		self.logger.info("received broadcasterShutdown message")

	def colorChanged(self, arg):
		self.logger.info(f"received colorChanged message: {arg}")
