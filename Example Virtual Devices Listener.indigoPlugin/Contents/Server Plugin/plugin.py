#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2026, Perceptive Automation, LLC. All rights reserved.
# https://www.indigodomo.com

try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
    """Logs what the Virtual Devices interface does.

    Virtual Devices is the built-in plugin behind Device Groups, Virtual On/Off Devices,
    Sprinkler Groups and Virtual Sensors. It has no hardware: it watches other devices and
    variables, and sends ordinary commands to them. indigo.virtual_devices lets a plugin
    listen to both halves, the same way indigo.zwave and indigo.insteon do for their traffic.
    """

    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
        self.debug: bool = False

    ########################################
    def startup(self):
        if not indigo.virtual_devices.is_enabled():
            self.logger.warning("the Virtual Devices plugin is not running; nothing will arrive until it is")
        # Incoming: a device or variable change made Virtual Devices update one of its devices.
        indigo.virtual_devices.subscribe_to_incoming()
        # Outgoing: Virtual Devices sent a command on behalf of one of its devices.
        indigo.virtual_devices.subscribe_to_outgoing()
        self.logger.info("subscribed to Virtual Devices messages")

    def shutdown(self):
        self.logger.debug("shutdown called")

    def toggle_debug(self):
        """Toggle plugin debug level."""
        self.debug = not self.debug
        self.logger.info(f"debug logging is {'on' if self.debug else 'off'}")

    ########################################
    def virtual_devices_command_received(self, msg):
        """Called after subscribe_to_incoming(). msg holds:

        virtual_device_id   the Virtual Devices device that was updated
        source_type         what changed, as the name of an indigo.TargetType member:
                            "indigo.TargetType.DEVICE" or "indigo.TargetType.VARIABLE".
                            eval(msg["source_type"]) gives the member itself.
        source_id           id of that device or variable
        on_state            the on/off state the virtual device was given, or
        error               the error text it was given instead (then there is no on_state)
        """
        if "error" in msg:
            outcome = f"error '{msg['error']}'"
        else:
            outcome = "on" if msg["on_state"] else "off"
        self.logger.info(
            f"received: {msg['source_type']} {msg['source_id']} changed, "
            f"so virtual device {msg['virtual_device_id']} is now {outcome}"
        )

    def virtual_devices_command_sent(self, msg):
        """Called after subscribe_to_outgoing(). msg holds:

        virtual_device_id   the Virtual Devices device the command was sent for
        target_type         what the command went to, as the name of an indigo.TargetType
                            member: "indigo.TargetType.DEVICE" or
                            "indigo.TargetType.ACTION_GROUP"
        target_id           id of that device or action group
        command             the command as the rest of Indigo names it: "indigo.device.turnOn",
                            "indigo.device.turnOff", "indigo.dimmer.setBrightness",
                            "indigo.sprinkler.setActiveZone" or "indigo.actionGroup.execute"
        value               the brightness or zone number; left out for commands without one
        """
        value = f" {msg['value']}" if "value" in msg else ""
        self.logger.info(
            f"sent: {msg['command']}{value} to {msg['target_type']} {msg['target_id']} "
            f"for virtual device {msg['virtual_device_id']}"
        )
