# TODO

Small, plan-less changes for this repo. See `dev-standards/todo-format.md` for the format
and the TODO → OmniFocus → CHANGELOG lifecycle. Lines tagged `Indigo Future` get no OmniFocus
task until they are retargeted to a specific release.

## Bug

- [ ] Custom Subscriber's `BROADCASTER_PLUGINID` is `com.perceptiveautomation.indigoplugin.custom-broadcaster`, but the Broadcaster's ID is `com.example.indigoplugin.custom-broadcaster`, so it never receives anything `Indigo Future`
- [ ] Debug toggle logs the opposite state in 15 of 16 examples ("toggling debug level off." right after turning it on) `Indigo Future`
- [ ] Action API's `validateActionConfigUi` has a copy-pasted docstring ("scene" type, dynamic lists) and logs `validateDeviceConfigUi` `Indigo Future`

## Docs

- [ ] Six examples have no deep-link help URL because the SDK docs page lacks their sections: Broadcaster, Subscriber, Factory, Thermostat, Variable Change Subscriber, ZWave Listener `Indigo Future`

## Research / Spike

- [ ] Work out how `IndigoSDK.dmg` gets built: `copy_sdk` publishes `$BUILDBASE/$SDK_PATH`, but `build_settings` defines only `SDK_BUILD_PATH` and no script builds the DMG `Indigo Future`
