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

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = True

	########################################
	def startup(self):
		self.debugLog(u"startup called -- broadcasting startup to all subscribers")
		# Broadcast to all listeners that we have started using the "broadcasterStarted"
		# broadcast key. Note the key is arbitrary and will just be used by the
		# subscribers in their subscribeToBroadcast() call.
		indigo.server.broadcastToSubscribers(u"broadcasterStarted")

	def shutdown(self):
		self.debugLog(u"shutdown called -- broadcasting shutdown to all subscribers")
		# Broadcast to all listeners that we have shutdown using the "broadcasterShutdown"
		# broadcast key.
		indigo.server.broadcastToSubscribers(u"broadcasterShutdown")

	########################################
	def runConcurrentThread(self):
		try:
			# Every 3 seconds broadcast to subscribers a new random color from our list:
			colorList = ["red", "green", "blue", "indigo", "orange", "black", "white", "magento", "silver", "gold"]
			while True:
				color = colorList[random.randint(0, len(colorList)-1)]
				# broadcastToSubscribers can take an additional argument to be passed to
				# the subscribers. Allowed types include basic python objects: string, number,
				# boolean, dict, or list. For server performance please keep the data size
				# sent small (a few kilobytes at most), and try not to broadcast more frequently
				# than once per second. Bursts of higher data rates should be fine.
				indigo.server.broadcastToSubscribers(u"colorChanged", color)
				self.sleep(3)
		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.
