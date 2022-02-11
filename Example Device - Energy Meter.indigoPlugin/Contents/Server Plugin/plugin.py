#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2022, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import random

import indigo
# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, plugin_id, plugin_display_name, plugin_version, plugin_prefs):
		super(Plugin, self).__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs)
		self.debug = True

	########################################
	def startup(self):
		self.logger.debug("startup called")

	def shutdown(self):
		self.logger.debug("shutdown called")

	########################################
	# Poll all of the states from the energy meter and pass new values to
	# Indigo Server.
	def _refresh_states_from_hardware(self, dev, log_refresh):
		# As an example here we update the current power (Watts) to a random
		# value, and we increase the kWh by a smidge.
		#
		# Note the states are automatically created based on the SupportsEnergyMeter
		# and SupportsPowerMeter device properties.
		#
		# The plugin instance property is updated by updating the states.
		key_value_list = list()
		if "curEnergyLevel" in dev.states:
			simulate_watts = random.randint(0, 500)
			simulate_watts_str = f"{simulate_watts} W"
			if log_refresh:
				self.logger.info(f'received "{dev.name}" power load to {simulate_watts_str}')
			key_value_list.append({'key': 'curEnergyLevel', 'value': simulate_watts, 'uiValue': simulate_watts_str})
		if "accumEnergyTotal" in dev.states:
			simulate_kwh = dev.states.get("accumEnergyTotal", 0) + 0.001
			simulate_kwh_str = f"{simulate_kwh:.3f} kWh"
			if log_refresh:
				self.logger.info(f'received "{dev.name}" energy total to {simulate_kwh_str}')
			key_value_list.append({'key': 'accumEnergyTotal', 'value': simulate_kwh, 'uiValue': simulate_kwh_str})
		dev.updateStatesOnServer(key_value_list)

	########################################
	def runConcurrentThread(self):
		try:
			while True:
				for dev in indigo.devices.iter("self"):
					if not dev.enabled or not dev.configured:
						continue
					# Plugins that need to poll out the status from the meter
					# could do so here, then broadcast back the new values to the
					# Indigo Server.
					self._refresh_states_from_hardware(dev, False)
				self.sleep(2)
		except self.StopThread:
			pass  # Optionally catch the StopThread exception and do any needed cleanup.

	########################################
	def validateDeviceConfigUi(self, values_dict, type_id, dev_id):
		return (True, values_dict)

	########################################
	def deviceStartComm(self, dev):
		# Called when communication with the hardware should be established.
		# Here would be a good place to poll out the current states from the
		# meter. If periodic polling of the meter is needed (that is, it
		# doesn't broadcast changes back to the plugin somehow), then consider
		# adding that to runConcurrentThread() above.
		self._refresh_states_from_hardware(dev, True)

	def deviceStopComm(self, dev):
		# Called when communication with the hardware should be shutdown.
		pass

	########################################
	# General Action callback
	######################
	def actionControlUniversal(self, action, dev):
		###### BEEP ######
		if action.deviceAction == indigo.kUniversalAction.Beep:
			# Beep the hardware module (dev) here:
			# FIXME: add implementation here
			self.logger.info(f"sent '{dev.name}' beep request")
		###### ENERGY UPDATE ######
		elif action.deviceAction == indigo.kUniversalAction.EnergyUpdate:
			# Request hardware module (dev) for its most recent meter data here:
			# FIXME: add implementation here
			self._refresh_states_from_hardware(dev, True)
		###### ENERGY RESET ######
		elif action.deviceAction == indigo.kUniversalAction.EnergyReset:
			# Request that the hardware module (dev) reset its accumulative energy usage data here:
			# FIXME: add implementation here
			self.logger.info(f"sent '{dev.name}' energy usage reset")
			# And then tell Indigo to reset it by just setting the value to 0.
			# This will automatically reset Indigo's time stamp for the accumulation.
			dev.updateStateOnServer("accumEnergyTotal", 0.0)
		###### STATUS REQUEST ######
		elif action.deviceAction == indigo.kUniversalAction.RequestStatus:
			# Query hardware module (dev) for its current status here:
			# FIXME: add implementation here
			self._refresh_states_from_hardware(dev, True)

	########################################
	# Custom Plugin Action callbacks (defined in Actions.xml)
	######################
	def set_backlight_brightness(self, action, dev):
		try:
			new_brightness = int(action.props.get("brightness", 100))
		except ValueError:
			# The int() cast above might fail if the user didn't enter a number:
			self.logger.info(
				f"set backlight brightness action to device '{dev.name}' -- invalid brightness value",
				isError=True
			)
			return
		# Command hardware module (dev) to set backlight brightness here:
		# FIXME: add implementation here
		send_success = True		# Set to False if it failed.
		if send_success:
			# If success then log that the command was successfully sent.
			self.logger.info(f"sent '{dev.name}' set backlight brightness to {new_brightness}")
			# And then tell the Indigo Server to update the state:
			dev.updateStateOnServer("backlightBrightness", new_brightness)
		else:
			# Else log failure but do NOT update state on Indigo Server.
			self.logger.info(f"send '{dev.name}' set backlight brightness to {new_brightness} failed", isError=True)
