#!/usr/bin/env python3
"""Fail a purported iOS 16 ARMSX2 IPA build when it has launch-time blockers.

Run on macOS after xcodebuild; this is not a substitute for on-device testing.
"""
import pathlib
import re
import subprocess
import sys

app = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
    "platforms/ios/build-ios-xcode/Release-iphoneos/ARMSX2iOS.app"
)
binary = app / "ARMSX2iOS"


def run(*command):
    return subprocess.check_output(command, text=True)


min_os = run("/usr/libexec/PlistBuddy", "-c", "Print :MinimumOSVersion",
             str(app / "Info.plist")).strip()
print(f"Info.plist MinimumOSVersion: {min_os}")
if not re.fullmatch(r"16(?:\.[0-9]+)*", min_os):
    sys.exit("ERROR: Info.plist does not target iOS 16.")

build = run("xcrun", "vtool", "-show-build", str(binary))
print("Mach-O build version:\n" + build)
if not re.search(r"minos\s+16(?:\.[0-9]+)*", build):
    sys.exit("ERROR: Mach-O does not target iOS 16.")

loads = run("xcrun", "otool", "-l", str(binary))
for command in re.split(r"(?m)^Load command [0-9]+\s*$", loads):
    cmd = re.search(r"(?m)^\s*cmd\s+(LC_LOAD(?:_WEAK)?_DYLIB)\s*$", command)
    if cmd is None:
        continue
    name = re.search(r"(?m)^\s*name\s+(\S+)", command)
    if not name or "/Symbols.framework/Symbols" not in name.group(1):
        continue
    print(f"Symbols.framework load command: {cmd.group(1)}")
    if cmd.group(1) != "LC_LOAD_WEAK_DYLIB":
        sys.exit(
            "ERROR: strong Symbols.framework dependency; "
            "app will abort at launch on iOS 16."
        )

print("Passed launch-dependency audit; iOS 16 UI/runtime testing still required.")
