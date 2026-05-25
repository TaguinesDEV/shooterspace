[app]

# Human-readable application title
title = Shooter Space

# Internal package identifiers
package.name = shooterspace
package.domain = io.github.taguinesdev

# Versioning
version = 0.1.0

# Application source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = __pycache__,tests,bin,.git,.buildozer,.sixth

# Requirements
requirements = python3,kivy

# Display
orientation = portrait
fullscreen = 1

# Android defaults for a simple Kivy game
android.archs = arm64-v8a, armeabi-v7a

# Keep the app installable while we are still local-save only
android.permissions =

[buildozer]

# Build output
log_level = 2
warn_on_root = 1
