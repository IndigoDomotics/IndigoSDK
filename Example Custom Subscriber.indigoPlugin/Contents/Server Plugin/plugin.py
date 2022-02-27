#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2022, Perceptive Automation, LLC. All rights reserved.
# https://www.indigodomo.com

import indigo

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

# Plugin ID of the Example Custom Broadcaster plugin (taken from its Info.plist file):
BROADCASTER_PLUGINID = "com.perceptiveautomation.indigoplugin.custom-broadcaster"

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug = True

    ########################################
    def startup(self):
        self.logger.debug("startup called -- subscribing to messages from Example Custom Broadcaster plugin")
        # The Example Custom Broadcaster plugin defines three broadcast keys: broadcasterStarted,
        # broadcasterShutdown, and colorChanged. We subscribe to notifications of all three. The
        # second argument is the broadcast key used by the broadcasting plugin, the third argument
        # is the name of our callback method. In this case they are the same, but they don't have
        # to be.
        indigo.server.subscribeToBroadcast(BROADCASTER_PLUGINID, "broadcasterStarted", "broadcasterStarted")
        indigo.server.subscribeToBroadcast(BROADCASTER_PLUGINID, "broadcasterShutdown", "broadcasterShutdown")
        indigo.server.subscribeToBroadcast(BROADCASTER_PLUGINID, "colorChanged", "colorChanged")

    def shutdown(self):
        self.logger.debug("shutdown called")

    ########################################
    def broadcasterStarted(self):
        self.logger.info("received broadcasterStarted message")

    def broadcasterShutdown(self):
        self.logger.info("received broadcasterShutdown message")

    def colorChanged(self, arg):
        self.logger.info(f"received colorChanged message: {arg}")
