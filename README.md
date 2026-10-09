# ARMSX2 for iOS 16 — Stable A15 Build

An **iOS-focused fork** of [ARMSX2](https://github.com/ARMSX2/ARMSX2), based on the **pre-2.6.0 / 2.5.3-era** source snapshot `19c83bf065ed21a19d8c46a1f578e37d2dab8efd`.

Designed for **iPhone 13 Pro Max (Apple A15), iOS 16.0**, with JIT available (for example via a compatible TrollStore/jailbreak setup).

## Why this stable branch exists

ARMSX2 iOS **2.6.0 officially requires iOS 17.4 or newer**. Syncing the new SwiftUI/controller-navigation frontend into an iOS 16 fork led to black settings pages, and the newer compiled app attempted to load the unavailable `Symbols.framework` at launch.

This branch restores the **previously working v2.5-era source baseline**. It is intentionally **frozen** against automatic upstream synchronizations. Do not merge `master` into this branch without a separate compatibility review.

The **`master` branch remains the current upstream-sync mirror**. For iOS 16, **build this branch**, not `master`.

## Preserved local features

- Apple **A15**-specific performance adjustments.
- Existing optional Metal presentation tuning (leave experimental 2x mode off if it stutters).
- **Gran Turismo 4** right-stick-to-analog-trigger pedal mapping and deadzone tuning.
- **Juiced** game-specific controller remapping and exclusive held-state routing.
- iOS 16 SwiftUI / Observation compatibility transforms.
- Native iOS game data and usual per-game settings. Keep the same bundle identifier `com.armsx2.ios` when installing an update.

## Build

1. Go to [Build ARMSX2 for iOS 16](https://github.com/txntixnz/ARMSX2-for-iOS-16/actions/workflows/build-ios16.yml).
2. Click **Run workflow**, choose branch **`ios16-stable-v25-a15`**, and run it.
3. After a successful workflow, download the **unsigned IPA** from the workflow's Artifacts section, install/sign with your existing iOS installation method, and check Settings and games.
4. **Do not install** an IPA if the iOS 16 compatibility audit failed. It checks both Mach-O minimum OS and unsupported linked system frameworks.

The initial recovery build needs real-device testing; a successful CI build alone is not proof that every game and settings page works.

## iOS-only checkout, shared core

The workflow fetches only the folders needed to compile the iOS app, rather than every desktop frontend. Shared `pcsx2/`, `common/`, `3rdparty/`, `cmake/`, and Android-vendored dependency sources **must remain** because the native iOS target builds from them. Deleting those folders would break the project; desktop-only directories can remain in Git history without being checked out in iOS CI.

Upstream authors and original PCSX2 contributors retain credit and ownership of their work; see [ARMSX2](https://github.com/ARMSX2/ARMSX2) and [PCSX2](https://github.com/PCSX2/pcsx2).
