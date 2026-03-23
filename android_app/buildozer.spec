[app]

# (str) Title of your application
title = Smart Calculator

# (str) Package name
package.name = smartcalculator

# (str) Package domain (needed for android/ios packaging)
package.domain = org.smartcat

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all files)
source.include_exts = py,png,jpg,kv,atlas,json,ttf,otf,woff,woff2

# (str) Application versioning
version = 1.0.0

# (list) Application requirements - use prebuilt
requirements = python3,kivy

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 27

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version - use older stable version
android.ndk = 23b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
