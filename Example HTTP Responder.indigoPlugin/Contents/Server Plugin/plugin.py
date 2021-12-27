#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2021, Indigo Domotics. All rights reserved.
# http://www.indigodomo.com
try:
	# This is primarily for IDEs so that they won't mark indigo stuff as undefined. The module itself is always imported
	# by the host process.
	import indigo
except:
	pass

import os
import jinja2
from datetime import datetime, date
import json
import dicttoxml

NO_FILE_SPECIFIED = "No File Specified"

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs, **kwargs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs, **kwargs)
		self.debug = True
		# Set up the environment for Jinja templates. The most important to to configure the file system loader so that
		# it points to our Resources/templates directory. Then we can just load the template via name (or name and
		# relative path within that folder if we choose).
		self.templates = jinja2.Environment(
			loader=jinja2.FileSystemLoader("../Resources/templates"),
			autoescape=True,
			auto_reload=self.debug, # this makes the templates load from disk every time you use them - good for debugging
		)
		# Next, we add some global variables that will be available to all templates automatically.
		self.templates.globals = {
			"plugin": self, # used primarily here to construct paths to the static/css directory
			"year_string": datetime.now().strftime("%Y"), # used for the copyright
		}
		self.pluginPrefs = pluginPrefs

	########################################
	def startup(self):
		self.logger.debug(u"startup called")

	def shutdown(self):
		self.logger.debug(u"shutdown called")

	########################################
	def api(self, action, dev=None, callerWaitingForResult=None):
		'''
		This handler is used to generate a simple api that returns device details for the specified device id.
		Example url:

			http://localhost:8176/message/com.indigodomo.indigoplugin.example-http-responder/api/123456.json
			http://localhost:8176/message/com.indigodomo.indigoplugin.example-http-responder/api/123456.json?condense-json=true

		The first part is the ID of a device and the extension as the type of content to return. We only do XML and JSON
		in this example. There is an optional arg to return JSON that doesn't have indents, which means it would be
		smaller. condense-json can be any value at all and it will skip the formatting with indents.

		:param action: action.props contains all the information passed from the web server
		:param dev: unused
		:param callerWaitingForResult: always True
		:return: a reply dict with the content value being JSON or XML representation of a device instance.
		'''
		self.logger.debug("Handling API request")
		props_dict = dict(action.props)
		file_path = list(props_dict["file_path"])
		reply = indigo.Dict()
		try:
			file_name = file_path[-1]
			id_string, format = file_name.split(".")
			dev_id = int(id_string)
			format = format.lower()
		except:
			self.logger.error("no file was specified in the request or the file name was incorrect")
			reply["content"] = "no file was specified in the request or the file name was incorrect"
			reply["status"] = 500
			return reply
		try:
			device = indigo.devices[dev_id]
			self.logger.debug("...for device {}".format(device.name))
			reply["status"] = 200
			if format == "xml":
				reply["content"] = dicttoxml.dicttoxml(dict(device), custom_root="Device")
			elif format == "json":
				try:
					condense = props_dict.get("url_query_args", {}).get("condense-json", False)
					if condense:
						reply["content"] = json.dumps(dict(device), separators=(',',':'), cls=indigo.utils.JSONDateEncoder)
					else:
						reply["content"] = json.dumps(dict(device), indent=4, cls=indigo.utils.JSONDateEncoder)
				except Exception as exc:
					self.logger.exception(exc)
			else:
				self.logger.error("specified format isn't supported")
				reply["content"] = "specified format isn't supported"
				reply["status"] = 500
				return reply
			reply["headers"] = {"Content-Type": "application/{}".format(format)}
			return reply
		except KeyError:
			self.logger.error("device id doesn't exist in database")
			# Here, we illustrate how to return a custom dynamic 404 page
			template = self.templates.get_template("device_missing.html")
			reply["status"] = 404
			reply["headers"] = indigo.Dict({"Content-Type": "text/html"})
			reply["content"] = template.render({"device_id": dev_id})
			return reply

	########################################
	def handle_static_file_request(self, action, dev=None, callerWaitingForResult=None):
		'''
		This handler just opens the file specified in the query string's "file-name" argument on the URL and returns
		the content. We just assume here it's some kind of text file. We'll look for the file in the Resources folder
		in this plugin. If it's not there, we'll return a 401.

		This example is here to illustrate one way to return a file from a plugin without putting it into one of the
		directories that are automatically served within the Resources folder (see the README.txt file in the Server Plugin
		folder for details on how the Indigo Web Server can automatically serve up content from your plugin.

			http://localhost:8176/message/com.indigodomo.indigoplugin.example-http-responder/handle_static_file_request/?file-name=test.csv

		:param action: action.props contains all the information passed from the web server
		:param dev: unused
		:param callerWaitingForResult: always True
		:return: a dict that contains the status, the Content-Type header, and the contents of the specified file.
		'''
		self.logger.debug("Handling HTTP request")
		props_dict = dict(action.props)
		reply = indigo.Dict()
		#######################
		# reply["content"] = "a 200 return from the plugin"
		# reply["status"] = 200
		# return reply
		#######################
		try:
			file_path = "../Resources/{}".format(props_dict["url_query_args"]["file-name"])
			self.logger.debug("...looking for file: {}".format(file_path))
		except:
			# file name wasn't specified, set a flag
			file_path = NO_FILE_SPECIFIED
		try:
			with open(file_path, "r") as f:
				file_contents = f.read()
			reply["status"] = 200
			reply["headers"] = indigo.Dict(
				{
					"Content-Type": "{}".format(
						indigo.utils.FILE_EXTENSION_MIME_MAP.get(
							os.path.splitext(file_path[-1])[-1].strip("."),
							"text/plain"
						)
					)
				}
			)
			reply["content"] = file_contents
		except:
			# file wasn't found
			if file_path == NO_FILE_SPECIFIED:
				self.logger.error("no file was specified in the request query arguments")
				reply["content"] = "no file was specified in the request query arguments"
				reply["status"] = 400
			else:
				# Here, we illustrate how to return a custom static 404 HTML page
				self.logger.error("requested file was not found: {}".format(props_dict["url_query_args"]["file-name"]))
				return indigo.utils.return_static_file(
					"{}/Contents/Resources/static/html/static_404.html".format(self.pluginFolderPath),
					status=404,
					path_is_relative=False,
				)
		return reply

	########################################
	def sample_config(self, action, dev=None, callerWaitingForResult=None):
		'''
		This handler represents a simple plugin configuration example. It will have the following URLs:

			http://localhost:8176/message/com.indigodomo.indigoplugin.example-http-responder/config

		It uses the config.html Jinja template in the templates directory. That template extends the base.html template
		file, which includes the static/css/config.css file using the built-in static file serving process for plugins.

		:param action: action.props contains all the information passed from the web server
		:param dev: unused
		:param callerWaitingForResult: always True
		:return: a dict that contains the status, the Content-Type header, and the contents of the specified file.
		'''
		self.logger.debug("Handling config request")
		props_dict = dict(action.props)
		reply = indigo.Dict()
		context = {
			"date_string": str(datetime.now()),  # Used in the config.html template
			"prefs": self.pluginPrefs,
		}
		if props_dict.get(u'incoming_request_method', "GET") == "POST":
			post_params = dict(props_dict["body_params"])
			if "operation" in post_params:
				if post_params["operation"] == "add":
					k = post_params.get("key", None)
					v = post_params.get("value", None)
					if not k or not v:
						context["error"] = "the key and value must not be empty to add them to the plugin config"
					else:
						self.pluginPrefs[k] = v
				else:
					context["error"] = "'add' is the only valid operation for this form"
			else:
				for k, v in post_params.items():
					if v == "delete":
						try:
							del(self.pluginPrefs[k])
						except:
							# probably a stale browser trying to delete a key that's already gone, just ignore it
							pass
			indigo.server.savePluginPrefs()
		try:
			template = self.templates.get_template("config.html")
			reply["status"] = 200
			reply["headers"] = indigo.Dict({"Content-Type": "text/html"})
			reply["content"] = template.render(context)
		except Exception as exc:
			# some error happened
			self.logger.error("some error occurred: {}".format(str(exc)))
			reply["status"] = 500
		return reply

	########################################
	def do_nothing(self, valuesDict, typeId):
		pass
