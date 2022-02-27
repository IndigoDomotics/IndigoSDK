#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2022, Perceptive Automation, LLC. All rights reserved.
# https://www.indigodomo.com

import indigo

import os
import sys

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
        self.logger.debug("startup called")

    def shutdown(self):
        self.logger.debug("shutdown called")

    ########################################
    # DeviceFactory methods (specified in Devices.xml):
    #
    # All device factory methods are passed a dev_id_list argument, which is
    # a list of device IDs in the current group being edited. Plugins add
    # and remove devices to/from the group by making indigo.device.create()
    # and indigo.device.delete(). On subsequent factory method calls the
    # dev_id_list will automatically be updated to reflect any changes.
    #
    # Plugins should set the main model type using dev.model, and the sub-
    # type using dev.subType, which is used for the tabbed UI. Be sure
    # and call dev.replaceOnServer() after modifying the .model and .subType
    # attributes to push those changes to the server.
    ####################
    def getDeviceFactoryUiValues(self, dev_id_list):
        values_dict = indigo.Dict()
        error_msg_dict = indigo.Dict()
        return (values_dict, error_msg_dict)

    def validateDeviceFactoryUi(self, values_dict, dev_id_list):
        errors_dict = indigo.Dict()
        return (True, values_dict, errors_dict)

    def closedDeviceFactoryUi(self, values_dict, user_cancelled, dev_id_list):
        return

    ####################
    def _get_device_group_list(self, filter, values_dict, dev_id_list):
        menu_items = []
        for dev_id in dev_id_list:
            if dev_id in indigo.devices:
                dev = indigo.devices[dev_id]
                dev_name = dev.name
            else:
                dev_name = "- device not found -"
            menu_items.append((dev_id, dev_name))
        return menu_items

    def _add_relay(self, values_dict, dev_id_list):
        newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="myRelayType")
        newdev.model = "Example Multi-Device"
        newdev.subType = "Relay"        # Manually need to set the model and subType names (for UI only)
        newdev.replaceOnServer()
        return values_dict

    def _add_dimmer(self, values_dict, dev_id_list):
        newdev = indigo.device.create(indigo.kProtocol.Plugin, deviceTypeId="myDimmerType")
        newdev.model = "Example Multi-Device"
        newdev.subType = "Dimmer"       # Manually need to set the model and subType names (for UI only)
        newdev.replaceOnServer()
        return values_dict

    def _add_x10_motion_sensor(self, values_dict, dev_id_list):
        # Not fully supported -- device groups currently should only contain
        # devices defined by the plugin. The UI doesn't properly handle showing
        # and editing X10 / INSTEON / etc. devices as part of the group.
        #
        # newdev = indigo.device.create(indigo.kProtocol.X10, deviceTypeId="Motion Detector")
        # newdev.model = "Example Multi-Device"
        # newdev.subType = "Motion" # Manually need to set the model and subType names (for UI only)
        # newdev.replaceOnServer()
        return values_dict

    def _add_x10_sprinkler_device(self, values_dict, dev_id_list):
        # Not fully supported -- device groups currently should only contain
        # devices defined by the plugin. The UI doesn't properly handle showing
        # and editing X10 / INSTEON / etc. devices as part of the group.
        #
        # newdev = indigo.device.create(indigo.kProtocol.X10, deviceTypeId="Rain8 (8 zone)")
        # newdev.model = "Example Multi-Device"
        # newdev.subType = "Sprinkler"  # Manually need to set the model and subType names (for UI only)
        # newdev.replaceOnServer()
        return values_dict

    def _remove_dimmer_devices(self, values_dict, dev_id_list):
        for dev_id in dev_id_list:
            try:
                dev = indigo.devices[dev_id]
                if dev.deviceTypeId == "myDimmerType":
                    indigo.device.delete(dev)
            except:
                pass    # delete doesn't allow (throws) on root elem
        return values_dict

    def _remove_relay_devices(self, values_dict, dev_id_list):
        for dev_id in dev_id_list:
            try:
                dev = indigo.devices[dev_id]
                if dev.deviceTypeId == "myRelayType":
                    indigo.device.delete(dev)
            except:
                pass    # delete doesn't allow (throws) on root elem
        return values_dict

    def _remove_all_devices(self, values_dict, dev_id_list):
        for dev_id in dev_id_list:
            try:
                indigo.device.delete(dev_id)
            except:
                pass    # delete doesn't allow (throws) on root elem
        return values_dict

    ########################################
    def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
        return (True, values_dict)

    ########################################
    # Relay / Dimmer Action callback
    ######################
    def actionControlDevice(self, action, dev):
        ###### TURN ON ######
        if action.deviceAction == indigo.kDeviceAction.TurnOn:
            # Command hardware module (dev) to turn ON here:
            # ** IMPLEMENT ME **
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" on")

                # And then tell the Indigo Server to update the state.
                dev.updateStateOnServer("onOffState", True)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" on failed")

        ###### TURN OFF ######
        elif action.deviceAction == indigo.kDeviceAction.TurnOff:
            # Command hardware module (dev) to turn OFF here:
            # ** IMPLEMENT ME **
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" off")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("onOffState", False)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" off failed")

        ###### TOGGLE ######
        elif action.deviceAction == indigo.kDeviceAction.Toggle:
            # Command hardware module (dev) to toggle here:
            # ** IMPLEMENT ME **
            new_on_state = not dev.onState
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" toggle")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("onOffState", new_on_state)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" toggle failed")

        ###### SET BRIGHTNESS ######
        elif action.deviceAction == indigo.kDeviceAction.SetBrightness:
            # Command hardware module (dev) to set brightness here:
            # ** IMPLEMENT ME **
            new_brightness = action.actionValue
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" set brightness to {new_brightness}")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("brightnessLevel", new_brightness)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" set brightness to {new_brightness} failed")

        ###### BRIGHTEN BY ######
        elif action.deviceAction == indigo.kDeviceAction.BrightenBy:
            # Command hardware module (dev) to do a relative brighten here:
            # ** IMPLEMENT ME **
            new_brightness = min(dev.brightness + action.actionValue, 100)
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" brighten to {new_brightness}")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("brightnessLevel", new_brightness)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" brighten to {new_brightness} failed")

        ###### DIM BY ######
        elif action.deviceAction == indigo.kDeviceAction.DimBy:
            # Command hardware module (dev) to do a relative dim here:
            # ** IMPLEMENT ME **
            new_brightness = max(dev.brightness - action.actionValue, 0)
            send_success = True      # Set to False if it failed.

            if send_success:
                # If success then log that the command was successfully sent.
                self.logger.info(f"sent \"{dev.name}\" dim to {new_brightness}")

                # And then tell the Indigo Server to update the state:
                dev.updateStateOnServer("brightnessLevel", new_brightness)
            else:
                # Else log failure but do NOT update state on Indigo Server.
                self.logger.error(f"send \"{dev.name}\" dim to {new_brightness} failed")


    ########################################
    # General Action callback
    ######################
    def actionControlUniversal(self, action, dev):
        ###### BEEP ######
        if action.deviceAction == indigo.kUniversalAction.Beep:
            # Beep the hardware module (dev) here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" beep request")

        ###### ENERGY UPDATE ######
        elif action.deviceAction == indigo.kUniversalAction.EnergyUpdate:
            # Request hardware module (dev) for its most recent meter data here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" energy update request")

        ###### ENERGY RESET ######
        elif action.deviceAction == indigo.kUniversalAction.EnergyReset:
            # Request that the hardware module (dev) reset its accumulative energy usage data here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" energy reset request")

        ###### STATUS REQUEST ######
        elif action.deviceAction == indigo.kUniversalAction.RequestStatus:
            # Query hardware module (dev) for its current status here:
            # ** IMPLEMENT ME **
            self.logger.info(f"sent \"{dev.name}\" status request")

    ########################################
    # Custom Plugin Action callbacks (defined in Actions.xml)
    ######################
    def set_backlight_brightness(self, plugin_action, dev):
        try:
            new_brightness = int(plugin_action.props.get("brightness", 100))
        except ValueError:
            # The int() cast above might fail if the user didn't enter a number:
            self.logger.error(f"set backlight brightness action to device \"{dev.name}\" -- invalid brightness value")
            return
        # Command hardware module (dev) to set backlight brightness here:
        # FIXME: add implementation here
        send_success = True     # Set to False if it failed.
        if send_success:
            # If success then log that the command was successfully sent.
            self.logger.info(f"sent \"{dev.name}\" set backlight brightness to {new_brightness}")
            # And then tell the Indigo Server to update the state:
            dev.updateStateOnServer("backlightBrightness", new_brightness)
        else:
            # Else log failure but do NOT update state on Indigo Server.
            self.logger.error(f"send \"{dev.name}\" set backlight brightness to {new_brightness} failed")
