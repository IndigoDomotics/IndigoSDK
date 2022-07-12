#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2022, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
try:
    # This is primarily for IDEs - the indigo package is always included.
    import indigo
except:
    pass

import json
import yaml
import dicttoxml

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs):
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs)
        self.debug = True

    ########################################
    def startup(self):
        self.logger.debug("startup called")

    def shutdown(self):
        self.logger.debug("shutdown called")

    @staticmethod
    def validate_device_info_action(dev_id, props):
        errors = indigo.Dict()
        if dev_id not in indigo.devices:
            errors["device"] = "'deviceId' must be included and must represent an existing device"
        if "format" not in props:
            errors["format"] = "'format' parameter is missing"
        elif props["format"] not in ["json", "xml", "yaml"]:
            errors["format"] = f"{props['format']} must be one of: 'json', 'xml', 'yaml'"
        return (bool(errors), errors)  # bool(errors) will return False if empty, True if not)

    ########################################
    def get_device_info(self, action, dev=None, caller_waiting_for_result=None):
        '''
        This handler is used to generate a simple api that returns device details for the specified device id. We lifted
        this example from the HTTP Responder plugin, but rather than return an HTML page, we'll just return an
        indigo.Dict to the caller for the device.

        We will also illustrate a pattern you can use for validating actions, both actions called as an API and actions
        configured and called through the UI. Historically, all validation has been done in the validate*ConfigUI
        methods, but for actions which can also be called from scripts or other plugins, that will not suffice since
        they construct their own properties to pass to the action and those aren't passed through the validate methods.
        It is also possible that the conditions will change at runtime from when the user configured the action - the
        most obvious scenario is if the user specifies substitution patterns in the action config. Since those values
        will most often change between the time the action was configured and the time the action runs, it's usually
        prudent to validate just before the action runs.

        The first part is the ID of a device and the extension as the type of content to return. We only do XML and JSON
        in this example. There is an optional arg to return JSON that doesn't have indents, which means it would be
        smaller. condense-json can be any value at all and it will skip the formatting with indents.

        :param action: action.props contains all the information passed from the action config or executeAction call
        :param dev: device whose details to return in the appropriate format
        :param caller_waiting_for_result: this will be true if it's an API call or false if it's called via the server
        :return: a reply dict with the content value being JSON or XML representation of a device instance.
        '''
        reply_dict = indigo.Dict()  # This will hold the status and errors or device details in the appropriate format
        props = dict(action.props)
        is_valid, errors = self.validate_device_info_action(dev.id, action.props)
        reply_dict["status"] = is_valid
        if not is_valid:
            if caller_waiting_for_result:
                self.logger.error(
                    f"Couldn't complete 'get_device_info' scripting action because of errors:\n{dict(errors)}")
            else:
                self.logger.error(f"Couldn't complete 'Get Device Info' action because of errors:\n{dict(errors)}")
            reply_dict["errors"] = errors
        else:
            device_dict = dict(dev)
            if props["format"] == "yaml":
                reply_dict["deviceInfo"] = yaml.dump(device_dict)
            elif props["format"] == "xml":
                reply_dict["deviceInfo"] = dicttoxml.dicttoxml(device_dict)
            else:
                reply_dict["deviceInfo"] = json.dumps(device_dict, indent=2, cls=indigo.utils.JSONDateEncoder)
            if not caller_waiting_for_result:
                # We're only going to write to the log if it's called from the UI action
                self.logger.info(f"Device details for device '{dev.name}':\n{reply_dict['deviceInfo']}")
        return reply_dict

    ########################################
    def validateActionConfigUi(self, values_dict, type_id, dev_id):
        # If the type_id is "scene", we want to clear the selections on both
        # dynamic lists so that they're not stored since we really don't
        # care about those.
        self.logger.debug(f"validateDeviceConfigUi: type_id: {type_id}  dev_id: {dev_id}")
        if type_id == "get_device_info":
            is_valid, errors = self.validate_device_info_action(dev_id, values_dict)
            return (is_valid, values_dict, errors)
        else:
            return (True, values_dict)

