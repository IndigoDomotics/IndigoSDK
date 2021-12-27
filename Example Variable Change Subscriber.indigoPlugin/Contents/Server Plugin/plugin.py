#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2018, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

try:
    import indigo
except:
    pass

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process. However, to avoid lots of error
# highlighting by many IDEs we added the import above which usually fixes it.

################################################################################
class Plugin(indigo.PluginBase):
    ########################################
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = True

    ########################################
    def startup(self):
        self.logger.debug(u"startup called -- subscribing to variable changes")
        # Subscribe to all variable changes
        indigo.variables.subscribeToChanges()

    def shutdown(self):
        self.logger.debug(u"shutdown called")

    ########################################
    def variableCreated(self, var):
        '''
        This method is called whenever a new variable is created.

        :param self: Your plugin instance
        :param var: The variable that has been created
        :return: No return value required
        '''
        # You must call the superclass method
        super(Plugin, self).variableCreated(var)
        self.logger.debug(u"variableCreated called for variable '{}': value: {}".format(var.name, var.value))
        # Do your stuff

    def variableUpdated(self, origVar, newVar):
        '''
        This method is called every time a variable is changed in any way (name, value, etc). Your
        plugin will likely need to inspect the variable to see if it's one you're interested in. You
        can compare the previous value to the new value if you need to.

        :param self: Your plugin instance
        :param origVar: An instance of the indigo.Variable object as it was before the change
        :param newVar: An instance of the indigo.Variable object as it is currently (after the change)
        :return: No return value required
        '''
        # You must call the superclass method
        super(Plugin, self).variableUpdated(origVar, newVar)
        self.logger.debug(u"variableUpdated called")
        self.logger.debug(u"old name: {}, old value: {}".format(origVar.name, origVar.value))
        self.logger.debug(u"new name: {}, new value: {}".format(newVar.name, newVar.value))
        # Do your stuff

    def variableDeleted(self, var):
        '''
        This method is called every time a variable is deleted. Since your plugin
        will likely depend on only specific variables, you'll want to make sure that
        you take the appropriate action when a variable that it depends on is deleted.

        :param self: Your plugin instance
        :param var: An instance of the indigo.Variable object that has been deleted
        :return: No return value required
        '''
        # You must call the superclass method
        super(Plugin, self).variableDeleted(var)
        self.logger.debug(u"variableDeleted called for variable '{}': value: {}".format(var.name, var.value))
        # Do your stuff
