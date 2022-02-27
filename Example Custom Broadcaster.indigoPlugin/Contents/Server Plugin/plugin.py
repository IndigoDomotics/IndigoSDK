#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2022, Perceptive Automation, LLC. All rights reserved.
# https://www.indigodomo.com

import indigo

import random

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug = True

    ########################################
    def startup(self):
        self.logger.debug("startup called -- broadcasting startup to all subscribers")
        # Broadcast to all listeners that we have started using the "broadcasterStarted"
        # broadcast key. Note the key is arbitrary and will just be used by the
        # subscribers in their subscribeToBroadcast() call.
        indigo.server.broadcastToSubscribers("broadcasterStarted")

    def shutdown(self):
        self.logger.debug("shutdown called -- broadcasting shutdown to all subscribers")
        # Broadcast to all listeners that we have shutdown using the "broadcasterShutdown"
        # broadcast key.
        indigo.server.broadcastToSubscribers("broadcasterShutdown")

    ########################################
    def runConcurrentThread(self):
        try:
            # Every 3 seconds broadcast to subscribers a new random color from our list:
            color_list = ["red", "green", "blue", "indigo", "orange", "black", "white", "magento", "silver", "gold"]
            while True:
                color = color_list[random.randint(0, len(color_list)-1)]
                # broadcastToSubscribers can take an additional argument to be passed to
                # the subscribers. Allowed types include basic python objects: string, number,
                # boolean, dict, or list. For server performance please keep the data size
                # sent small (a few kilobytes at most), and try not to broadcast more frequently
                # than once per second. Bursts of higher data rates should be fine.
                indigo.server.broadcastToSubscribers("colorChanged", color)
                self.sleep(3)
        except self.StopThread:
            pass  # Optionally catch the StopThread exception and do any needed cleanup.
