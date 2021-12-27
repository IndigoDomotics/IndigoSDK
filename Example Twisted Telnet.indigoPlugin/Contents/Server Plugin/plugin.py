#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2014, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

# *** Using Twisted inside a plugin ***
#
# Twisted (http://twistedmatrix.com) can be started inside a plugin
# runConcurrentThread() function. All factory creating and reactor.run() calls
# should be made inside runConcurrentThread().
#
# Note that callback methods from the Indigo host (for menu items, UI actions,
# etc.) are executed in a different thread than runConcurrentThread(). Because
# twisted is not threadsafe, use the reactor.callFromThread() function to
# execute any twisted functions from these callbacks. See stopConcurrentThread()
# for an example that stops the reactor safely.
#
# To test from the Terminal enter:
#
# telnet 127.0.0.1 9176
#
# Then you can enter device names which will be toggled for 2 seconds.
#
# You can use the plugin's installed menu items to disable and enable
# the remote flashing capability. The enable state, along with a global
# flash count, are automatically saved in the plugin's preferences file.

import indigo

import os
import sys

from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

kTelnetPort = 9176

################################################################################
class TelnetProtocol(LineReceiver):
	########################################
	def connectionMade(self):
		indigo.server.log(u"client connection established")
		self.sendLine("Hello there, welcome to the Indigo Twisted Plugin device flasher server.")
		if indigo.activePlugin.pluginPrefs["flashingEnabled"]:
			self.sendLine("Enter a device name:")
		else:
			self.sendLine("Sorry, but device flashing is currently disabled.")

	def connectionLost(self, reason):
		indigo.server.log(u"client connection closed")

	def lineReceived(self, deviceName):
		flashCount = int(indigo.activePlugin.pluginPrefs["flashingCount"])
		indigo.server.log(u"received client request (#%d) to flash: %s" % (flashCount, deviceName))
		if indigo.activePlugin.pluginPrefs["flashingEnabled"]:
			try:
				indigo.device.toggle(deviceName, duration=2)		# toggle the device for 2 seconds
				indigo.activePlugin.pluginPrefs["flashingCount"] += 1
			except Exception, e:
				errStr = str(e)
				self.sendLine(errStr)
				if "ElementNotFoundError" in errStr:
					indigo.activePlugin.errorLog(errStr)
				else:
					indigo.activePlugin.exceptionLog()
		else:
			self.sendLine("Sorry, but device flashing is currently disabled.")
			indigo.activePlugin.errorLog(u"** request denied -- flashing is disabled **")

################################################################################
class TelnetFactory(Factory):
	########################################
	protocol = TelnetProtocol

	def __init__(self):
		pass

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	telnetFactory = None
	listeningPort = None

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

	########################################
	def startup(self):
		if "flashingEnabled" not in self.pluginPrefs:
			self.pluginPrefs["flashingEnabled"] = True	# default (first launch) pref values
			self.pluginPrefs["flashingCount"] = 0

	def shutdown(self):		# called after runConcurrentThread() exits
		pass

	########################################
	# If runConcurrentThread() is defined, then a new thread is automatically created
	# and runConcurrentThread() is called in that thread after startup() has been called.
	#
	# runConcurrentThread() should loop forever and only return after self.stopThread
	# becomes True. If this function returns prematurely then the plugin host process
	# will log an error and attempt to call runConcurrentThread() again after several seconds.
	def runConcurrentThread(self):
		try:
			indigo.server.log(u"starting telnet server on port %d" % (kTelnetPort,))
			indigo.server.log(u"to test, open the Terminal application and enter:\n\ntelnet 127.0.0.1 %d\n" % (kTelnetPort,))
			self.telnetFactory = TelnetFactory()
			self.listeningPort = reactor.listenTCP(kTelnetPort, self.telnetFactory)
			reactor.run()
		except self.StopThread:
			pass	# Optionally catch the StopThread exception and do any needed cleanup.

	def stopConcurrentThread(self):
		super(Plugin, self).stopConcurrentThread()
		reactor.callFromThread(self.listeningPort.stopListening)
		reactor.callFromThread(reactor.stop)

	########################################
	# Actions defined in MenuItems.xml:
	####################
	def enableClientFlashingAction(self):
		indigo.server.log(u"telnet client device flashing enabled")
		self.pluginPrefs["flashingEnabled"] = True

	def disableClientFlashingAction(self):
		indigo.server.log(u"telnet client device flashing disabled")
		self.pluginPrefs["flashingEnabled"] = False

