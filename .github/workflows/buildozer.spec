[app]

# (str) Title of your application
title = Diabolic Peninsular

# (str) Package name
package.name = diabolicpeninsular

# (str) Package domain (needed for android/ios packaging)
package.domain = org.spectrumsecurity

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*,*.py

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec,json,md,yml,sh

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin, docs, .github

# (list) List of exclusions using pattern matching
source.exclude_patterns = license,*.apk,*.aab

# (str) Application versioning (method 1)
version = 5.3

# (str) Application versioning (method 2)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = python3,kivy,requests,bs4,flask

# (str) Custom source folders for requirements
# requirements.source.kivy = kivy

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.1.0

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 23b

# (bool) Use --private data storage (True) or --dir public storage (False)
# android.private_storage = True

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since the extra Java libs
# will be added to the APK when building.
# android.add_src =

# (list) List of Java AAR files to add to the libs so that pyjnius can access
# their classes. Don't add AARs that you do not need, since the extra Java libs
# will be added to the APK when building.
# android.add_aars =

# (list) List of Java dependencies such as 'com.google.android.gms:play-services-*:10.2.1'
# that will be added to the gradle build script. AARs and JARs listed in android.add_aars
# and android.add_src will be automatically added and do not need to be listed here.
# android.gradle_dependencies =

# (bool) Enable AndroidX support. Enable when using AndroidX libraries.
# android.enable_androidx = True

# (list) android library dependencies that will be added to the gradle build script.
# android.gradle_dependencies = 'com.android.support:support-v4:27.0.2'

# (str) Android logcat filters to use
# android.logcat_filters = *:S

# (bool) Copy library instead of making a libpyjnius.so
# android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

#
# Python for android (p4a) specific
#

# (str) python-for-android branch to use, defaults to master
# p4a.branch = master

# (str) python-for-android git clone directory (if empty, it will be automatically cloned)
# p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
# p4a.local_recipes =

# (str) Filename to the hook for p4a
# p4a.hook =

# (str) Bootstrap to use for android builds
# p4a.bootstrap = sdl2

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
# ios.kivy_ios_dir = ../kivy-ios

# (str) Name of the certificate to use for signing the debug version
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release / AppStore version
# ios.codesign.release = "iPhone Distribution: <lastname> <firstname> (<hexstring>)"

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 1

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (bool) Increment the version in the android/ios folder with the build number
# automatically? (0 = False, 1 = True)
automatic_versioning = 0

# (list) Path to the build directory
build_dir = ./build

# (list) Path to the bin directory
bin_dir = ./bin

# (str) The directory in which the android tools are stored (if empty, it will be automatically placed in the build dir)
# android.sdk_dir =

# (str) The directory in which the android NDK is stored (if empty, it will be automatically placed in the build dir)
# android.ndk_dir =

# (str) The directory in which the android Ant is stored (if empty, it will be automatically placed in the build dir)
# android.ant_dir =

# (bool) If True, then opens an SSH server in the device, and log the output
# android.ssh = False
