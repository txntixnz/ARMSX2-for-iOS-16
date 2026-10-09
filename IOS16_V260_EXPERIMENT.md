# ARMSX2 iOS 2.6.0 → iOS 16.0: experimental backport

**Status: unverified.** This branch is **not** a confirmed working iOS 16 build.

## Why 2.6.0 crashes

Official ARMSX2 **iOS** 2.6.0 requires iOS 17.4+. The iOS 16.0 crash report from 2026-10-09 showed a `DYLD / Library missing` abort for `/System/Library/Frameworks/Symbols.framework/Symbols` (in the main executable), before app code ran. Changing `MinimumOSVersion` alone cannot solve this.

## Recovery design

- Branch `ios16-stable-v25-a15` preserves the older v2.5-era core and custom controls. Do not replace or rebase it.
- This branch uses the newer iOS 2.6 frontend/core and retains the custom A15, Gran Turismo 4 pedals, and Juiced mappings from the fork's workflow.
- The iOS 16 SwiftUI backport script includes the settings-navigation source experiment from the previous draft PR.
- The native iOS app *attempts* to weak-link `Symbols.framework` (rather than requiring it at launch). This may still be insufficient when newer APIs are executed on iOS 16.
- CI checks the executable's Mach-O deployment target, the app's Info.plist minimum OS, and whether `Symbols.framework` is **strongly** linked; it will not upload an IPA if the audit fails.
- The test package uses `com.armsx2.ios.v260test` to install **alongside** your stable package `com.armsx2.ios` and leave its data alone. Libraries and save files will not automatically appear in the test app.

## Testing

1. Go to [Build iOS 16](https://github.com/txntixnz/ARMSX2-for-iOS-16/actions/workflows/build-ios16.yml) and choose branch `ios16-v260-compat-experimental`, or inspect the build automatically triggered by branch commits.
2. Download `ARMSX2-iOS16-v260-experimental-unsigned` *only after CI succeeds*.
3. Install with your existing signing/TrollStore setup. Do not delete the older installed emulator.
4. First verify **launch**, then Settings > Graphics / Audio / Game Controller with and without a connected controller, then JIT/game startup, save/load and existing custom control mappings.
5. Report the first observed fault with a device `.ips` crash report or `xcodebuild.log`. The test branch may require further SwiftUI backports.

The launch-dependency check is **necessary but not sufficient**; a weakly linked dependency can still fail when code references it at runtime. This is exploratory, not a guaranteed iOS 16 port.
