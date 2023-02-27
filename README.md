# IndigoSDK

Indigo includes a Python-based API and object model for integrating 3rd party hardware, applications, and services into the Indigo Server. Indigo Plugins allow new native devices, triggers, and actions to be added directly to Indigo. The latest [extensive technical documentation](https://www.indigodomo.com/docs/documents#technical_documents) is available online, including:

- [Indigo Scripting Tutorial](https://www.indigodomo.com/docs/plugin_scripting_tutorial) - dive into scripting Indigo by examples.
- [Indigo Plugin Developer's Guide (current release)](https://www.indigodomo.com/docs/plugin_guide) - how to create plugin bundles for easy distribution, plugin UI, APIs, callback hooks, and more.
- [Indigo Object Model Reference (current release)](https://www.indigodomo.com/docs/object_model_reference) - the Indigo Object Model (IOM) and how to use it in Python.

### Plugin Examples

Included in this SDK are several Indigo Plugin Examples. These examples include the full python source code and XML files. To see all of the source files once downloaded to your Mac, right-click (or control-click) on the plugin bundle (.indigoPlugin file) and select **Show Package Contents** menu item. The [Plugin Developer's Guide](https://www.indigodomo.com/docs/plugin_guide) has thorough documentation on how each file is used.

**IMPORTANT:** Although these example plugins are great templates to start with, and we encourage you to copy them, you must edit the **Info.plist** file inside the bundle after you make a copy for your plugin. Inside the **Info.plist** XML file you must give the plugin a unique identifier, called the **CFBundleIndentifier**. And you should also change your plugin's display name (**CFBundleDisplayName**) and help URL (**CFBundleURLTypes**). See the [Info.plist section of the Developer's Guide](https://www.indigodomo.com/docs/plugin_guide#the_infoplist_file) for additional details.

#### Example Plugin List

This is a list of example plugins with a brief description of what each one does.

| Plugin                                                     | Description                                                                                                                                                                                                                                                                                 |
|------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Example&nbsp;Action&nbsp;API                               | This plugin illustrates how to create an API in a plugin that can be called from scripts or other plugins. If your plugin can provide some kind of information or service that's not associated with a device (as a state for instance), then this pattern is what you'd like to follow.    |
| Example&nbsp;Custom&nbsp;Broadcaster                       | This plugin illustrates how to use the publish/subscribe functionality that Indigo provides for inter-plugin communication. Specifically, this plugin illustrates how to broadcast out information to subscribers.                                                                          |
| Example&nbsp;Custom&nbsp;Subscriber                        | This plugin illustrates how to use the publish/subscribe functionality that Indigo provides for inter-plugin communication. Specifically, this plugin illustrates how to subscribe to broadcasts from the above broadcaster plugin.                                                         |
| Example&nbsp;Database&nbsp;Traverse                        | This plugin illustrates how walk through all Indigo objects and access a few of it's properties, including how to get the Folder object for the object.                                                                                                                                     |
| Example&nbsp;Device&nbsp;-&nbsp;Custom                     | This plugin illustrates how to create custom devices - those are devices that don't fall into one of the built-in device types (Dimmer, Relay, Sensor, Speed Control, Sprinkler, Thermostat). An example of a custom device might be a device representing an A/V device like an amplifier. |
| Example&nbsp;Device&nbsp;-&nbsp;Energy&nbsp;Meter          | Any device can be configured to also be an energy monitor. This plugin illustrates how to create a device that monitors energy usage.                                                                                                                                                       |
| Example&nbsp;Device&nbsp;-&nbsp;Factory                    | This plugin illustrates how to use a Device Factory to create multiple related devices. For some device types, there can actually be multiple related Indigo Devices. For instance, a multi-sensor can be multiple sensor devices including temperature, humidity, motion, etc.             |
| Example&nbsp;Device&nbsp;-&nbsp;Relay&nbsp;and&nbsp;Dimmer | This plugin illustrates how to create standard Relay (on/off) and Dimmer devices.                                                                                                                                                                                                           |
| Example&nbsp;Device&nbsp;-&nbsp;Sensor                     | This plugin illustrates how to create Sensor devices.                                                                                                                                                                                                                                       |
| Example&nbsp;Device&nbsp;-&nbsp;Speed&nbsp;Control         | This plugin illustrates how to create Speed Control devices, primarily fans.                                                                                                                                                                                                                |
| Example&nbsp;Device&nbsp;-&nbsp;Sprinkler                  | This plugin illustrates how to create Sprinkler devices.                                                                                                                                                                                                                                    |
| Example&nbsp;Device&nbsp;-&nbsp;Thermostat                 | This plugin illustrates how to create Thermostat devices.                                                                                                                                                                                                                                   |
| Example&nbsp;HTTP&nbsp;Responder                           | Any plugin can be made to respond to HTTP requests. Plugins can provide static files, like images or static HTML pages. But they can also generate dynamic HTTP content. This example plugin illustrates what you need to do to implement that functionality.                               |
| Example&nbsp;INSTEON:X10&nbsp;Listener                     | This plugin illustrates how to listen in on Insteon and X10 traffic.                                                                                                                                                                                                                        |
| Example&nbsp;Variable&nbsp;Change&nbsp;Subscriber          | This plugin illustrates how to catch changes to variables and perform actions when a variable is added, updated, or deleted.                                                                                                                                                                |
| Example&nbsp;Z-Wave&nbsp;Listener                          | This plugin illustrates how to listen in on Z-Wave traffic.                                                                                                                                                                                                                                 |


### Development Support

For help with plugin development, or to report any API problems or requests, join us on our [active and helpful developer forum.](https://forums.indigodomo.com/viewforum.php?f=18)

Copyright © 2023 Perceptive Automation, LLC. All rights reserved.
