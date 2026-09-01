####################
# Copyright (c) 2026, Indigo Domotics. All rights reserved.
# https://www.indigodomo.com
try:
    # This is primarily for IDEs - the indigo package is always included when a plugin is started.
    import indigo
except ImportError:
    pass



################################################################################
class Plugin(indigo.PluginBase):
    """Logs every folder and tag change the server sends us.

    Two separate subscription mechanisms are shown here:

    1. Folders -- subscribed per list, like device or variable changes, and delivered to
       folder_created() / folder_updated() / folder_deleted().
    2. The tag library -- a single global subscription, because there is one tag library
       shared by every object type rather than one per type.

    Neither arrives unless you ask for it. A plugin that never subscribes gets no folder or
    tag callbacks at all, which is deliberate: most plugins do not care, and the server does
    not send broadcasts nobody asked for.
    """

    ########################################
    def __init__(
            self: indigo.PluginBase,
            plugin_id: str,
            plugin_display_name: str,
            plugin_version: str,
            plugin_prefs: indigo.Dict,
            **kwargs: dict
    ) -> None:
        """
        The init method that is called when a plugin is first instantiated.

        :param plugin_id: the ID string of the plugin from Info.plist
        :param plugin_display_name: the name string of the plugin from Info.plist
        :param plugin_version: the version string from Info.plist
        :param plugin_prefs: an indigo.Dict containing the prefs for the plugin
        :param kwargs: passthrough for any other keyword args
        :return: None
        """
        super().__init__(plugin_id, plugin_display_name, plugin_version, plugin_prefs, **kwargs)
        self.debug: bool = False

    ########################################
    def startup(self: indigo.PluginBase) -> None:
        """
        Subscribe to the changes we want. Subscriptions have to be made before the changes
        happen, so startup is the place for them.

        :return: None
        """
        # Each object type has its own folder list, and each is subscribed to separately --
        # subscribing to device folders does not subscribe you to variable folders. Subscribe
        # only to the ones you actually care about; this example takes all six so that every
        # callback below can be demonstrated.
        indigo.devices.folders.subscribeToChanges()
        indigo.variables.folders.subscribeToChanges()
        indigo.actionGroups.folders.subscribeToChanges()
        indigo.schedules.folders.subscribeToChanges()
        indigo.triggers.folders.subscribeToChanges()
        indigo.controlPages.folders.subscribeToChanges()
        self.logger.info("subscribed to folder changes for all six object types")

        # The tag library is global -- one library shared by every object type -- so there is
        # a single subscription rather than one per list.
        #
        # Guarded because tag subscriptions are newer than folder ones: on a server that
        # predates them the method is simply absent. This is the pattern to copy if your
        # plugin has to run against more than one Indigo version -- without it the plugin
        # fails in startup() on the older server and none of the rest runs either.
        try:
            indigo.server.subscribeToTagChanges()
            self.logger.info("subscribed to tag library changes")
        except AttributeError:
            self.logger.warning(
                "this Indigo Server has no tag subscriptions -- skipping that half; "
                "the folder subscriptions above are active"
            )

    def shutdown(self: indigo.PluginBase) -> None:
        """
        Any cleanup logic needed before the plugin is completely shut down.

        :return: None
        """
        self.logger.debug("shutdown called")

    ########################################
    # Folder callbacks.
    #
    # There is one set of these for all six folder lists, so use folder.parentType to tell
    # which list a change came from: "device", "variable", "actionGroup", "schedule",
    # "trigger" or "controlPage".
    #
    # Note these are snake_case only. Unlike the older device/variable callbacks there is no
    # midCap alias (folderCreated and friends do not exist) -- these were added after Indigo
    # moved to snake_case, so there is no legacy spelling to stay compatible with.
    ########################################
    def folder_created(self: indigo.PluginBase, folder: indigo.Folder) -> None:
        """
        Called when a folder is created in one of the subscribed lists.

        :param folder: the newly created folder
        :return: None
        """
        self.logger.info(f"folder_created: {folder.parentType} folder '{folder.name}' (id {folder.id})")

    def folder_updated(
            self: indigo.PluginBase,
            orig_folder: indigo.Folder,
            new_folder: indigo.Folder
    ) -> None:
        """
        Called when a folder changes -- renamed, or its "display in remote UI" toggled.

        Both the before and after versions are passed, so you can see what actually changed
        rather than having to cache the previous state yourself.

        :param orig_folder: the folder as it was before the change
        :param new_folder: the folder as it is now
        :return: None
        """
        changes: list = []
        if orig_folder.name != new_folder.name:
            changes.append(f"name '{orig_folder.name}' -> '{new_folder.name}'")
        if orig_folder.remoteDisplay != new_folder.remoteDisplay:
            changes.append(f"remoteDisplay {orig_folder.remoteDisplay} -> {new_folder.remoteDisplay}")
        detail: str = ", ".join(changes) if changes else "no visible property change"
        self.logger.info(
            f"folder_updated: {new_folder.parentType} folder (id {new_folder.id}) -- {detail}"
        )

    def folder_deleted(self: indigo.PluginBase, folder: indigo.Folder) -> None:
        """
        Called when a folder is deleted from one of the subscribed lists.

        Objects that were in the folder are not deleted with it -- they move to the top level,
        which reaches you as an ordinary device/variable/etc. update, not as a folder change.

        :param folder: the folder as it was just before deletion
        :return: None
        """
        self.logger.info(f"folder_deleted: {folder.parentType} folder '{folder.name}' (id {folder.id})")

    ########################################
    # Tag library callbacks.
    #
    # One subscription for the whole library, because there is one library -- unlike folders,
    # which are subscribed per object type.
    #
    # Each tag arrives as a one-entry {name: "AABBCC"} map rather than a loose name and
    # color. A tag is an entry in a map everywhere in this API, so one tag is a map of one,
    # and indigo.server.tags hands back the whole library in exactly the same shape.
    #
    # Tags on an object are a different thing and do NOT come through here: adding or removing
    # a tag on a device changes the device, so it arrives as an ordinary device_updated().
    # This callback is about the library itself -- which tags exist, and what color each one
    # is. A recolor is the case that ONLY reaches you here, since recoloring a tag changes no
    # object at all.
    ########################################
    def tag_created(self: indigo.PluginBase, tag: dict) -> None:
        """
        Called when a tag is added to the server's tag library.

        :param tag: the new tag as a one-entry {name: "AABBCC"} map
        :return: None
        """
        for name, color in tag.items():
            self.logger.info(f"tag_created: '{name}' color #{color}")

    def tag_updated(self: indigo.PluginBase, orig_tag: dict, new_tag: dict) -> None:
        """
        Called when a tag is renamed and/or recolored.

        Both the before and after are given, so whichever did not change simply repeats -- a
        pure recolor has the same name in both, a pure rename the same color. That means you
        never have to have cached the previous library to see what happened.

        :param orig_tag: the tag before the change, as {name: color}
        :param new_tag: the tag after the change, as {name: color}
        :return: None
        """
        orig_name, orig_color = next(iter(orig_tag.items()))
        new_name, new_color = next(iter(new_tag.items()))
        changes: list = []
        if orig_name != new_name:
            changes.append(f"renamed '{orig_name}' -> '{new_name}'")
        if orig_color != new_color:
            changes.append(f"recolored #{orig_color} -> #{new_color}")
        self.logger.info(f"tag_updated: {', '.join(changes) if changes else 'no visible change'}")

    def tag_deleted(self: indigo.PluginBase, tag: dict) -> None:
        """
        Called when a tag is removed from the server's tag library.

        The tag is also removed from every object that carried it, and each of those objects
        reaches you as an ordinary update for its own type -- not through this callback.

        :param tag: the tag as it was just before deletion, as {name: color}
        :return: None
        """
        for name, color in tag.items():
            self.logger.info(f"tag_deleted: '{name}' color #{color}")

    ########################################
    # Menu items -- these just dump current state, so you can compare it against the
    # callbacks above as you make changes in the client.
    ########################################
    def log_folders(self: indigo.PluginBase) -> None:
        """
        Log every folder of every type.

        :return: None
        """
        folder_lists: dict = {
            "device": indigo.devices.folders,
            "variable": indigo.variables.folders,
            "actionGroup": indigo.actionGroups.folders,
            "schedule": indigo.schedules.folders,
            "trigger": indigo.triggers.folders,
            "controlPage": indigo.controlPages.folders,
        }
        for type_name, folder_list in folder_lists.items():
            names: list = [f.name for f in folder_list]
            self.logger.info(f"{type_name} folders ({len(names)}): {', '.join(names) if names else '(none)'}")

    def log_tags(self: indigo.PluginBase) -> None:
        """
        Log the server's whole tag library.

        indigo.server.tags is a {name: color} map of every tag in the library, including tags
        no object currently carries.

        :return: None
        """
        tags: dict = dict(indigo.server.tags)
        if not tags:
            self.logger.info("the tag library is empty")
            return
        self.logger.info(f"tag library ({len(tags)} tags):")
        for name, color in sorted(tags.items()):
            self.logger.info(f"    {name} = #{color}")

    def toggle_debug(self: indigo.PluginBase) -> None:
        """
        Toggle plugin debug level.

        :return: None
        """
        self.debug = not self.debug
        if self.debug:
            self.logger.info("toggling debug level on.")
        else:
            self.logger.info("toggling debug level off.")
